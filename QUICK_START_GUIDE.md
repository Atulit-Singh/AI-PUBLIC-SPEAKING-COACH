# 🚀 AI Public Speaking Coach - Quick Start Guide

## 📋 Prerequisites
- **Python 3.7+** installed on your system
- **Webcam** for visual analysis
- **Microphone** for voice analysis
- **Modern web browser** (Chrome, Firefox, Safari, Edge)

## ⚡ Quick Installation & Launch

### Option 1: Automated Setup (Windows)
```bash
# 1. Download/clone the project
git clone <repository-url>
cd AI_PUBLIC_SPEAKING_COACH

# 2. Run the automated setup
run.bat
```

### Option 2: Manual Setup (All Platforms)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup media files (optional)
python setup_media.py

# 3. Start the application
cd backend
python app.py
```

### Option 3: One-Command Launch
```bash
# Install and run in one go
pip install -r requirements.txt && cd backend && python app.py
```

## 🌐 Access Your Coach

1. **Open your browser** and go to: `http://localhost:5000`
2. **Grant permissions** when prompted for camera and microphone access
3. **Start practicing!** 🎯

## 🎯 How to Use

### Step 1: Select Your Mode
Choose from three practice environments:
- **🧘 Normal Practice** - Relaxed, distraction-free
- **👔 Mock Interview** - Professional jury panel simulation  
- **🎤 Public Speaking** - Auditorium with crowd distractions

### Step 2: Get Your Topic
- Click **"Get New Topic"** for a mode-specific speaking prompt
- Read the instructions and tips provided

### Step 3: Start Your Session
- Click **"Start Session"** to begin recording
- **Speak for at least 30 seconds** (minimum requirement)
- Watch live metrics: face detection, blink rate, movement, speech duration

### Step 4: Complete & Analyze
- Session auto-stops after 2 minutes or click **"Stop & Analyze"**
- View your comprehensive anxiety analysis report
- Get personalized improvement recommendations

### Step 5: Track Progress
- Click **"View Progress"** to see your improvement over time
- Monitor session statistics and trends
- Compare performance across different modes

## 📊 Understanding Your Results

### Anxiety Levels:
- **🟢 0-30**: Low anxiety (Great job!)
- **🟡 30-60**: Moderate anxiety (Room for improvement)
- **🔴 60-100**: High anxiety (Focus on relaxation techniques)

### Key Metrics:
- **Blink Rate**: Normal is 15-20 per minute
- **Movement Level**: Measures head stability
- **Speech Duration**: Must be 30+ seconds for valid analysis
- **Face Detection Rate**: Percentage of time face was visible

## 🎮 Mode-Specific Features

### Mock Interview Mode 👔
- **Jury Panel Video**: 3 professional judges in corner overlay
- **Interactive Reactions**: Judges nod, take notes, show expressions
- **Interview Topics**: "Tell me about yourself", "Why hire you?", etc.
- **Difficulty**: 30% higher anxiety sensitivity

### Public Speaking Mode 🎤
- **Crowd Simulation**: Visual audience with stage lighting
- **Timed Distractions**: Phone rings, coughs, applause, door slams
- **Background Noise**: Continuous crowd murmuring
- **Difficulty**: 50% higher anxiety sensitivity

## 🔧 Troubleshooting

### Camera/Microphone Issues:
1. **Check browser permissions** - Allow camera and microphone access
2. **Try different browser** - Chrome works best
3. **Check device connections** - Ensure camera/mic are connected
4. **Restart browser** - Close and reopen the browser

### "Insufficient Speech" Error:
- **Speak longer**: Minimum 30 seconds required
- **Stay visible**: Keep your face in camera view
- **Speak clearly**: Address the topic directly
- **Check face detection**: Green "Detected" badge should show

### No Audio/Video Effects:
- **Media files missing**: Run `python setup_media.py`
- **Download audio/video**: See `backend/static/sounds/README.md`
- **Application works without media** - Visual effects still function

### Performance Issues:
- **Close other applications** - Free up system resources
- **Use wired internet** - For better stability
- **Lower video quality** - If browser struggles

## 📁 Project Structure
```
AI_PUBLIC_SPEAKING_COACH/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── static/
│   │   ├── sounds/         # Audio effects (optional)
│   │   └── videos/         # Jury panel video (optional)
│   └── templates/
├── reports/                # Generated analysis reports
├── sessions.db            # Progress tracking database
├── requirements.txt       # Python dependencies
└── run.bat               # Windows quick start
```

## 🎯 Tips for Best Results

### Before Starting:
- **Good lighting** - Ensure your face is well-lit
- **Stable camera** - Position camera at eye level
- **Quiet environment** - Minimize background noise
- **Comfortable position** - Sit or stand naturally

### During Session:
- **Look at camera** - Maintain "eye contact" with lens
- **Speak naturally** - Don't rush or overthink
- **Use gestures** - Natural hand movements are good
- **Stay in frame** - Keep your face visible throughout

### For Better Analysis:
- **Complete full 2 minutes** - Longer sessions = better data
- **Try different modes** - Each offers unique challenges
- **Practice regularly** - Consistency improves results
- **Review recommendations** - Apply suggested improvements

## 📈 Progress Tracking Features

### Session History:
- **All sessions saved** automatically to database
- **Valid vs Invalid** sessions tracked separately
- **Mode distribution** shows your practice preferences
- **Improvement trends** calculated over time

### Progress Indicators:
- **🟢 Improving**: Anxiety scores decreasing over time
- **🟡 Stable**: Consistent performance levels
- **🔴 Declining**: May need to focus on specific areas

### Statistics Dashboard:
- **Total sessions** completed
- **Average anxiety scores** across all modes
- **Recent session details** with timestamps
- **Mode-specific performance** comparisons

## 🆘 Getting Help

### Common Questions:
1. **Q: Why do I need 30 seconds minimum?**
   A: Shorter sessions don't provide enough data for meaningful analysis

2. **Q: Can I use without camera?**
   A: Camera is required for visual anxiety analysis (blink rate, movement)

3. **Q: Do I need the audio/video files?**
   A: No, but they enhance the immersive experience significantly

4. **Q: How accurate is the anxiety detection?**
   A: Results are indicative trends, not medical diagnoses

### Support Resources:
- **Check README.md** - Comprehensive documentation
- **Review error messages** - Usually provide clear guidance
- **Try different browsers** - Chrome recommended
- **Restart application** - Often resolves temporary issues

## 🎉 Ready to Start!

Your AI Public Speaking Coach is ready to help you build confidence and improve your presentation skills. Start with Normal Practice mode to get comfortable, then challenge yourself with Mock Interview and Public Speaking modes as you progress!

**Launch command**: `python backend/app.py`
**Access URL**: `http://localhost:5000`

Good luck with your public speaking journey! 🌟