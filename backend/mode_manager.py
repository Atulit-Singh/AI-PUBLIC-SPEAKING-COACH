import random
import json

class ModeManager:
    def __init__(self):
        self.modes = {
            'practice': {
                'name': 'Normal Practice',
                'description': 'Relaxed environment for skill building',
                'background': 'practice_room.jpg',
                'audio_effects': [],
                'jury_video': None,
                'crowd_noise': False,
                'difficulty_multiplier': 1.0
            },
            'interview': {
                'name': 'Mock Interview',
                'description': 'Professional interview simulation with jury panel',
                'background': 'interview_room.jpg',
                'audio_effects': ['office_ambience.mp3'],
                'jury_video': 'jury_panel.mp4',
                'crowd_noise': False,
                'difficulty_multiplier': 1.3
            },
            'public_speech': {
                'name': 'Public Speaking',
                'description': 'Auditorium environment with crowd distractions',
                'background': 'auditorium.jpg',
                'audio_effects': ['crowd_murmur.mp3', 'applause.mp3'],
                'jury_video': None,
                'crowd_noise': True,
                'difficulty_multiplier': 1.5
            }
        }
        
        self.interview_topics = [
            "Tell me about yourself and your background.",
            "What are your greatest strengths and weaknesses?",
            "Why do you want to work for our company?",
            "Describe a challenging situation you faced and how you handled it.",
            "Where do you see yourself in 5 years?",
            "Why should we hire you over other candidates?",
            "Tell me about a time you worked in a team.",
            "How do you handle stress and pressure?",
            "What motivates you in your work?",
            "Describe your leadership style."
        ]
        
        self.public_speech_topics = [
            "The importance of climate change action in our generation.",
            "How technology is reshaping the future of work.",
            "The role of education in building a better society.",
            "Why mental health awareness matters more than ever.",
            "The impact of social media on modern relationships.",
            "Innovation and entrepreneurship in the digital age.",
            "The power of diversity and inclusion in organizations.",
            "Sustainable living: small changes, big impact.",
            "The future of artificial intelligence and humanity.",
            "Building resilience in times of uncertainty."
        ]
        
        self.crowd_events = [
            {'time': 30, 'type': 'phone_ring', 'intensity': 'medium'},
            {'time': 45, 'type': 'cough', 'intensity': 'low'},
            {'time': 60, 'type': 'applause', 'intensity': 'high'},
            {'time': 75, 'type': 'murmur', 'intensity': 'medium'},
            {'time': 90, 'type': 'door_slam', 'intensity': 'high'},
            {'time': 105, 'type': 'whisper', 'intensity': 'low'}
        ]
    
    def get_mode_config(self, mode_type):
        return self.modes.get(mode_type, self.modes['practice'])
    
    def get_mode_topics(self, mode_type):
        if mode_type == 'interview':
            return random.choice(self.interview_topics)
        elif mode_type == 'public_speech':
            return random.choice(self.public_speech_topics)
        else:
            # Return normal practice topics (handled by topic_generator)
            return None
    
    def get_crowd_events(self, session_duration=120):
        """Get crowd distraction events for public speaking mode"""
        events = []
        for event in self.crowd_events:
            if event['time'] < session_duration:
                events.append({
                    'time': event['time'],
                    'type': event['type'],
                    'intensity': event['intensity'],
                    'audio_file': f"sounds/{event['type']}.mp3"
                })
        return events
    
    def get_jury_reactions(self):
        """Get jury reaction patterns for interview mode"""
        return [
            {'time': 20, 'reaction': 'nod_approval', 'juror': 1},
            {'time': 35, 'reaction': 'take_notes', 'juror': 2},
            {'time': 50, 'reaction': 'lean_forward', 'juror': 3},
            {'time': 65, 'reaction': 'slight_frown', 'juror': 1},
            {'time': 80, 'reaction': 'smile', 'juror': 2},
            {'time': 95, 'reaction': 'check_watch', 'juror': 3},
            {'time': 110, 'reaction': 'final_notes', 'juror': 1}
        ]
    
    def calculate_mode_anxiety_adjustment(self, base_score, mode_type):
        """Adjust anxiety score based on mode difficulty"""
        multiplier = self.modes[mode_type]['difficulty_multiplier']
        return min(100, base_score * multiplier)