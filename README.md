# AI Public Speaking Coach

An AI-powered application that helps improve public speaking skills by analyzing visual and vocal anxiety indicators in real-time.

## Features

### Visual Analysis
- **Blink Rate Detection**: Monitors excessive blinking as an anxiety indicator
- **Movement Tracking**: Detects head movement and fidgeting
- **Face Detection**: Real-time face tracking using MediaPipe
- **Live Metrics**: Real-time display of anxiety indicators

### Voice Analysis
- **Pause Detection**: Identifies long pauses and hesitations
- **Stuttering Analysis**: Detects repetitive speech patterns
- **Fluency Assessment**: Measures speech rate and continuity
- **Audio Recording**: Captures 2-minute speech samples

### Interactive Features
- **Random Topic Generator**: 30+ diverse speaking topics
- **2-minute Timer**: Structured speaking sessions
- **Real-time Feedback**: Live anxiety metrics during recording
- **Comprehensive Reports**: Detailed analysis with visualizations

### Report Generation
- **Anxiety Scoring**: Overall, visual, and voice anxiety scores
- **Interactive Charts**: Matplotlib-generated visualizations
- **Personalized Recommendations**: Immediate tips, practice exercises, and long-term strategies
- **Progress Tracking**: JSON reports for historical analysis

## Technology Stack

### Backend
- **Python Flask**: Web framework and API
- **OpenCV**: Computer vision and camera handling
- **MediaPipe**: Face mesh detection and landmark tracking
- **Librosa**: Audio processing and analysis
- **Matplotlib/Seaborn**: Data visualization
- **NumPy/Pandas**: Data processing

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Real-time camera and audio handling
- **Bootstrap 5**: UI framework
- **Font Awesome**: Icons and visual elements

## 🚀 Quick Start

### Automated Setup (Windows):
```bash
run.bat
```

### Manual Setup (All Platforms):
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup media files (optional)
python setup_media.py

# 3. Start application
cd backend && python app.py
```

### Access Your Coach:
**URL**: `http://localhost:5000`
**Requirements**: Camera & microphone permissions

📖 **Detailed Guide**: See [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)

## 🎯 How to Use

1. **Select Mode**: Choose your practice environment
2. **Get Topic**: Receive mode-specific speaking prompts  
3. **Start Session**: Begin recording (30-second minimum)
4. **Speak Naturally**: Address topic while system analyzes
5. **View Results**: Get detailed anxiety analysis & recommendations
6. **Track Progress**: Monitor improvement over time

### ⚠️ Session Requirements:
- **Minimum 30 seconds** of speech required
- **Face must be visible** for visual analysis
- **Invalid sessions** prompt automatic re-recording
- **Progress tracking** saves all valid sessions

## 🎭 Three Immersive Practice Modes

### 🧘 Normal Practice Mode
- **Environment**: Clean, distraction-free interface
- **Topics**: General conversation topics
- **Difficulty**: Standard anxiety scoring
- **Best For**: Building basic confidence and skills

### 👔 Mock Interview Mode
- **Environment**: Professional interview setting
- **Visual**: Video overlay of 3 judges panel
- **Topics**: Interview questions ("Tell me about yourself", etc.)
- **Features**: 
  - Realistic jury reactions (nodding, note-taking, expressions)
  - Professional office ambience sounds
  - Interactive judge responses based on timing
- **Difficulty**: 30% higher anxiety sensitivity
- **Best For**: Job interview preparation

### 🎤 Public Speaking Mode  
- **Environment**: Auditorium with crowd simulation
- **Visual**: Audience seats with stage lighting effects
- **Topics**: Public speaking themes (climate change, technology, etc.)
- **Features**:
  - Continuous crowd murmuring background
  - Timed distractions: phone rings (30s), coughs (45s), applause (60s), door slams (90s)
  - Real-time distraction indicators
  - Dynamic noise level alerts
- **Difficulty**: 50% higher anxiety sensitivity  
- **Best For**: Conference presentations, public talks

## 📊 Progress Tracking & Session Management

### Automatic Session Recording:
- **SQLite Database**: Stores all session data permanently
- **Valid Sessions**: 30+ seconds of detected speech
- **Invalid Sessions**: Automatic re-recording prompts
- **Progress Metrics**: Anxiety trends, improvement tracking

### Session Validation:
- **Minimum Duration**: 30 seconds of active speech required
- **Face Detection**: Must be visible for visual analysis
- **Re-recording**: Automatic prompt for insufficient sessions
- **Quality Control**: Ensures meaningful data collection

### Progress Dashboard:
- **Session Statistics**: Total, valid, and incomplete sessions
- **Improvement Trends**: Improving, stable, or declining indicators
- **Mode Distribution**: Practice preferences across different modes
- **Historical Data**: Recent session details with timestamps
- **Anxiety Tracking**: Average scores and progress over time

## System Requirements

- **Camera**: Webcam for visual analysis
- **Microphone**: Audio input for voice analysis
- **Browser**: Modern browser with WebRTC support (Chrome, Firefox, Safari)
- **Python**: 3.7+ with required packages

## Anxiety Indicators Analyzed

### Visual Indicators
- Blink rate (normal: 15-20 blinks/minute)
- Head movement and stability
- Face detection consistency

### Voice Indicators
- Pause frequency and duration
- Speech stuttering patterns
- Overall fluency and speech rate

## Scoring System

- **0-30**: Low anxiety level
- **30-60**: Moderate anxiety level  
- **60-100**: High anxiety level

## Media Files Setup

The application requires audio and video files for full immersive experience:

