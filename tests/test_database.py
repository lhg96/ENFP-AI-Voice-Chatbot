#!/usr/bin/env python3
"""
데이터베이스 기능 테스트
"""
import unittest
import sys
import os
import tempfile
import sqlite3
from datetime import datetime

# 프로젝트 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from components.database import ConversationDB


class TestDatabase(unittest.TestCase):
    """데이터베이스 기능 테스트"""
    
    def setUp(self):
        """테스트 준비"""
        # 임시 데이터베이스 파일 생성
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.db = ConversationDB(self.db_path)
    
    def tearDown(self):
        """테스트 정리"""
        # 데이터베이스 연결 종료 및 파일 삭제
        self.db.close()
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_database_creation(self):
        """데이터베이스 생성 테스트"""
        print("💾 데이터베이스 생성 테스트...")
        
        # 데이터베이스 파일이 생성되었는지 확인
        self.assertTrue(os.path.exists(self.db_path), "데이터베이스 파일이 생성되지 않았습니다")
        
        # 테이블이 생성되었는지 확인
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        self.assertIn('conversations', tables, "conversations 테이블이 생성되지 않았습니다")
        
        conn.close()
        print("✅ 데이터베이스 생성 성공")
    
    def test_save_conversation(self):
        """대화 저장 테스트"""
        print("💬 대화 저장 테스트...")
        
        # 테스트 데이터
        test_data = {
            'user_text': '안녕하세요!',
            'sentiment': '긍정적',
            'mbti': 'ENFP',
            'ai_response': '안녕하세요! 좋은 하루 보내고 계시네요!'
        }
        
        # 대화 저장
        conversation_id = self.db.save_conversation(
            test_data['user_text'],
            test_data['sentiment'], 
            test_data['mbti'],
            test_data['ai_response']
        )
        
        # 저장된 ID 확인
        self.assertIsNotNone(conversation_id, "대화가 저장되지 않았습니다")
        self.assertIsInstance(conversation_id, int, "대화 ID가 정수가 아닙니다")
        
        print(f"✅ 대화 저장 성공 (ID: {conversation_id})")
    
    def test_get_conversations(self):
        """대화 조회 테스트"""
        print("📖 대화 조회 테스트...")
        
        # 여러 대화 저장
        conversations_data = [
            ('첫 번째 메시지', '긍정적', 'ENFP', '첫 번째 응답'),
            ('두 번째 메시지', '중립', 'INFP', '두 번째 응답'),
            ('세 번째 메시지', '부정적', 'ESFJ', '세 번째 응답')
        ]
        
        saved_ids = []
        for user_text, sentiment, mbti, ai_response in conversations_data:
            conv_id = self.db.save_conversation(user_text, sentiment, mbti, ai_response)
            saved_ids.append(conv_id)
        
        # 모든 대화 조회
        all_conversations = self.db.get_conversations()
        
        # 저장된 개수와 조회된 개수 확인
        self.assertEqual(len(all_conversations), len(conversations_data),
                        "저장된 대화 개수와 조회된 개수가 다릅니다")
        
        # 최신 대화가 먼저 오는지 확인 (ORDER BY timestamp DESC)
        timestamps = [conv['timestamp'] for conv in all_conversations]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True),
                        "대화가 최신순으로 정렬되지 않았습니다")
        
        print(f"✅ 대화 조회 성공 ({len(all_conversations)}개)")
    
    def test_get_statistics(self):
        """통계 조회 테스트"""
        print("📊 통계 조회 테스트...")
        
        # 테스트 데이터 저장 (감정별 분포 테스트)
        test_data = [
            ('메시지1', '긍정적', 'ENFP', '응답1'),
            ('메시지2', '긍정적', 'ENFP', '응답2'),
            ('메시지3', '부정적', 'INFP', '응답3'),
            ('메시지4', '중립', 'ESFJ', '응답4')
        ]
        
        for user_text, sentiment, mbti, ai_response in test_data:
            self.db.save_conversation(user_text, sentiment, mbti, ai_response)
        
        # 통계 조회
        stats = self.db.get_statistics()
        
        # 통계 데이터 검증
        self.assertIn('total_conversations', stats)
        self.assertIn('sentiment_distribution', stats)
        self.assertIn('mbti_distribution', stats)
        self.assertIn('recent_conversations', stats)
        
        # 총 대화 수 확인
        self.assertEqual(stats['total_conversations'], len(test_data))
        
        # 감정 분포 확인
        sentiment_dist = stats['sentiment_distribution']
        self.assertEqual(sentiment_dist['긍정적'], 2)
        self.assertEqual(sentiment_dist['부정적'], 1)
        self.assertEqual(sentiment_dist['중립'], 1)
        
        print(f"✅ 통계 조회 성공:")
        print(f"   - 총 대화 수: {stats['total_conversations']}")
        print(f"   - 감정 분포: {sentiment_dist}")
    
    def test_clear_database(self):
        """데이터베이스 초기화 테스트"""
        print("🗑️ 데이터베이스 초기화 테스트...")
        
        # 테스트 데이터 저장
        self.db.save_conversation('테스트', '긍정적', 'ENFP', '응답')
        
        # 데이터가 있는지 확인
        conversations_before = self.db.get_conversations()
        self.assertGreater(len(conversations_before), 0, "테스트 데이터가 저장되지 않았습니다")
        
        # 데이터베이스 초기화
        self.db.clear_database()
        
        # 데이터가 삭제되었는지 확인
        conversations_after = self.db.get_conversations()
        self.assertEqual(len(conversations_after), 0, "데이터베이스가 초기화되지 않았습니다")
        
        print("✅ 데이터베이스 초기화 성공")
    
    def test_database_integrity(self):
        """데이터베이스 무결성 테스트"""
        print("🔍 데이터베이스 무결성 테스트...")
        
        # 특수 문자가 포함된 데이터 테스트
        special_data = [
            ('텍스트에 "따옴표"와 \'작은따옴표\' 포함', '긍정적', 'ENFP', 'AI 응답'),
            ('줄바꿈\n포함된\n텍스트', '중립', 'INFP', '응답\n여러줄'),
            ('이모지 🎉🚀💖 포함', '긍정적', 'ESFJ', '이모지 응답 😊'),
            ('NULL 값 테스트', None, None, None)
        ]
        
        for user_text, sentiment, mbti, ai_response in special_data:
            try:
                conv_id = self.db.save_conversation(user_text, sentiment, mbti, ai_response)
                self.assertIsNotNone(conv_id, f"특수 데이터 저장 실패: {user_text}")
            except Exception as e:
                self.fail(f"특수 데이터 저장 중 오류: {user_text}, {e}")
        
        # 저장된 데이터 조회 및 검증
        conversations = self.db.get_conversations()
        self.assertEqual(len(conversations), len(special_data), "특수 데이터가 모두 저장되지 않았습니다")
        
        print("✅ 데이터베이스 무결성 테스트 성공")


if __name__ == '__main__':
    print("💾 ENFP AI Voice Chatbot - Database 기능 테스트 시작")
    print("=" * 60)
    
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 60)
    print("🎉 데이터베이스 테스트가 완료되었습니다!")