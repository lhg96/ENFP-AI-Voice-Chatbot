#!/usr/bin/env python3
"""
통합 기능 테스트
"""
import unittest
import sys
import os
import tempfile
import time

# 프로젝트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from components.analyzer import analyze_sentiment, estimate_mbti
    from components.database import ConversationDB
    import config
except ImportError as e:
    print(f"⚠️ 모듈 임포트 오류: {e}")
    print("프로젝트 구조를 확인해주세요.")


class TestIntegration(unittest.TestCase):
    """통합 기능 테스트"""
    
    def setUp(self):
        """테스트 준비"""
        # 임시 데이터베이스
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = ConversationDB(self.db_path)
        
        # 테스트 시나리오
        self.test_conversations = [
            "정말 행복한 하루예요! 친구들과 파티에서 즐겁게 놀았어요",
            "혼자 조용히 책을 읽으며 깊은 생각에 빠져 있어요",
            "계획을 세워서 체계적으로 프로젝트를 진행하고 있어요",
            "유연하게 상황에 맞춰 자유롭게 적응하며 살아가요"
        ]
    
    def tearDown(self):
        """테스트 정리"""
        self.db.close()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_full_conversation_flow(self):
        """전체 대화 흐름 테스트"""
        print("🔄 전체 대화 흐름 통합 테스트...")
        
        processed_conversations = []
        
        for i, user_input in enumerate(self.test_conversations):
            print(f"\n--- 대화 {i+1}: {user_input[:30]}... ---")
            
            # 1. 감정 분석
            sentiment = analyze_sentiment(user_input)
            self.assertIn(sentiment, ['긍정적', '부정적', '중립'])
            print(f"📊 감정 분석: {sentiment}")
            
            # 2. MBTI 추정  
            mbti = estimate_mbti(user_input)
            self.assertEqual(len(mbti), 4)
            print(f"🧠 MBTI 추정: {mbti}")
            
            # 3. AI 응답 (모의)
            ai_response = f"ENFP AI: {user_input}에 대한 {sentiment} 감정과 {mbti} 특성을 반영한 응답"
            
            # 4. 데이터베이스 저장
            conv_id = self.db.save_conversation(user_input, sentiment, mbti, ai_response)
            self.assertIsNotNone(conv_id)
            print(f"💾 데이터베이스 저장: ID {conv_id}")
            
            processed_conversations.append({
                'id': conv_id,
                'user_text': user_input,
                'sentiment': sentiment,
                'mbti': mbti,
                'ai_response': ai_response
            })
            
            # 처리 시간 시뮬레이션
            time.sleep(0.1)
        
        # 5. 저장된 대화 조회
        saved_conversations = self.db.get_conversations()
        self.assertEqual(len(saved_conversations), len(self.test_conversations))
        print(f"\n📖 저장된 대화 수: {len(saved_conversations)}")
        
        # 6. 통계 확인
        stats = self.db.get_statistics()
        print(f"📊 통계:")
        print(f"   - 총 대화 수: {stats['total_conversations']}")
        print(f"   - 감정 분포: {stats['sentiment_distribution']}")
        print(f"   - MBTI 분포: {stats['mbti_distribution']}")
        
        print("\n✅ 전체 대화 흐름 테스트 성공!")
    
    def test_error_handling(self):
        """오류 처리 테스트"""
        print("⚠️ 오류 처리 테스트...")
        
        # 빈 텍스트 처리
        empty_sentiment = analyze_sentiment("")
        empty_mbti = estimate_mbti("")
        
        self.assertEqual(empty_sentiment, "분석할 텍스트가 없습니다")
        self.assertEqual(empty_mbti, "분석할 텍스트가 없습니다")
        
        # 데이터베이스에 빈 데이터 저장
        conv_id = self.db.save_conversation("", empty_sentiment, empty_mbti, "빈 텍스트 응답")
        self.assertIsNotNone(conv_id)
        
        print("✅ 오류 처리 테스트 성공")
    
    def test_performance_baseline(self):
        """기본 성능 테스트"""
        print("⏱️ 기본 성능 테스트...")
        
        test_text = "이것은 성능 측정을 위한 테스트 텍스트입니다."
        
        # 감정 분석 성능
        start_time = time.time()
        sentiment = analyze_sentiment(test_text)
        sentiment_time = time.time() - start_time
        
        # MBTI 추정 성능
        start_time = time.time()
        mbti = estimate_mbti(test_text)
        mbti_time = time.time() - start_time
        
        # 데이터베이스 저장 성능
        start_time = time.time()
        conv_id = self.db.save_conversation(test_text, sentiment, mbti, "성능 테스트 응답")
        db_time = time.time() - start_time
        
        print(f"📈 성능 측정 결과:")
        print(f"   - 감정 분석: {sentiment_time:.3f}초")
        print(f"   - MBTI 추정: {mbti_time:.3f}초") 
        print(f"   - 데이터베이스 저장: {db_time:.3f}초")
        
        # 성능 기준 확인 (각 기능이 10초 이내)
        self.assertLess(sentiment_time, 10, "감정 분석이 너무 오래 걸립니다")
        self.assertLess(mbti_time, 10, "MBTI 추정이 너무 오래 걸립니다")
        self.assertLess(db_time, 1, "데이터베이스 저장이 너무 오래 걸립니다")
        
        print("✅ 기본 성능 테스트 통과")
    
    def test_config_validation(self):
        """설정 값 검증 테스트"""
        print("⚙️ 설정 값 검증 테스트...")
        
        # 필수 설정 값 존재 확인
        required_configs = [
            'OLLAMA_BASE_URL',
            'OLLAMA_MODEL', 
            'VOICE_SAMPLE_RATE',
            'VOICE_CHANNELS',
            'VOICE_DURATION',
            'DATABASE_PATH'
        ]
        
        for config_name in required_configs:
            self.assertTrue(hasattr(config, config_name), 
                          f"필수 설정 '{config_name}'이 없습니다")
            
            config_value = getattr(config, config_name)
            self.assertIsNotNone(config_value, 
                               f"설정 '{config_name}'이 None입니다")
        
        # 설정 값 타입 확인
        self.assertIsInstance(config.VOICE_SAMPLE_RATE, int)
        self.assertIsInstance(config.VOICE_CHANNELS, int)
        self.assertIsInstance(config.VOICE_DURATION, (int, float))
        
        print(f"✅ 설정 값 검증 성공 ({len(required_configs)}개 설정 확인)")


if __name__ == '__main__':
    print("🔗 ENFP AI Voice Chatbot - 통합 기능 테스트 시작")
    print("=" * 60)
    print("이 테스트는 전체 시스템의 통합 동작을 확인합니다.")
    print("=" * 60)
    
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("🎉 통합 기능 테스트가 완료되었습니다!")