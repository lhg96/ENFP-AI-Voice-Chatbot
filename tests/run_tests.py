#!/usr/bin/env python3
"""
전체 테스트 실행기
"""
import sys
import os
import unittest

# 프로젝트 경로 추가
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app_path = os.path.join(project_root, 'app')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if app_path not in sys.path:
    sys.path.insert(0, app_path)

def run_all_tests():
    """모든 테스트 실행"""
    print("🧪 ENFP AI Voice Chatbot - 전체 기능성 테스트 실행")
    print("=" * 70)
    
    # 테스트 디스커버리
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    # 테스트 실행
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 결과 요약
    print("\n" + "=" * 70)
    print("📊 테스트 결과 요약:")
    print(f"   - 실행된 테스트: {result.testsRun}개")
    print(f"   - 성공: {result.testsRun - len(result.failures) - len(result.errors)}개")
    print(f"   - 실패: {len(result.failures)}개")
    print(f"   - 오류: {len(result.errors)}개")
    
    # 실패한 테스트 상세 정보
    if result.failures:
        print("\n❌ 실패한 테스트:")
        for test, traceback in result.failures:
            print(f"   - {test}: {traceback.splitlines()[-1]}")
    
    # 오류가 발생한 테스트 상세 정보
    if result.errors:
        print("\n⚠️ 오류가 발생한 테스트:")
        for test, traceback in result.errors:
            print(f"   - {test}: {traceback.splitlines()[-1]}")
    
    # 최종 결과
    if result.wasSuccessful():
        print("\n🎉 모든 테스트가 성공적으로 완료되었습니다!")
        return True
    else:
        print(f"\n💥 {len(result.failures) + len(result.errors)}개의 테스트에서 문제가 발생했습니다.")
        return False

def run_quick_test():
    """빠른 핵심 기능 테스트"""
    print("⚡ 빠른 핵심 기능 테스트 실행")
    print("=" * 50)
    
    try:
        # 기본 임포트 테스트
        print("📦 모듈 임포트 테스트...")
        from components.analyzer import analyze_sentiment, estimate_mbti
        from components.database import ConversationDB
        import config
        print("✅ 모든 모듈 임포트 성공")
        
        # 기본 기능 테스트
        print("\n🧠 핵심 기능 테스트...")
        
        # 감정 분석 테스트
        sentiment = analyze_sentiment("오늘 정말 좋은 날이에요!")
        print(f"✅ 감정 분석: '{sentiment}'")
        
        # MBTI 추정 테스트
        mbti = estimate_mbti("친구들과 함께 파티에서 즐겁게 대화했어요")
        print(f"✅ MBTI 추정: '{mbti}'")
        
        # 데이터베이스 테스트
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
            db = ConversationDB(temp_db.name)
            conv_id = db.save_conversation("테스트", sentiment, mbti, "AI 응답")
            print(f"✅ 데이터베이스 저장: ID {conv_id}")
            db.close()
        
        # 설정 테스트
        print(f"✅ 설정 로드: Ollama URL = {config.OLLAMA_BASE_URL}")
        
        print("\n🎉 빠른 테스트 완료 - 모든 핵심 기능이 정상 작동합니다!")
        return True
        
    except Exception as e:
        print(f"\n❌ 빠른 테스트 실패: {str(e)}")
        print("💡 상세한 오류 정보는 전체 테스트를 실행해 주세요.")
        return False

if __name__ == '__main__':
    print("🚀 ENFP AI Voice Chatbot 테스트 시작")
    print("=" * 70)
    
    # 명령행 인수 확인
    if len(sys.argv) > 1 and sys.argv[1] == 'quick':
        # 빠른 테스트
        success = run_quick_test()
    else:
        # 전체 테스트
        print("실행 옵션:")
        print("  python run_tests.py       # 전체 테스트")
        print("  python run_tests.py quick # 빠른 핵심 테스트")
        print()
        
        choice = input("전체 테스트를 실행하시겠습니까? (y/N): ").strip().lower()
        
        if choice in ['y', 'yes', '예']:
            success = run_all_tests()
        else:
            success = run_quick_test()
    
    # 종료 코드 설정
    sys.exit(0 if success else 1)