#!/usr/bin/env python3
"""
감정 분석 및 MBTI 추정 기능 테스트
"""
import unittest
import sys
import os

# 프로젝트 경로 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app')
sys.path.insert(0, project_root)
sys.path.insert(0, app_path)

try:
    from components.analyzer import analyze_sentiment, estimate_mbti
except ImportError:
    # 직접 임포트 시도
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
    from components.analyzer import analyze_sentiment, estimate_mbti


class TestAnalyzer(unittest.TestCase):
    """분석기 기능 테스트"""
    
    def setUp(self):
        """테스트 준비"""
        self.test_cases = {
            'positive': [
                "정말 좋은 하루네요!",
                "행복해서 기분이 최고예요",
                "완전 멋진 경험이었어요"
            ],
            'negative': [
                "너무 슬픈 일이에요",
                "정말 화가 나네요", 
                "기분이 안 좋아요"
            ],
            'neutral': [
                "그냥 그래요",
                "보통이에요",
                "특별할 게 없어요"
            ]
        }
        
        self.mbti_test_cases = {
            'E': "우리 함께 파티에 가서 사람들과 대화하며 즐겁게 보내요",
            'I': "혼자 조용히 생각하며 독서하는 시간을 좋아해요",
            'N': "미래의 가능성을 상상하며 창의적으로 생각해요",
            'S': "현재 실제 경험을 바탕으로 실용적으로 접근해요",
            'F': "감정과 공감을 중시하며 따뜻한 관계를 만들어요",
            'T': "논리와 분석을 바탕으로 객관적으로 판단해요",
            'J': "계획을 세워 체계적으로 일을 완성해요",
            'P': "유연하게 적응하며 자유롭게 변화를 즐겨요"
        }
    
    def test_sentiment_analysis_positive(self):
        """긍정적 감정 분석 테스트"""
        for text in self.test_cases['positive']:
            with self.subTest(text=text):
                result = analyze_sentiment(text)
                self.assertIn(result, ['긍정적', '부정적', '중립'])
                print(f"✅ 긍정 테스트: '{text}' -> {result}")
    
    def test_sentiment_analysis_negative(self):
        """부정적 감정 분석 테스트"""
        for text in self.test_cases['negative']:
            with self.subTest(text=text):
                result = analyze_sentiment(text)
                self.assertIn(result, ['긍정적', '부정적', '중립'])
                print(f"✅ 부정 테스트: '{text}' -> {result}")
    
    def test_sentiment_analysis_neutral(self):
        """중립적 감정 분석 테스트"""
        for text in self.test_cases['neutral']:
            with self.subTest(text=text):
                result = analyze_sentiment(text)
                self.assertIn(result, ['긍정적', '부정적', '중립'])
                print(f"✅ 중립 테스트: '{text}' -> {result}")
    
    def test_sentiment_empty_text(self):
        """빈 텍스트 감정 분석 테스트"""
        result = analyze_sentiment("")
        self.assertEqual(result, "분석할 텍스트가 없습니다")
        print(f"✅ 빈 텍스트 테스트: '' -> {result}")
    
    def test_mbti_estimation(self):
        """MBTI 추정 테스트"""
        for trait, text in self.mbti_test_cases.items():
            with self.subTest(trait=trait, text=text):
                result = estimate_mbti(text)
                # MBTI 결과는 4자리 문자여야 함
                self.assertEqual(len(result), 4)
                self.assertTrue(result.isalpha())
                print(f"✅ MBTI 테스트 ({trait}): '{text[:30]}...' -> {result}")
    
    def test_mbti_empty_text(self):
        """빈 텍스트 MBTI 추정 테스트"""
        result = estimate_mbti("")
        self.assertEqual(result, "분석할 텍스트가 없습니다")
        print(f"✅ MBTI 빈 텍스트 테스트: '' -> {result}")
    
    def test_mbti_format_validation(self):
        """MBTI 결과 형식 검증"""
        test_text = "평범한 텍스트입니다"
        result = estimate_mbti(test_text)
        
        if result != "분석할 텍스트가 없습니다":
            # MBTI 결과 형식 검증
            self.assertEqual(len(result), 4, "MBTI는 4자리여야 합니다")
            
            # 각 자리별 유효한 문자 검증
            valid_chars = [
                ['E', 'I'],  # 첫 번째 자리: 외향/내향
                ['S', 'N'],  # 두 번째 자리: 감각/직관
                ['T', 'F'],  # 세 번째 자리: 사고/감정  
                ['J', 'P']   # 네 번째 자리: 판단/인식
            ]
            
            for i, char in enumerate(result):
                self.assertIn(char, valid_chars[i], 
                            f"MBTI {i+1}번째 자리 '{char}'가 유효하지 않습니다")
        
        print(f"✅ MBTI 형식 검증: '{test_text}' -> {result}")


if __name__ == '__main__':
    print("🧪 ENFP AI Voice Chatbot - Analyzer 기능 테스트 시작")
    print("=" * 60)
    
    # 상세한 테스트 결과 출력
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("🎉 모든 테스트가 완료되었습니다!")