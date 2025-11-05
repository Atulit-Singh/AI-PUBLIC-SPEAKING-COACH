# Video Files for AI Public Speaking Coach

This directory should contain video files for the immersive interview experience.

## Required Video Files:

### Interview Mode:
- `jury_panel.mp4` - Video of 3 judges/interviewers sitting at a panel

## Video Specifications:
- **Format:** MP4 (H.264 codec recommended)
- **Resolution:** 1280x720 (720p) or higher
- **Duration:** 2-3 minutes (will loop during session)
- **Frame Rate:** 30fps
- **Audio:** Optional (will be muted in application)
- **File Size:** Keep under 50MB for web performance

## Content Requirements:

### Jury Panel Video (`jury_panel.mp4`):
- **Scene:** 3 professional-looking individuals sitting at a panel/table
- **Setting:** Office or conference room environment
- **Behavior:** 
  - Neutral to slightly serious expressions
  - Occasional note-taking gestures
  - Subtle head movements (nodding, looking at papers)
  - Professional attire (business formal)
- **Camera Angle:** Wide shot showing all three panel members
- **Lighting:** Professional, well-lit environment

## Creating Your Own Video:

### Option 1: Record Real People
1. Set up a conference room or office space
2. Position 3 people at a table/desk
3. Use a tripod for stable footage
4. Record 2-3 minutes of natural interview panel behavior
5. Edit to remove any distracting elements

### Option 2: Use Stock Video
- Search for "interview panel", "business meeting", "judges panel"
- Ensure proper licensing for your use case
- Popular stock video sites:
  - Shutterstock
  - Getty Images
  - Adobe Stock
  - Pexels (free)
  - Pixabay (free)

### Option 3: AI-Generated Video
- Use AI video generation tools
- Create realistic business meeting scenarios
- Ensure consistent quality and professional appearance

## Technical Setup:
1. Place the video file in this directory as `jury_panel.mp4`
2. The application will automatically load and display it during interview mode
3. Video will be positioned as a small overlay in the bottom-right corner
4. JavaScript will trigger visual reactions (highlighting specific judges) based on session events

## Fallback:
If the video file is not available, the interview mode will still function with:
- Text-based jury reactions
- Visual indicators showing judge responses
- All other interview mode features intact

The video enhances immersion but is not required for core functionality.