#!/usr/bin/env python3
"""
Core Functions Test for ENFP AI Voice Chatbot
핵심 기능 (감정 분석, MBTI 추정) 간단 테스트
"""
import sys
import os

# Add the app directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app')
sys.path.insert(0, project_root)
sys.path.insert(0, app_path)

def test_analyzer():
    """Test analyzer functions."""
    print("🧪 Testing ENFP AI Voice Chatbot Core Functions...")
    
    try:
        from components.analyzer import analyze_sentiment, estimate_mbti
        
        # Test sentiment analysis
        print("\n📊 Sentiment Analysis Test:")
        test_text = "정말 좋은 하루네요!"
        sentiment = analyze_sentiment(test_text)
        print(f"Text: '{test_text}' -> Sentiment: {sentiment}")
        
        # Test MBTI estimation
        print("\n🧠 MBTI Estimation Test:")
        mbti_text = "우리 함께 파티에 가서 사람들과 대화하며 즐겁게 보내요"
        mbti = estimate_mbti(mbti_text)
        print(f"Text: '{mbti_text}' -> MBTI: {mbti}")
        
        print("\n✅ All core functions working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Core function test failed: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_analyzer()
    print("\n🎉 Core functions test completed!" if success else "\n⚠️ Core functions test had issues!")
    sys.exit(0 if success else 1)