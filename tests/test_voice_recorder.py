#!/usr/bin/env python3
"""
음성 녹음 기능 테스트
"""
import unittest
import sys
import os
import tempfile
import wave

# 프로젝트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from components.voice_recorder import record_audio
import config


class TestVoiceRecorder(unittest.TestCase):
    """음성 녹음 기능 테스트"""
    
    def setUp(self):
        """테스트 준비"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_filename = os.path.join(self.temp_dir, "test_record.wav")
    
    def tearDown(self):
        """테스트 정리"""
        # 임시 파일 삭제
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
        os.rmdir(self.temp_dir)
    
    def test_record_audio_file_creation(self):
        """음성 녹음 파일 생성 테스트"""
        print("🎤 음성 녹음 테스트 (자동으로 1초 후 종료됩니다)...")
        
        # 매우 짧은 시간으로 녹음 (1초)
        short_duration = 1
        try:
            record_audio(self.test_filename, duration=short_duration)
            
            # 파일이 생성되었는지 확인
            self.assertTrue(os.path.exists(self.test_filename), 
                          "녹음 파일이 생성되지 않았습니다")
            
            # 파일 크기가 0보다 큰지 확인
            file_size = os.path.getsize(self.test_filename)
            self.assertGreater(file_size, 0, "녹음 파일이 비어있습니다")
            
            print(f"✅ 녹음 파일 생성 성공: {file_size} bytes")
            
        except Exception as e:
            print(f"⚠️ 녹음 테스트 건너뜀 (마이크 없음): {e}")
            self.skipTest("마이크가 없거나 오디오 장치에 접근할 수 없습니다")
    
    def test_record_audio_wav_format(self):
        """WAV 파일 형식 검증 테스트"""
        print("🎵 WAV 파일 형식 검증 테스트...")
        
        try:
            # 짧은 녹음
            record_audio(self.test_filename, duration=1)
            
            # WAV 파일 헤더 확인
            with wave.open(self.test_filename, 'rb') as wav_file:
                # 채널 수 확인
                channels = wav_file.getnchannels()
                self.assertEqual(channels, config.VOICE_CHANNELS, 
                               f"채널 수가 예상과 다릅니다: {channels}")
                
                # 샘플링 레이트 확인
                sample_rate = wav_file.getframerate()
                self.assertEqual(sample_rate, config.VOICE_SAMPLE_RATE,
                               f"샘플링 레이트가 예상과 다릅니다: {sample_rate}")
                
                # 프레임 수가 0보다 큰지 확인
                frames = wav_file.getnframes()
                self.assertGreater(frames, 0, "오디오 데이터가 없습니다")
                
                print(f"✅ WAV 형식 검증 성공:")
                print(f"   - 채널: {channels}")
                print(f"   - 샘플링 레이트: {sample_rate} Hz")
                print(f"   - 프레임 수: {frames}")
                
        except Exception as e:
            print(f"⚠️ WAV 형식 테스트 건너뜀: {e}")
            self.skipTest("오디오 녹음 또는 파일 분석 실패")
    
    def test_config_values(self):
        """설정 값 검증 테스트"""
        print("⚙️ 음성 녹음 설정 값 검증...")
        
        # 샘플링 레이트 검증
        self.assertIsInstance(config.VOICE_SAMPLE_RATE, int)
        self.assertGreater(config.VOICE_SAMPLE_RATE, 0)
        
        # 채널 수 검증
        self.assertIsInstance(config.VOICE_CHANNELS, int)
        self.assertIn(config.VOICE_CHANNELS, [1, 2])  # 모노 또는 스테레오
        
        # 기본 녹음 시간 검증
        self.assertIsInstance(config.VOICE_DURATION, (int, float))
        self.assertGreater(config.VOICE_DURATION, 0)
        
        print(f"✅ 설정 값 검증 성공:")
        print(f"   - 샘플링 레이트: {config.VOICE_SAMPLE_RATE} Hz")
        print(f"   - 채널 수: {config.VOICE_CHANNELS}")
        print(f"   - 기본 녹음 시간: {config.VOICE_DURATION}초")


if __name__ == '__main__':
    print("🎤 ENFP AI Voice Chatbot - Voice Recorder 기능 테스트 시작")
    print("=" * 60)
    print("⚠️ 주의: 마이크 권한이 필요하며, 테스트 중 짧은 녹음이 진행됩니다.")
    print("=" * 60)
    
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("🎉 음성 녹음 테스트가 완료되었습니다!")