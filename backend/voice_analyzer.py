import librosa
import numpy as np
import soundfile as sf
from scipy import signal
import pyaudio
import wave
import threading
import time
from collections import deque

class VoiceAnxietyAnalyzer:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.chunk_size = 1024
        self.recording = False
        self.audio_data = []
        self.silence_threshold = 0.01
        self.speech_segments = []
        self.baseline_noise = None
        
    def record_audio(self, duration=120):  # 2 minutes
        """Record audio for specified duration"""
        audio = pyaudio.PyAudio()
        
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        
        print("Recording started...")
        self.recording = True
        frames = []
        
        for _ in range(0, int(self.sample_rate / self.chunk_size * duration)):
            if not self.recording:
                break
            data = stream.read(self.chunk_size)
            frames.append(data)
        
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Convert to numpy array
        audio_data = b''.join(frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        self.audio_data = audio_array.astype(np.float32) / 32768.0
        
        return self.audio_data
    
    def detect_pauses(self, audio_data, adaptive_threshold=True):
        """Detect pauses with adaptive threshold and noise compensation"""
        if len(audio_data) == 0:
            return []
        
        # Calculate RMS energy with overlapping windows
        frame_length = int(0.025 * self.sample_rate)
        hop_length = int(0.010 * self.sample_rate)
        
        rms = librosa.feature.rms(
            y=audio_data, 
            frame_length=frame_length, 
            hop_length=hop_length
        )[0]
        
        # Adaptive threshold based on audio characteristics
        if adaptive_threshold:
            # Use percentile-based threshold
            noise_floor = np.percentile(rms, 20)  # Bottom 20% as noise
            speech_level = np.percentile(rms, 80)  # Top 80% as speech
            threshold = noise_floor + (speech_level - noise_floor) * 0.3
        else:
            threshold = self.silence_threshold
        
        # Smooth RMS to reduce false positives
        smoothed_rms = signal.medfilt(rms, kernel_size=5)
        silence_frames = smoothed_rms < threshold
        
        # Convert to time
        times = librosa.frames_to_time(
            np.arange(len(rms)), 
            sr=self.sample_rate, 
            hop_length=hop_length
        )
        
        # Find pause segments with minimum duration
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i, is_silent in enumerate(silence_frames):
            if is_silent and not in_pause:
                in_pause = True
                pause_start = times[i]
            elif not is_silent and in_pause:
                in_pause = False
                pause_duration = times[i] - pause_start
                if pause_duration > 0.3:  # Reduced minimum pause duration
                    pauses.append(pause_duration)
        
        return pauses
    
    def detect_stuttering(self, audio_data):
        """Improved stuttering detection with multiple features"""
        if len(audio_data) < self.sample_rate:  # Less than 1 second
            return 0
        
        try:
            # Extract multiple features for better accuracy
            mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=self.sample_rate)[0]
            zero_crossings = librosa.feature.zero_crossing_rate(audio_data)[0]
            
            # Detect repetitive MFCC patterns
            stutter_score = 0
            window_size = 15  # Smaller window for better detection
            correlation_threshold = 0.75  # Slightly lower threshold
            
            if mfccs.shape[1] < window_size * 2:
                return 0
            
            for i in range(0, mfccs.shape[1] - window_size, 5):  # Step by 5 frames
                current_window = mfccs[:, i:i+window_size]
                
                # Look for similar patterns in nearby windows
                for j in range(i+window_size, min(i+window_size*3, mfccs.shape[1]-window_size)):
                    next_window = mfccs[:, j:j+window_size]
                    
                    # Calculate correlation
                    corr = np.corrcoef(current_window.flatten(), next_window.flatten())
                    if corr.shape == (2, 2) and not np.isnan(corr[0, 1]):
                        if corr[0, 1] > correlation_threshold:
                            stutter_score += 1
            
            # Normalize by number of comparisons
            max_comparisons = max(1, (mfccs.shape[1] - window_size) // 5)
            normalized_score = stutter_score / max_comparisons
            
            # Additional check: rapid zero crossing rate changes (disfluency indicator)
            zcr_changes = np.diff(zero_crossings)
            rapid_changes = np.sum(np.abs(zcr_changes) > np.std(zcr_changes) * 2)
            zcr_penalty = min(0.3, rapid_changes / len(zcr_changes))
            
            return min(1.0, normalized_score + zcr_penalty)
            
        except Exception as e:
            return 0
    
    def analyze_speech_rate(self, audio_data):
        """Improved speech rate analysis with voice activity detection"""
        if len(audio_data) == 0:
            return 0
        
        frame_length = int(0.025 * self.sample_rate)
        hop_length = int(0.010 * self.sample_rate)
        
        # Multiple features for better voice activity detection
        zcr = librosa.feature.zero_crossing_rate(
            audio_data, frame_length=frame_length, hop_length=hop_length
        )[0]
        
        rms = librosa.feature.rms(
            y=audio_data, frame_length=frame_length, hop_length=hop_length
        )[0]
        
        # Spectral centroid for voice quality
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio_data, sr=self.sample_rate, hop_length=hop_length
        )[0]
        
        # Adaptive thresholds based on audio characteristics
        rms_threshold = np.percentile(rms, 30)  # Bottom 30% as silence
        zcr_threshold = np.percentile(zcr, 70)   # Top 70% as unvoiced
        centroid_threshold = np.percentile(spectral_centroid, 40)  # Voice range
        
        # Improved voice activity detection
        voice_activity = (
            (rms > rms_threshold) & 
            (zcr < zcr_threshold) & 
            (spectral_centroid > centroid_threshold)
        )
        
        # Calculate speech ratio with smoothing
        smoothed_activity = signal.medfilt(voice_activity.astype(int), kernel_size=5)
        speech_ratio = np.sum(smoothed_activity) / len(smoothed_activity)
        
        return speech_ratio
    
    def get_voice_anxiety_score(self, audio_data):
        """Calculate voice anxiety with improved accuracy and weighting"""
        if len(audio_data) == 0:
            return {
                'anxiety_score': 0, 'pause_score': 0, 'stutter_score': 0,
                'fluency_score': 0, 'avg_pause_duration': 0,
                'num_long_pauses': 0, 'total_pauses': 0
            }
        
        # Analyze with improved methods
        pauses = self.detect_pauses(audio_data, adaptive_threshold=True)
        stutter_score = self.detect_stuttering(audio_data)
        speech_rate = self.analyze_speech_rate(audio_data)
        
        # Enhanced pause analysis
        if pauses:
            avg_pause_duration = np.mean(pauses)
            pause_frequency = len(pauses) / (len(audio_data) / self.sample_rate / 60)  # per minute
            num_long_pauses = len([p for p in pauses if p > 1.5])  # Reduced threshold
        else:
            avg_pause_duration = 0
            pause_frequency = 0
            num_long_pauses = 0
        
        # Improved scoring with non-linear scaling
        # Pause scoring (normal: 2-4 pauses per minute, <1s average)
        pause_freq_score = max(0, min(100, (pause_frequency - 4) * 15)) if pause_frequency > 4 else 0
        pause_duration_score = max(0, min(100, (avg_pause_duration - 1.0) * 50)) if avg_pause_duration > 1.0 else 0
        long_pause_penalty = min(50, num_long_pauses * 15)
        pause_score = (pause_freq_score + pause_duration_score + long_pause_penalty) / 3
        
        # Stutter scoring with better normalization
        stutter_score_norm = min(100, stutter_score * 80)  # Reduced sensitivity
        
        # Fluency scoring (normal speech ratio: 0.4-0.7)
        if speech_rate < 0.3:
            fluency_score = (0.3 - speech_rate) * 150  # Too little speech
        elif speech_rate > 0.8:
            fluency_score = (speech_rate - 0.8) * 100   # Too much continuous speech
        else:
            fluency_score = 0  # Normal range
        
        fluency_score = min(100, fluency_score)
        
        # Weighted combination (pauses most reliable, stuttering least)
        anxiety_score = (
            pause_score * 0.5 + 
            fluency_score * 0.3 + 
            stutter_score_norm * 0.2
        )
        
        return {
            'anxiety_score': min(100, max(0, anxiety_score)),
            'pause_score': pause_score,
            'stutter_score': stutter_score_norm,
            'fluency_score': fluency_score,
            'avg_pause_duration': avg_pause_duration,
            'num_long_pauses': num_long_pauses,
            'total_pauses': len(pauses)
        }