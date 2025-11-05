# Audio Files for AI Public Speaking Coach

This directory should contain the following audio files for the different modes:

## Required Audio Files:

### Public Speaking Mode (Crowd Distractions):
- `crowd_murmur.mp3` - Background crowd murmuring (looped)
- `applause.mp3` - Audience applause sound
- `phone_ring.mp3` - Phone ringing distraction
- `cough.mp3` - Audience member coughing
- `door_slam.mp3` - Door slamming sound
- `whisper.mp3` - Audience whispering

### Interview Mode:
- `office_ambience.mp3` - Quiet office background noise

## Audio File Specifications:
- Format: MP3
- Quality: 128kbps or higher
- Duration: 2-5 seconds for sound effects, 30+ seconds for ambient sounds
- Volume: Normalized to prevent audio clipping

## Sources for Audio Files:
You can obtain these audio files from:
1. **Free Sources:**
   - Freesound.org (Creative Commons licensed)
   - Zapsplat.com (free with registration)
   - YouTube Audio Library
   - BBC Sound Effects Library

2. **Paid Sources:**
   - AudioJungle
   - Pond5
   - Getty Images Audio

3. **Generate Your Own:**
   - Record in a quiet environment
   - Use audio editing software like Audacity (free)
   - Apply noise reduction and normalization

## Implementation Notes:
- Files are loaded automatically when the application starts
- Volume levels are controlled programmatically based on event intensity
- Crowd murmur loops continuously during public speaking mode
- Sound effects are triggered at specific times during the session

## Fallback:
If audio files are not available, the application will continue to work but without the immersive audio experience. The visual elements (jury panel, crowd simulation) will still function normally.