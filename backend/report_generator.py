import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class ReportGenerator:
    def __init__(self):
        self.report_data = {}
        
    def generate_anxiety_report(self, visual_data, voice_data, session_info):
        """Generate comprehensive anxiety analysis report"""
        
        # Calculate overall scores
        visual_anxiety = self._calculate_visual_anxiety(visual_data)
        voice_anxiety = voice_data['anxiety_score']
        overall_anxiety = (visual_anxiety + voice_anxiety) / 2
        
        # Generate report data
        self.report_data = {
            'session_info': session_info,
            'timestamp': datetime.now().isoformat(),
            'overall_anxiety_score': overall_anxiety,
            'visual_analysis': {
                'anxiety_score': visual_anxiety,
                'blink_rate': np.mean([d['blink_rate'] for d in visual_data if d['face_detected']]),
                'movement_level': np.mean([d['movement_level'] for d in visual_data if d['face_detected']]),
                'face_detection_rate': len([d for d in visual_data if d['face_detected']]) / len(visual_data) * 100
            },
            'voice_analysis': voice_data,
            'recommendations': self._generate_recommendations(overall_anxiety, visual_anxiety, voice_anxiety)
        }
        
        # Generate visualizations
        self._create_visualizations(visual_data, voice_data)
        
        return self.report_data
    
    def _calculate_visual_anxiety(self, visual_data):
        """Calculate anxiety score from visual indicators"""
        if not visual_data:
            return 0
        
        face_detected_data = [d for d in visual_data if d['face_detected']]
        if not face_detected_data:
            return 0
        
        avg_blink_rate = np.mean([d['blink_rate'] for d in face_detected_data])
        avg_movement = np.mean([d['movement_level'] for d in face_detected_data])
        
        # Normal blink rate: 15-20 per minute
        blink_score = max(0, min(100, (avg_blink_rate - 15) * 5))
        movement_score = min(100, avg_movement * 1000)
        
        return (blink_score + movement_score) / 2
    
    def _create_visualizations(self, visual_data, voice_data):
        """Create visualization charts"""
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('AI Public Speaking Coach - Anxiety Analysis Report', fontsize=16, fontweight='bold')
        
        # 1. Anxiety Scores Comparison
        categories = ['Visual\nAnxiety', 'Voice\nAnxiety', 'Overall\nAnxiety']
        scores = [
            self.report_data['visual_analysis']['anxiety_score'],
            self.report_data['voice_analysis']['anxiety_score'],
            self.report_data['overall_anxiety_score']
        ]
        
        colors = ['#ff6b6b' if score > 70 else '#feca57' if score > 40 else '#48dbfb' for score in scores]
        bars = axes[0, 0].bar(categories, scores, color=colors, alpha=0.8)
        axes[0, 0].set_title('Anxiety Scores Overview', fontweight='bold')
        axes[0, 0].set_ylabel('Anxiety Score (0-100)')
        axes[0, 0].set_ylim(0, 100)
        
        # Add value labels on bars
        for bar, score in zip(bars, scores):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 2. Blink Rate Over Time
        face_detected_data = [d for d in visual_data if d['face_detected']]
        if face_detected_data:
            timestamps = [d['timestamp'] for d in face_detected_data]
            blink_rates = [d['blink_rate'] for d in face_detected_data]
            
            axes[0, 1].plot(timestamps, blink_rates, color='#ff6b6b', linewidth=2, marker='o', markersize=4)
            axes[0, 1].axhline(y=20, color='orange', linestyle='--', alpha=0.7, label='Normal Range')
            axes[0, 1].axhline(y=15, color='orange', linestyle='--', alpha=0.7)
            axes[0, 1].fill_between([min(timestamps), max(timestamps)], 15, 20, alpha=0.2, color='green')
            axes[0, 1].set_title('Blink Rate Over Time', fontweight='bold')
            axes[0, 1].set_xlabel('Time (seconds)')
            axes[0, 1].set_ylabel('Blinks per minute')
            axes[0, 1].legend()
        
        # 3. Voice Analysis Breakdown
        voice_metrics = ['Pause\nScore', 'Stutter\nScore', 'Fluency\nScore']
        voice_scores = [
            voice_data['pause_score'],
            voice_data['stutter_score'],
            voice_data['fluency_score']
        ]
        
        colors_voice = ['#ff6b6b' if score > 50 else '#feca57' if score > 25 else '#48dbfb' for score in voice_scores]
        bars_voice = axes[1, 0].bar(voice_metrics, voice_scores, color=colors_voice, alpha=0.8)
        axes[1, 0].set_title('Voice Analysis Breakdown', fontweight='bold')
        axes[1, 0].set_ylabel('Score (0-100)')
        axes[1, 0].set_ylim(0, 100)
        
        for bar, score in zip(bars_voice, voice_scores):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                           f'{score:.1f}', ha='center', va='bottom', fontweight='bold')
        
        # 4. Improvement Areas Radar Chart
        categories_radar = ['Blink Rate', 'Movement', 'Pauses', 'Stuttering', 'Fluency']
        values = [
            min(100, max(0, (self.report_data['visual_analysis']['blink_rate'] - 15) * 5)),
            min(100, self.report_data['visual_analysis']['movement_level'] * 1000),
            voice_data['pause_score'],
            voice_data['stutter_score'],
            voice_data['fluency_score']
        ]
        
        # Normalize to 0-100 scale and invert so lower is better
        values_normalized = [100 - v for v in values]
        
        angles = np.linspace(0, 2 * np.pi, len(categories_radar), endpoint=False).tolist()
        values_normalized += values_normalized[:1]  # Complete the circle
        angles += angles[:1]
        
        axes[1, 1].remove()
        ax_radar = fig.add_subplot(224, projection='polar')
        ax_radar.plot(angles, values_normalized, 'o-', linewidth=2, color='#48dbfb')
        ax_radar.fill(angles, values_normalized, alpha=0.25, color='#48dbfb')
        ax_radar.set_xticks(angles[:-1])
        ax_radar.set_xticklabels(categories_radar)
        ax_radar.set_ylim(0, 100)
        ax_radar.set_title('Performance Areas\n(Higher = Better)', fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Save the plot
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'reports/anxiety_report_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return f'reports/anxiety_report_{timestamp}.png'
    
    def _generate_recommendations(self, overall_anxiety, visual_anxiety, voice_anxiety):
        """Generate personalized recommendations"""
        recommendations = {
            'immediate_tips': [],
            'practice_exercises': [],
            'long_term_strategies': []
        }
        
        # Immediate tips based on anxiety level
        if overall_anxiety > 70:
            recommendations['immediate_tips'].extend([
                "Practice deep breathing exercises before speaking",
                "Use the 4-7-8 breathing technique to calm nerves",
                "Focus on one friendly face in the audience"
            ])
        elif overall_anxiety > 40:
            recommendations['immediate_tips'].extend([
                "Take a moment to pause and collect your thoughts",
                "Use positive self-talk before presentations",
                "Practice power poses to boost confidence"
            ])
        else:
            recommendations['immediate_tips'].extend([
                "Continue your current preparation methods",
                "Focus on engaging with your audience",
                "Use gestures to enhance your message"
            ])
        
        # Visual anxiety specific recommendations
        if visual_anxiety > 50:
            recommendations['practice_exercises'].extend([
                "Practice maintaining steady eye contact with the camera",
                "Record yourself speaking to become comfortable with being watched",
                "Practice relaxation techniques to reduce physical tension"
            ])
        
        # Voice anxiety specific recommendations
        if voice_anxiety > 50:
            recommendations['practice_exercises'].extend([
                "Practice speaking slowly and deliberately",
                "Record yourself reading aloud to improve fluency",
                "Use tongue twisters to improve articulation"
            ])
        
        # Long-term strategies
        recommendations['long_term_strategies'] = [
            "Join a public speaking group like Toastmasters",
            "Practice speaking on various topics regularly",
            "Work on building confidence through small speaking opportunities",
            "Consider professional coaching if anxiety persists",
            "Practice mindfulness and stress management techniques"
        ]
        
        return recommendations
    
    def save_report_json(self):
        """Save report data as JSON"""
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'reports/report_data_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.report_data, f, indent=2, default=str)
        
        return filename