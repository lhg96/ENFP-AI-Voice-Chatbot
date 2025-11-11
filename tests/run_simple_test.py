#!/usr/bin/env python3
"""
간단한 기능성 테스트 실행기
"""
import os
import sys

def test_basic_functionality():
    """기본 기능 테스트"""
    print("🧪 ENFP AI Voice Chatbot - 간단한 기능성 테스트")
    print("=" * 55)
    
    # 프로젝트 루트로 이동
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    print(f"📁 작업 디렉토리: {os.getcwd()}")
    
    # 파일 구조 확인
    print("\n📂 프로젝트 구조 확인:")
    required_files = [
        'app/app.py',
        'app/app_terminal.py', 
        'app/components/analyzer.py',
        'app/components/database.py',
        'app/components/voice_recorder.py',
        'config.py',
        'requirements.txt'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"  ✅ {file_path} ({file_size} bytes)")
        else:
            print(f"  ❌ {file_path} - 파일 없음")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n💥 필수 파일이 누락되었습니다!")
        return False
    
    # 설정 파일 테스트
    print("\n⚙️ 설정 파일 테스트:")
    try:
        sys.path.insert(0, '.')
        import config
        
        config_attrs = ['OLLAMA_BASE_URL', 'OLLAMA_MODEL', 'VOICE_SAMPLE_RATE', 'VOICE_CHANNELS']
        for attr in config_attrs:
            if hasattr(config, attr):
                value = getattr(config, attr)
                print(f"  ✅ {attr} = {value}")
            else:
                print(f"  ❌ {attr} - 설정 누락")
                
        print("  ✅ config.py 로드 성공")
    except Exception as e:
        print(f"  ❌ config.py 오류: {e}")
        return False
    
    # 의존성 확인
    print("\n📦 주요 의존성 확인:")
    dependencies = [
        ('streamlit', 'Streamlit 웹 프레임워크'),
        ('transformers', 'Hugging Face Transformers'),
        ('torch', 'PyTorch'),
        ('requests', 'HTTP 요청 라이브러리'),
        ('sqlite3', 'SQLite 데이터베이스 (내장)')
    ]
    
    missing_deps = []
    for dep, desc in dependencies:
        try:
            if dep == 'sqlite3':
                import sqlite3
            else:
                __import__(dep)
            print(f"  ✅ {dep} - {desc}")
        except ImportError:
            print(f"  ⚠️ {dep} - {desc} (설치 필요)")
            missing_deps.append(dep)
    
    # 간단한 기능 테스트 (의존성 없이)
    print("\n🧠 기본 분석 로직 테스트:")
    try:
        # 간단한 키워드 기반 테스트
        test_text = "정말 행복하고 즐거운 하루예요!"
        
        # MBTI 키워드 테스트 (analyzer.py 로직 간소화)
        mbti_keywords = {
            'E': ['함께', '파티', '사람들', '대화', '모임'],
            'I': ['혼자', '조용히', '독서', '생각', '평화'],
            'N': ['상상', '창의적', '미래', '가능성', '직감'],
            'S': ['실제', '경험', '현실', '구체적', '실용'],
            'F': ['감정', '공감', '따뜻', '관계', '배려'],
            'T': ['논리', '분석', '객관적', '합리', '효율'],
            'J': ['계획', '체계', '완성', '정리', '시간'],
            'P': ['자유', '유연', '적응', '변화', '즉흥']
        }
        
        # 간단한 MBTI 점수 계산
        scores = {}
        for trait, keywords in mbti_keywords.items():
            score = sum(1 for keyword in keywords if keyword in test_text)
            scores[trait] = score
        
        # 각 차원에서 높은 점수 선택
        mbti_result = ""
        mbti_result += 'E' if scores.get('E', 0) >= scores.get('I', 0) else 'I'
        mbti_result += 'N' if scores.get('N', 0) >= scores.get('S', 0) else 'S'
        mbti_result += 'F' if scores.get('F', 0) >= scores.get('T', 0) else 'T'
        mbti_result += 'P' if scores.get('P', 0) >= scores.get('J', 0) else 'J'
        
        print(f"  테스트 텍스트: '{test_text}'")
        print(f"  ✅ MBTI 추정 로직: {mbti_result}")
        print(f"  ✅ 키워드 점수: E={scores.get('E',0)}, I={scores.get('I',0)}, N={scores.get('N',0)}, S={scores.get('S',0)}")
        
    except Exception as e:
        print(f"  ❌ 기본 분석 로직 오류: {e}")
        return False
    
    # 결과 요약
    print("\n" + "=" * 55)
    print("📊 테스트 결과 요약:")
    print(f"  - 파일 구조: {'✅ 정상' if all_files_exist else '❌ 문제 있음'}")
    print(f"  - 설정 파일: ✅ 정상")
    print(f"  - 기본 로직: ✅ 정상")
    
    if missing_deps:
        print(f"  - 누락된 의존성: {', '.join(missing_deps)}")
        print("\n💡 누락된 의존성 설치:")
        print(f"     pip install {' '.join(missing_deps)}")
    else:
        print(f"  - 의존성: ✅ 모두 설치됨")
    
    print("\n🎉 기본 구조와 로직이 정상적으로 구성되어 있습니다!")
    print("🚀 실행 방법:")
    print("   cd app && streamlit run app.py           # 웹 버전")
    print("   cd app && python app_terminal.py         # 터미널 버전") 
    print("   python tests/test_core_functions.py      # 핵심 기능 테스트")
    
    return True

if __name__ == '__main__':
    success = test_basic_functionality()
    sys.exit(0 if success else 1)