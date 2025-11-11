#!/bin/bash
# ENFP AI Voice Chatbot 테스트 실행 스크립트

echo "🧪 ENFP AI Voice Chatbot 테스트 실행"
echo "======================================="

# 간단한 구조 테스트
echo "📝 1. 기본 구조 및 기능성 테스트..."
python tests/run_simple_test.py

echo ""
echo "📝 2. 핵심 기능 테스트..."  
python tests/test_core_functions.py

echo ""
echo "🎯 테스트 완료!"
echo ""
echo "💡 고급 테스트 실행 방법:"
echo "   cd tests && python test_analyzer.py      # 분석기 상세 테스트"
echo "   cd tests && python test_database.py      # 데이터베이스 테스트"
echo "   cd tests && python test_integration.py   # 통합 테스트"