### Quick Setup:
```bash
python setup_media.py
```

### Manual Setup:
1. **Audio Files** (place in `backend/static/sounds/`):
   - `crowd_murmur.mp3` - Background crowd noise
   - `applause.mp3` - Audience applause
   - `phone_ring.mp3` - Phone distraction
   - `cough.mp3` - Audience cough
   - `door_slam.mp3` - Door slam sound

2. **Video Files** (place in `backend/static/videos/`):
   - `jury_panel.mp4` - Video of 3 judges for interview mode

### Free Media Sources:
- **Audio**: freesound.org, zapsplat.com, YouTube Audio Library
- **Video**: pexels.com, pixabay.com, videvo.net

**Note**: Application works without media files but with reduced immersion.

### Session Database:
All sessions are automatically saved to `sessions.db` with:
- Session metadata (timestamp, mode, topic, duration)
- Anxiety analysis results (overall, visual, voice scores)
- Performance metrics (blink rate, movement, pauses, fluency)
- Validation status (valid/invalid based on 30-second minimum)
- Progress tracking data for improvement analysis

## Suggested Modifications for Enhanced Effectiveness

### 1. Advanced AI Integration
```python
# Add emotion recognition
from tensorflow import keras
emotion_model = keras.models.load_model('emotion_model.h5')

# Implement sentiment analysis
from transformers import pipeline
sentiment_analyzer = pipeline('sentiment-analysis')
```

### 2. Gamification Features
- **Progress Badges**: Achievement system for improvement milestones
- **Leaderboards**: Compare progress with other users
- **Challenges**: Weekly speaking challenges with specific focus areas
- **Streak Tracking**: Consecutive practice day counters

### 3. Enhanced Interactivity
```javascript
// Add real-time coaching prompts
class RealTimeCoach {
    provideLiveFeedback(anxietyLevel) {
        if (anxietyLevel > 70) {
            this.showPrompt("Take a deep breath and slow down");
        }
    }
}

// Implement gesture recognition
class GestureAnalyzer {
    analyzeHandMovements(landmarks) {
        // Detect excessive hand gestures
        // Provide gesture improvement suggestions
    }
}
```

### 4. Personalization Engine
- **Learning Algorithms**: Adapt recommendations based on user progress
- **Custom Topics**: Allow users to add industry-specific topics
- **Difficulty Levels**: Beginner, intermediate, advanced speaking challenges
- **Personal Goals**: Set and track specific improvement targets

### 5. Social Features
- **Peer Review**: Allow users to review each other's sessions
- **Group Sessions**: Virtual speaking clubs and practice groups
- **Mentor Matching**: Connect with experienced speakers
- **Community Challenges**: Group speaking events and competitions

### 6. Advanced Analytics
```python
# Implement trend analysis
class ProgressAnalyzer:
    def analyze_improvement_trends(self, user_sessions):
        # Track anxiety reduction over time
        # Identify improvement patterns
        # Predict future performance
        pass

# Add comparative analysis
class BenchmarkAnalyzer:
    def compare_with_peers(self, user_data, demographic_data):
        # Compare with similar users
        # Provide percentile rankings
        pass
```

### 7. Mobile Integration
- **Progressive Web App**: Mobile-responsive design
- **Push Notifications**: Practice reminders and encouragement
- **Offline Mode**: Practice without internet connection
- **Voice-only Mode**: Audio-only practice sessions

### 8. Professional Features
- **Industry Templates**: Business presentations, academic talks, sales pitches
- **Time Variations**: 30-second elevator pitches to 10-minute presentations
- **Audience Simulation**: Different audience types and reactions
- **Presentation Tools**: Slide integration and timing analysis

### 9. Accessibility Enhancements
- **Multi-language Support**: Topics and feedback in multiple languages
- **Hearing Impaired**: Visual-only analysis mode
- **Motor Impaired**: Alternative input methods
- **Screen Reader**: Full accessibility compliance

### 10. Integration Capabilities
```python
# Calendar integration
class CalendarIntegration:
    def schedule_practice_sessions(self):
        # Integrate with Google Calendar, Outlook
        pass

# Video conferencing integration
class MeetingIntegration:
    def analyze_real_meetings(self):
        # Zoom, Teams integration for real-world analysis
        pass
```

## 📁 File Structure
```
AI_PUBLIC_SPEAKING_COACH/
├── backend/
│   ├── app.py                 # Flask application & API
│   ├── emotion_detector.py    # Visual analysis (OpenCV/MediaPipe)
│   ├── voice_analyzer.py      # Audio analysis (Librosa)
│   ├── topic_generator.py     # Topic generation
│   ├── report_generator.py    # Report & visualization creation
│   ├── mode_manager.py        # Practice mode configurations
│   ├── session_tracker.py     # Progress tracking & database
│   ├── templates/index.html   # Main web interface
│   └── static/
│       ├── script.js          # Frontend JavaScript
│       ├── sounds/            # Audio effects (optional)
│       └── videos/            # Jury panel video (optional)
├── reports/                   # Generated analysis reports
├── sessions.db               # SQLite progress database
├── setup_media.py            # Media file setup script
├── run.bat                   # Windows quick start
├── QUICK_START_GUIDE.md      # Detailed usage guide
└── requirements.txt          # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your enhancement
4. Add tests and documentation
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

## Future Roadmap

- [ ] Machine learning model training for better accuracy
- [ ] Real-time emotion recognition
- [ ] Multi-user session support
- [ ] Advanced reporting dashboard
- [ ] Mobile application development
- [ ] Integration with popular presentation tools