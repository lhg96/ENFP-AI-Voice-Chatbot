"""
Simple voice recorder for audio capture
"""
import sounddevice as sd
import numpy as np
import wave
import tempfile
import os
import logging

logger = logging.getLogger(__name__)

class VoiceRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.recorded_frames = []

    def callback(self, indata, frames, time, status):
        """Audio callback function."""
        if status:
            logger.error(f'Recording error: {status}')
        self.recorded_frames.append(indata.copy())

    def start_recording(self):
        """Start recording."""
        try:
            self.recording = True
            self.recorded_frames = []
                    
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=self.callback
            )
            self.stream.start()
            logger.info("Recording started")
        except Exception as e:
            logger.error(f"Failed to start recording: {str(e)}")
            self.recording = False
            raise

    def stop_recording(self):
        """Stop recording and return file path."""
        try:
            if hasattr(self, 'stream') and self.stream:
                self.stream.stop()
                self.stream.close()
            self.recording = False
            
            if not self.recorded_frames:
                logger.warning("No audio frames recorded")
                return None
            
            # Create WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                temp_path = temp_wav.name
                
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                
                # Convert and write audio data
                for frame in self.recorded_frames:
                    audio_data = (frame * 32767).astype(np.int16)
                    wf.writeframes(audio_data.tobytes())
            
            logger.info(f"Recording saved to: {temp_path}")
            return temp_path
                
        except Exception as e:
            logger.error(f"Failed to stop recording: {str(e)}")
            return None

    def is_recording(self):
        """Check if currently recording."""
        return self.recording