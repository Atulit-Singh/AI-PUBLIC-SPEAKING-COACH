import json
import os
from datetime import datetime
import sqlite3
from pathlib import Path

class SessionTracker:
    def __init__(self, db_path="sessions.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for session tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                mode TEXT NOT NULL,
                topic TEXT NOT NULL,
                duration REAL NOT NULL,
                speech_duration REAL NOT NULL,
                overall_anxiety REAL NOT NULL,
                visual_anxiety REAL NOT NULL,
                voice_anxiety REAL NOT NULL,
                blink_rate REAL NOT NULL,
                movement_level REAL NOT NULL,
                face_detection_rate REAL NOT NULL,
                pause_count INTEGER NOT NULL,
                stutter_score REAL NOT NULL,
                fluency_score REAL NOT NULL,
                valid_session INTEGER NOT NULL,
                report_path TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_session(self, session_data, report_data, report_path):
        """Save session data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate speech duration (time with face detected)
        speech_duration = len([d for d in session_data['visual_indicators'] if d['face_detected']])
        valid_session = 1 if speech_duration >= 30 else 0  # Minimum 30 seconds
        
        cursor.execute('''
            INSERT INTO sessions (
                timestamp, mode, topic, duration, speech_duration,
                overall_anxiety, visual_anxiety, voice_anxiety,
                blink_rate, movement_level, face_detection_rate,
                pause_count, stutter_score, fluency_score,
                valid_session, report_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            session_data.get('current_mode', 'practice'),
            session_data.get('current_topic', ''),
            session_data['duration'],
            speech_duration,
            report_data['overall_anxiety_score'],
            report_data['visual_analysis']['anxiety_score'],
            report_data['voice_analysis']['anxiety_score'],
            report_data['visual_analysis']['blink_rate'],
            report_data['visual_analysis']['movement_level'],
            report_data['visual_analysis']['face_detection_rate'],
            report_data['voice_analysis']['total_pauses'],
            report_data['voice_analysis']['stutter_score'],
            report_data['voice_analysis']['fluency_score'],
            valid_session,
            report_path
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id, valid_session
    
    def get_progress_data(self, limit=10):
        """Get recent session progress data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM sessions 
            WHERE valid_session = 1 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        sessions = cursor.fetchall()
        conn.close()
        
        if not sessions:
            return None
        
        # Convert to list of dictionaries
        columns = [
            'id', 'timestamp', 'mode', 'topic', 'duration', 'speech_duration',
            'overall_anxiety', 'visual_anxiety', 'voice_anxiety',
            'blink_rate', 'movement_level', 'face_detection_rate',
            'pause_count', 'stutter_score', 'fluency_score',
            'valid_session', 'report_path'
        ]
        
        return [dict(zip(columns, session)) for session in sessions]
    
    def get_session_stats(self):
        """Get overall session statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total sessions
        cursor.execute('SELECT COUNT(*) FROM sessions')
        total_sessions = cursor.fetchone()[0]
        
        # Valid sessions
        cursor.execute('SELECT COUNT(*) FROM sessions WHERE valid_session = 1')
        valid_sessions = cursor.fetchone()[0]
        
        # Invalid sessions
        invalid_sessions = total_sessions - valid_sessions
        
        # Average anxiety scores (valid sessions only)
        cursor.execute('''
            SELECT AVG(overall_anxiety), AVG(visual_anxiety), AVG(voice_anxiety)
            FROM sessions WHERE valid_session = 1
        ''')
        avg_scores = cursor.fetchone()
        
        # Mode distribution
        cursor.execute('''
            SELECT mode, COUNT(*) FROM sessions 
            WHERE valid_session = 1 
            GROUP BY mode
        ''')
        mode_stats = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'valid_sessions': valid_sessions,
            'invalid_sessions': invalid_sessions,
            'avg_overall_anxiety': avg_scores[0] or 0,
            'avg_visual_anxiety': avg_scores[1] or 0,
            'avg_voice_anxiety': avg_scores[2] or 0,
            'mode_distribution': mode_stats
        }
    
    def check_improvement_trend(self):
        """Check if user is improving over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT overall_anxiety FROM sessions 
            WHERE valid_session = 1 
            ORDER BY timestamp DESC 
            LIMIT 5
        ''')
        
        recent_scores = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if len(recent_scores) < 3:
            return "insufficient_data"
        
        # Simple trend analysis
        first_half = sum(recent_scores[:len(recent_scores)//2]) / (len(recent_scores)//2)
        second_half = sum(recent_scores[len(recent_scores)//2:]) / (len(recent_scores) - len(recent_scores)//2)
        
        if first_half - second_half > 5:  # Anxiety decreased by 5+ points
            return "improving"
        elif second_half - first_half > 5:  # Anxiety increased by 5+ points
            return "declining"
        else:
            return "stable"