import random

class TopicGenerator:
    def __init__(self):
        self.topics = [
            "Describe your ideal vacation destination and why you would want to visit there.",
            "If you could have dinner with any historical figure, who would it be and what would you discuss?",
            "Explain the importance of environmental conservation in today's world.",
            "Describe a skill you would like to learn and how it would benefit your life.",
            "If you could solve one global problem, what would it be and how would you approach it?",
            "Discuss the role of technology in modern education.",
            "Describe your favorite childhood memory and why it's special to you.",
            "If you could start your own business, what would it be and why?",
            "Explain the importance of mental health awareness in society.",
            "Describe a book or movie that changed your perspective on life.",
            "Discuss the benefits and challenges of remote work.",
            "If you could live in any time period, when would it be and why?",
            "Explain the importance of cultural diversity in communities.",
            "Describe a personal challenge you overcame and what you learned from it.",
            "Discuss the impact of social media on modern relationships.",
            "If you could have any superpower, what would it be and how would you use it?",
            "Explain the importance of lifelong learning in career development.",
            "Describe your vision for the future of transportation.",
            "Discuss the role of art and creativity in society.",
            "If you could change one thing about your city, what would it be and why?",
            "Explain the importance of work-life balance.",
            "Describe a tradition from your culture that you value.",
            "Discuss the benefits of volunteering and community service.",
            "If you could master any language instantly, which would you choose and why?",
            "Explain the importance of financial literacy for young adults.",
            "Describe your ideal home and what makes it special.",
            "Discuss the impact of artificial intelligence on future jobs.",
            "If you could witness any historical event, what would it be and why?",
            "Explain the importance of physical fitness and healthy living.",
            "Describe a person who has been a positive influence in your life."
        ]
        
        self.used_topics = set()
    
    def get_random_topic(self):
        """Get a random topic that hasn't been used recently"""
        available_topics = [t for t in self.topics if t not in self.used_topics]
        
        if not available_topics:
            self.used_topics.clear()  # Reset if all topics used
            available_topics = self.topics
        
        topic = random.choice(available_topics)
        self.used_topics.add(topic)
        
        return topic
    
    def get_speaking_instructions(self):
        """Get instructions for the speaking exercise"""
        return {
            'duration': 120,  # 2 minutes
            'instructions': [
                "Speak clearly and at a comfortable pace",
                "Try to maintain eye contact with the camera",
                "Use gestures naturally to support your speech",
                "Take deep breaths if you feel nervous",
                "It's okay to pause and think - don't rush",
                "Speak from your personal experience when possible"
            ],
            'tips': [
                "Structure your response with a beginning, middle, and end",
                "Use specific examples to illustrate your points",
                "Don't worry about being perfect - focus on communicating your ideas",
                "If you lose your train of thought, take a moment to refocus"
            ]
        }