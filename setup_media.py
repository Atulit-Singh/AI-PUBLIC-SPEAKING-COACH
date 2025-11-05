#!/usr/bin/env python3
"""
Media Setup Script for AI Public Speaking Coach
Creates placeholder media files and provides download instructions
"""

import os
import json
from pathlib import Path

def create_placeholder_audio():
    """Create placeholder audio files with instructions"""
    sounds_dir = Path("backend/static/sounds")
    sounds_dir.mkdir(parents=True, exist_ok=True)
    
    audio_files = [
        "crowd_murmur.mp3",
        "applause.mp3", 
        "phone_ring.mp3",
        "cough.mp3",
        "door_slam.mp3",
        "whisper.mp3",
        "office_ambience.mp3"
    ]
    
    for audio_file in audio_files:
        placeholder_path = sounds_dir / audio_file
        if not placeholder_path.exists():
            # Create empty placeholder file
            placeholder_path.touch()
            print(f"Created placeholder: {placeholder_path}")

def create_placeholder_video():
    """Create placeholder video files with instructions"""
    videos_dir = Path("backend/static/videos")
    videos_dir.mkdir(parents=True, exist_ok=True)
    
    video_files = ["jury_panel.mp4"]
    
    for video_file in video_files:
        placeholder_path = videos_dir / video_file
        if not placeholder_path.exists():
            # Create empty placeholder file
            placeholder_path.touch()
            print(f"Created placeholder: {placeholder_path}")

def create_media_config():
    """Create configuration file for media assets"""
    config = {
        "audio_files": {
            "crowd_murmur.mp3": {
                "description": "Background crowd murmuring for public speaking mode",
                "duration": "30+ seconds",
                "loop": True,
                "volume": 0.3
            },
            "applause.mp3": {
                "description": "Audience applause sound effect",
                "duration": "3-5 seconds", 
                "loop": False,
                "volume": 0.6
            },
            "phone_ring.mp3": {
                "description": "Phone ringing distraction",
                "duration": "2-3 seconds",
                "loop": False,
                "volume": 0.5
            },
            "cough.mp3": {
                "description": "Audience member coughing",
                "duration": "1-2 seconds",
                "loop": False,
                "volume": 0.4
            },
            "door_slam.mp3": {
                "description": "Door slamming sound",
                "duration": "1-2 seconds",
                "loop": False,
                "volume": 0.7
            }
        },
        "video_files": {
            "jury_panel.mp4": {
                "description": "Video of 3 judges for interview mode",
                "resolution": "1280x720",
                "duration": "2-3 minutes",
                "loop": True
            }
        },
        "download_sources": {
            "free_audio": [
                "https://freesound.org",
                "https://zapsplat.com", 
                "https://www.youtube.com/audiolibrary",
                "https://sound-effects.bbcrewind.co.uk"
            ],
            "free_video": [
                "https://www.pexels.com/videos",
                "https://pixabay.com/videos",
                "https://www.videvo.net"
            ],
            "paid_sources": [
                "https://audiojungle.net",
                "https://www.shutterstock.com",
                "https://www.gettyimages.com"
            ]
        }
    }
    
    config_path = Path("media_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Created media configuration: {config_path}")

def print_instructions():
    """Print setup instructions"""
    print("\n" + "="*60)
    print("AI PUBLIC SPEAKING COACH - MEDIA SETUP")
    print("="*60)
    print("\nPlaceholder files have been created. To complete the setup:")
    print("\n1. AUDIO FILES (backend/static/sounds/):")
    print("   - Replace placeholder .mp3 files with actual audio")
    print("   - Use the media_config.json for specifications")
    print("   - Free sources: freesound.org, zapsplat.com")
    print("\n2. VIDEO FILES (backend/static/videos/):")
    print("   - Replace jury_panel.mp4 with actual video")
    print("   - Should show 3 professional judges/interviewers")
    print("   - Free sources: pexels.com, pixabay.com")
    print("\n3. ALTERNATIVE (No Media Files):")
    print("   - Application works without media files")
    print("   - Visual effects and text indicators still function")
    print("   - Audio enhances but is not required")
    print("\n4. QUICK START:")
    print("   - Run: python backend/app.py")
    print("   - Open: http://localhost:5000")
    print("   - Grant camera/microphone permissions")
    print("\n" + "="*60)

def main():
    """Main setup function"""
    print("Setting up AI Public Speaking Coach media files...")
    
    create_placeholder_audio()
    create_placeholder_video() 
    create_media_config()
    print_instructions()

if __name__ == "__main__":
    main()