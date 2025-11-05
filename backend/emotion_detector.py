import cv2
import mediapipe as mp
import numpy as np
import time
from collections import deque

class EmotionAnxietyDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Tracking variables
        self.blink_counter = 0
        self.blink_times = deque(maxlen=100)
        self.movement_history = deque(maxlen=50)
        self.face_positions = deque(maxlen=30)
        self.start_time = time.time()
        
        # Eye landmarks for blink detection
        self.LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
        self.RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
        
    def calculate_ear(self, landmarks, eye_points):
        """Calculate Eye Aspect Ratio for blink detection"""
        eye_landmarks = np.array([(landmarks[point].x, landmarks[point].y) for point in eye_points])
        
        # Vertical distances
        A = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        B = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        
        # Horizontal distance
        C = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])
        
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_movement(self, face_center):
        """Detect excessive head movement"""
        self.face_positions.append(face_center)
        
        if len(self.face_positions) >= 10:
            positions = np.array(self.face_positions)
            movement = np.std(positions, axis=0)
            total_movement = np.sqrt(movement[0]**2 + movement[1]**2)
            return total_movement
        return 0
    
    def analyze_frame(self, frame):
        """Analyze single frame for anxiety indicators"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        anxiety_indicators = {
            'blink_rate': 0,
            'movement_level': 0,
            'face_detected': False,
            'timestamp': time.time() - self.start_time
        }
        
        if results.multi_face_landmarks:
            anxiety_indicators['face_detected'] = True
            
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                
                # Calculate EAR for both eyes
                left_ear = self.calculate_ear(landmarks, self.LEFT_EYE)
                right_ear = self.calculate_ear(landmarks, self.RIGHT_EYE)
                ear = (left_ear + right_ear) / 2.0
                
                # Blink detection
                if ear < 0.25:  # Threshold for closed eye
                    self.blink_counter += 1
                    self.blink_times.append(time.time())
                
                # Calculate blink rate (blinks per minute)
                current_time = time.time()
                recent_blinks = [t for t in self.blink_times if current_time - t < 60]
                anxiety_indicators['blink_rate'] = len(recent_blinks)
                
                # Face center for movement detection
                face_center = (
                    landmarks[1].x * frame.shape[1],
                    landmarks[1].y * frame.shape[0]
                )
                anxiety_indicators['movement_level'] = self.detect_movement(face_center)
        
        return anxiety_indicators
    
    def get_anxiety_score(self, indicators_history):
        """Calculate overall anxiety score based on indicators"""
        if not indicators_history:
            return 0
        
        avg_blink_rate = np.mean([i['blink_rate'] for i in indicators_history])
        avg_movement = np.mean([i['movement_level'] for i in indicators_history])
        
        # Normalize scores (normal blink rate: 15-20 per minute)
        blink_score = max(0, min(100, (avg_blink_rate - 15) * 5))
        movement_score = min(100, avg_movement * 1000)
        
        anxiety_score = (blink_score + movement_score) / 2
        return min(100, anxiety_score)