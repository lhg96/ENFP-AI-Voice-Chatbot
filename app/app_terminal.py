#!/usr/bin/env python3
"""
Simple terminal version of ENFP AI Voice Chatbot
"""
import speech_recognition as sr
import os
import sys
from dotenv import load_dotenv
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from components.analyzer import analyze_sentiment, estimate_mbti

# Disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

# Initialize tools
recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.5

def listen_and_respond():
    """Simple voice input and analysis."""
    try:
        with sr.Microphone() as source:
            print("🎙️ 듣는 중... (5초간)")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
        
        text = recognizer.recognize_google(audio, language='ko-KR')
        print(f"👤 사용자: {text}")
        
        # 종료 체크
        if text.lower() in ["종료", "exit", "quit", "끝"]:
            return False
        
        # 분석
        sentiment = analyze_sentiment(text)
        mbti = estimate_mbti(text)
        
        print(f"😊 감정: {sentiment}")
        print(f"🧠 MBTI: {mbti}")
        
        return True
        
    except sr.UnknownValueError:
        print("❌ 음성을 인식하지 못했습니다.")
        return True
    except sr.RequestError as e:
        print(f"❌ 음성 인식 서비스 오류: {e}")
        return True
    except Exception as e:
        print(f"❌ 오류: {e}")
        return True

def main():
    """Simple main function."""
    print("🌟 ENFP AI 음성 분석기 🌟")
    print("말씀하세요. '종료'라고 하면 끝납니다.\n")
    
    while True:
        input("Enter를 눌러 말하기... ")
        if not listen_and_respond():
            print("👋 안녕히 가세요!")
            break

if __name__ == "__main__":
    main()