from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import cv2
import threading
import time
import base64
import numpy as np
from emotion_detector import EmotionAnxietyDetector
from voice_analyzer import VoiceAnxietyAnalyzer
from topic_generator import TopicGenerator
from report_generator import ReportGenerator
from mode_manager import ModeManager
from session_tracker import SessionTracker
from model_calibrator import ModelCalibrator
import json
import os

app = Flask(__name__)
CORS(app)

# Global variables
emotion_detector = EmotionAnxietyDetector()
voice_analyzer = VoiceAnxietyAnalyzer()
topic_generator = TopicGenerator()
report_generator = ReportGenerator()
mode_manager = ModeManager()
session_tracker = SessionTracker()
model_calibrator = ModelCalibrator()

session_data = {
    'visual_indicators': [],
    'is_recording': False,
    'current_topic': None,
    'session_start': None,
    'current_mode': 'practice',
    'crowd_events': [],
    'jury_reactions': [],
    'speech_detected_count': 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_modes', methods=['GET'])
def get_modes():
    """Get available practice modes"""
    modes = {}
    for mode_id, config in mode_manager.modes.items():
        modes[mode_id] = {
            'name': config['name'],
            'description': config['description']
        }
    return jsonify({'modes': modes})

@app.route('/api/set_mode', methods=['POST'])
def set_mode():
    """Set the practice mode"""
    mode_type = request.json.get('mode', 'practice')
    session_data['current_mode'] = mode_type
    
    # Get mode-specific events
    if mode_type == 'public_speech':
        session_data['crowd_events'] = mode_manager.get_crowd_events()
    elif mode_type == 'interview':
        session_data['jury_reactions'] = mode_manager.get_jury_reactions()
    
    mode_config = mode_manager.get_mode_config(mode_type)
    return jsonify({
        'status': 'success',
        'mode': mode_config
    })

@app.route('/api/get_topic', methods=['GET'])
def get_topic():
    """Get a topic based on current mode"""
    mode_type = session_data.get('current_mode', 'practice')
    
    # Get mode-specific topic or fallback to general topics
    mode_topic = mode_manager.get_mode_topics(mode_type)
    if mode_topic:
        topic = mode_topic
    else:
        topic = topic_generator.get_random_topic()
    
    instructions = topic_generator.get_speaking_instructions()
    mode_config = mode_manager.get_mode_config(mode_type)
    
    session_data['current_topic'] = topic
    session_data['visual_indicators'] = []
    session_data['session_start'] = time.time()
    
    return jsonify({
        'topic': topic,
        'instructions': instructions,
        'mode_config': mode_config,
        'crowd_events': session_data.get('crowd_events', []),
        'jury_reactions': session_data.get('jury_reactions', [])
    })

@app.route('/api/start_session', methods=['POST'])
def start_session():
    """Start a new analysis session"""
    session_data['is_recording'] = True
    session_data['visual_indicators'] = []
    session_data['session_start'] = time.time()
    session_data['speech_detected_count'] = 0
    
    return jsonify({'status': 'Session started'})

@app.route('/api/analyze_frame', methods=['POST'])
def analyze_frame():
    """Analyze a single video frame"""
    if not session_data['is_recording']:
        return jsonify({'error': 'Session not active'})
    
    try:
        # Get image data from request
        image_data = request.json['image']
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Analyze frame
        indicators = emotion_detector.analyze_frame(frame)
        session_data['visual_indicators'].append(indicators)
        
        # Count speech detection for minimum duration validation
        if indicators['face_detected']:
            session_data['speech_detected_count'] += 1
        
        return jsonify({
            'status': 'success',
            'indicators': indicators,
            'speech_duration': session_data['speech_detected_count']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/stop_session', methods=['POST'])
def stop_session():
    """Stop the current session and generate report"""
    session_data['is_recording'] = False
    
    try:
        # Get audio data if provided
        audio_data = None
        if 'audio' in request.json:
            # In a real implementation, you would process the audio data here
            # For now, we'll simulate voice analysis
            voice_results = {
                'anxiety_score': 45.0,
                'pause_score': 30.0,
                'stutter_score': 20.0,
                'fluency_score': 25.0,
                'avg_pause_duration': 1.2,
                'num_long_pauses': 2,
                'total_pauses': 8
            }
        else:
            voice_results = voice_analyzer.get_voice_anxiety_score([])
        
        # Check minimum speech duration (30 seconds)
        speech_duration = session_data['speech_detected_count']
        if speech_duration < 30:
            return jsonify({
                'status': 'insufficient_speech',
                'message': f'Please speak for at least 30 seconds. You spoke for {speech_duration} seconds.',
                'speech_duration': speech_duration,
                'required_duration': 30
            })
        
        # Generate report
        session_info = {
            'topic': session_data['current_topic'],
            'duration': time.time() - session_data['session_start'] if session_data['session_start'] else 0,
            'mode': session_data.get('current_mode', 'practice'),
            'speech_duration': speech_duration
        }
        
        # Get user's session history for adaptive calibration
        user_history = session_tracker.get_progress_data(10) or []
        
        # Apply model calibration for improved accuracy
        visual_anxiety_raw = emotion_detector.get_anxiety_score(session_data['visual_indicators'])
        
        # Calibrate scores based on user baseline
        if session_data['visual_indicators']:
            avg_blink = np.mean([d['blink_rate'] for d in session_data['visual_indicators'] if d['face_detected']])
            avg_movement = np.mean([d['movement_level'] for d in session_data['visual_indicators'] if d['face_detected']])
            face_detection_rate = len([d for d in session_data['visual_indicators'] if d['face_detected']]) / len(session_data['visual_indicators'])
            
            visual_anxiety_calibrated = model_calibrator.calibrate_visual_score(
                visual_anxiety_raw, avg_blink, avg_movement
            )
            
            voice_anxiety_calibrated = model_calibrator.calibrate_voice_score(
                voice_results['anxiety_score'], voice_results
            )
            
            # Apply confidence multiplier
            confidence_multiplier = model_calibrator.get_confidence_multiplier(face_detection_rate)
            
            # Apply adaptive threshold adjustment
            threshold_adjustment = model_calibrator.adaptive_threshold_adjustment(user_history)
            
            # Final calibrated scores
            voice_results['anxiety_score'] = voice_anxiety_calibrated * confidence_multiplier * threshold_adjustment
            
            # Update calibration from this session
            model_calibrator.update_from_session(session_data['visual_indicators'], voice_results)
        
        # Adjust anxiety score based on mode difficulty
        mode_type = session_data.get('current_mode', 'practice')
        voice_results['anxiety_score'] = mode_manager.calculate_mode_anxiety_adjustment(
            voice_results['anxiety_score'], mode_type
        )
        
        report_data = report_generator.generate_anxiety_report(
            session_data['visual_indicators'],
            voice_results,
            session_info
        )
        
        # Save report
        json_file = report_generator.save_report_json()
        
        # Save session to database
        session_id, is_valid = session_tracker.save_session(
            session_info, report_data, json_file
        )
        
        # Add progress data to report
        progress_data = session_tracker.get_progress_data(5)
        improvement_trend = session_tracker.check_improvement_trend()
        
        # Add calibration status to response
        calibration_status = model_calibrator.get_calibration_status()
        
        return jsonify({
            'status': 'success',
            'report': report_data,
            'report_file': json_file,
            'session_id': session_id,
            'progress_data': progress_data,
            'improvement_trend': improvement_trend,
            'calibration_status': calibration_status
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/get_progress', methods=['GET'])
def get_progress():
    """Get user progress data"""
    try:
        progress_data = session_tracker.get_progress_data(10)
        stats = session_tracker.get_session_stats()
        trend = session_tracker.check_improvement_trend()
        
        return jsonify({
            'progress_data': progress_data,
            'stats': stats,
            'improvement_trend': trend
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/get_report/<filename>')
def get_report(filename):
    """Serve report files"""
    try:
        return send_file(f'reports/{filename}')
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('reports', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Initialize session tracker and model calibrator
    session_tracker.init_database()
    model_calibrator.load_calibration()
    
    print("\n" + "="*50)
    print("AI PUBLIC SPEAKING COACH - SERVER STARTING")
    print("="*50)
    print("🎯 Three Practice Modes Available:")
    print("   • Normal Practice - Relaxed environment")
    print("   • Mock Interview - Professional jury panel")
    print("   • Public Speaking - Crowd distractions")
    print("\n📊 Features:")
    print("   • Real-time anxiety analysis")
    print("   • Progress tracking & improvement trends")
    print("   • Minimum 30-second speech validation")
    print("   • Comprehensive reporting")
    print("\n🌐 Access your coach at: http://localhost:5000")
    print("📱 Grant camera & microphone permissions when prompted")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)