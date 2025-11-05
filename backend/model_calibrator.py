import numpy as np
import json
import os
from datetime import datetime

class ModelCalibrator:
    def __init__(self):
        self.calibration_file = "model_calibration.json"
        self.load_calibration()
    
    def load_calibration(self):
        """Load existing calibration data"""
        if os.path.exists(self.calibration_file):
            with open(self.calibration_file, 'r') as f:
                self.calibration = json.load(f)
        else:
            self.calibration = {
                'visual': {
                    'baseline_blink_rate': 17.5,  # Normal average
                    'baseline_movement': 0.02,
                    'confidence_threshold': 0.6
                },
                'voice': {
                    'baseline_pause_frequency': 3.0,  # per minute
                    'baseline_pause_duration': 0.8,   # seconds
                    'baseline_speech_ratio': 0.55
                },
                'last_updated': None,
                'sample_count': 0
            }
    
    def save_calibration(self):
        """Save calibration data"""
        self.calibration['last_updated'] = datetime.now().isoformat()
        with open(self.calibration_file, 'w') as f:
            json.dump(self.calibration, f, indent=2)
    
    def update_visual_baseline(self, session_data):
        """Update visual analysis baseline from valid sessions"""
        valid_data = [d for d in session_data if d.get('face_detected', False)]
        if len(valid_data) < 10:  # Need minimum data
            return
        
        # Calculate new baselines
        blink_rates = [d['blink_rate'] for d in valid_data if d['blink_rate'] > 0]
        movements = [d['movement_level'] for d in valid_data if d['movement_level'] > 0]
        
        if blink_rates:
            # Use median for robustness against outliers
            new_blink_baseline = np.median(blink_rates)
            # Weighted update (70% old, 30% new)
            self.calibration['visual']['baseline_blink_rate'] = (
                self.calibration['visual']['baseline_blink_rate'] * 0.7 + 
                new_blink_baseline * 0.3
            )
        
        if movements:
            new_movement_baseline = np.median(movements)
            self.calibration['visual']['baseline_movement'] = (
                self.calibration['visual']['baseline_movement'] * 0.7 + 
                new_movement_baseline * 0.3
            )
    
    def update_voice_baseline(self, voice_results):
        """Update voice analysis baseline"""
        if voice_results['total_pauses'] == 0:
            return
        
        # Calculate pause frequency (per minute)
        audio_duration = 120  # 2 minutes typical
        pause_frequency = voice_results['total_pauses'] / (audio_duration / 60)
        
        # Update baselines with weighted average
        self.calibration['voice']['baseline_pause_frequency'] = (
            self.calibration['voice']['baseline_pause_frequency'] * 0.8 + 
            pause_frequency * 0.2
        )
        
        if voice_results['avg_pause_duration'] > 0:
            self.calibration['voice']['baseline_pause_duration'] = (
                self.calibration['voice']['baseline_pause_duration'] * 0.8 + 
                voice_results['avg_pause_duration'] * 0.2
            )
    
    def calibrate_visual_score(self, raw_score, blink_rate, movement_level):
        """Calibrate visual anxiety score based on user baseline"""
        baseline_blink = self.calibration['visual']['baseline_blink_rate']
        baseline_movement = self.calibration['visual']['baseline_movement']
        
        # Adjust blink rate scoring
        if blink_rate > 0:
            blink_deviation = (blink_rate - baseline_blink) / baseline_blink
            blink_adjustment = blink_deviation * 20  # Scale factor
        else:
            blink_adjustment = 0
        
        # Adjust movement scoring
        if movement_level > 0 and baseline_movement > 0:
            movement_deviation = (movement_level - baseline_movement) / baseline_movement
            movement_adjustment = movement_deviation * 15
        else:
            movement_adjustment = 0
        
        # Combine adjustments
        calibrated_score = raw_score + blink_adjustment + movement_adjustment
        return max(0, min(100, calibrated_score))
    
    def calibrate_voice_score(self, raw_score, voice_results):
        """Calibrate voice anxiety score based on user baseline"""
        baseline_freq = self.calibration['voice']['baseline_pause_frequency']
        baseline_duration = self.calibration['voice']['baseline_pause_duration']
        
        # Calculate current pause frequency
        pause_frequency = voice_results['total_pauses'] / 2  # per minute (2-min session)
        
        # Adjust based on deviation from baseline
        freq_deviation = (pause_frequency - baseline_freq) / max(baseline_freq, 1)
        duration_deviation = (voice_results['avg_pause_duration'] - baseline_duration) / max(baseline_duration, 0.1)
        
        # Apply adjustments
        freq_adjustment = freq_deviation * 25
        duration_adjustment = duration_deviation * 20
        
        calibrated_score = raw_score + freq_adjustment + duration_adjustment
        return max(0, min(100, calibrated_score))
    
    def get_confidence_multiplier(self, face_detection_rate, audio_quality=1.0):
        """Calculate confidence multiplier based on data quality"""
        # Face detection confidence
        face_confidence = min(1.0, face_detection_rate / 0.8)  # 80% is good
        
        # Overall confidence
        overall_confidence = (face_confidence + audio_quality) / 2
        
        # Return multiplier (0.5 to 1.0)
        return max(0.5, overall_confidence)
    
    def adaptive_threshold_adjustment(self, user_history):
        """Adjust thresholds based on user's historical performance"""
        if len(user_history) < 5:
            return 1.0  # No adjustment for new users
        
        # Calculate user's average anxiety level
        avg_anxiety = np.mean([session['overall_anxiety'] for session in user_history])
        
        # Adjust sensitivity based on user's typical range
        if avg_anxiety < 30:  # Low anxiety user
            return 1.2  # Increase sensitivity
        elif avg_anxiety > 70:  # High anxiety user
            return 0.8  # Decrease sensitivity
        else:
            return 1.0  # Normal sensitivity
    
    def update_from_session(self, visual_data, voice_results):
        """Update calibration from completed session"""
        self.update_visual_baseline(visual_data)
        self.update_voice_baseline(voice_results)
        self.calibration['sample_count'] += 1
        
        # Save every 5 sessions
        if self.calibration['sample_count'] % 5 == 0:
            self.save_calibration()
    
    def get_calibration_status(self):
        """Get current calibration status"""
        return {
            'is_calibrated': self.calibration['sample_count'] >= 3,
            'sample_count': self.calibration['sample_count'],
            'last_updated': self.calibration['last_updated'],
            'baselines': {
                'blink_rate': self.calibration['visual']['baseline_blink_rate'],
                'movement': self.calibration['visual']['baseline_movement'],
                'pause_frequency': self.calibration['voice']['baseline_pause_frequency'],
                'pause_duration': self.calibration['voice']['baseline_pause_duration']
            }
        }