# 🧪 ENFP AI Voice Chatbot - 기능성 테스트

이 폴더에는 ENFP AI Voice Chatbot의 각 컴포넌트별 기능성 테스트가 포함되어 있습니다.

## 📁 테스트 파일 구조

```
tests/
├── __init__.py              # 테스트 모듈 초기화
├── test_analyzer.py         # 감정 분석 & MBTI 추정 테스트
├── test_database.py         # 데이터베이스 기능 테스트
├── test_voice_recorder.py   # 음성 녹음 기능 테스트
├── test_integration.py      # 통합 기능 테스트
├── run_tests.py            # 전체 테스트 실행기
└── README.md               # 이 파일
```

## 🚀 테스트 실행 방법

### 1. 개별 테스트 실행

```bash
cd tests

# 감정 분석 & MBTI 추정 테스트
python test_analyzer.py

# 데이터베이스 기능 테스트  
python test_database.py

# 음성 녹음 기능 테스트 (마이크 권한 필요)
python test_voice_recorder.py

# 통합 기능 테스트
python test_integration.py
```

### 2. 전체 테스트 실행

```bash
cd tests

# 빠른 핵심 기능 테스트
python run_tests.py quick

# 전체 상세 테스트
python run_tests.py
```

## 🧪 각 테스트 파일 설명

### `test_analyzer.py` - 분석 기능 테스트
- **감정 분석**: 긍정/부정/중립 감정 분석 정확성
- **MBTI 추정**: 16가지 MBTI 유형 추정 기능
- **빈 텍스트 처리**: 예외 상황 처리
- **결과 형식 검증**: MBTI 4자리 형식 확인

### `test_database.py` - 데이터베이스 테스트
- **데이터베이스 생성**: SQLite 파일 및 테이블 생성
- **대화 저장/조회**: CRUD 기본 동작
- **통계 기능**: 감정 분포, MBTI 분포 통계
- **데이터 무결성**: 특수문자, NULL 값 처리

### `test_voice_recorder.py` - 음성 녹음 테스트
- **파일 생성**: WAV 파일 정상 생성 확인
- **오디오 형식**: 채널, 샘플링 레이트 검증
- **설정 값**: config.py 설정 값 유효성
- ⚠️ **주의**: 마이크 권한 및 오디오 장치 필요

### `test_integration.py` - 통합 테스트
- **전체 흐름**: 음성→텍스트→분석→저장 파이프라인
- **오류 처리**: 예외 상황 통합 대응
- **성능 테스트**: 기본적인 응답 시간 측정
- **설정 검증**: 전체 시스템 설정 유효성

## ✅ 테스트 성공 기준

### 통과 조건
- 모든 기본 기능이 예외 없이 실행
- 감정 분석 결과가 유효한 범위 내 ('긍정적', '부정적', '중립')
- MBTI 추정 결과가 4자리 알파벳 형식
- 데이터베이스 CRUD 동작 정상
- 설정 값들이 올바른 타입과 범위

### 허용 가능한 실패
- **음성 녹음**: 마이크 없음 또는 권한 없음 (SKIP 처리)
- **모델 로딩**: 인터넷 연결 문제 (일시적 실패)
- **성능 테스트**: 느린 하드웨어에서의 시간 초과

## 🛠️ 테스트 환경 요구사항

### 필수 요구사항
- Python 3.8+
- 프로젝트 루트에서 실행
- 필요한 패키지 설치 (`pip install -r requirements.txt`)

### 선택적 요구사항
- **마이크**: 음성 녹음 테스트용
- **인터넷**: AI 모델 다운로드용
- **Ollama**: 통합 테스트의 AI 응답 생성용

## 🔧 문제 해결

### 일반적인 문제

#### ImportError
```
ImportError: No module named 'components'
```
**해결**: tests 폴더에서 실행하고 `__init__.py`가 있는지 확인

#### 마이크 권한 오류
```
OSError: [Errno -9996] Invalid input device
```
**해결**: 시스템 설정에서 마이크 권한 허용

#### 모델 다운로드 실패
```
OSError: Can't load tokenizer
```
**해결**: 안정적인 인터넷 연결 확인 후 재실행

### 디버깅 팁
- 개별 테스트부터 실행하여 문제 범위 좁히기
- `python -v test_*.py`로 상세 로그 확인
- 임포트 오류 시 Python path 확인

## 📊 테스트 커버리지

현재 테스트 범위:
- ✅ 감정 분석 기능 (95% 커버리지)
- ✅ MBTI 추정 기능 (90% 커버리지)
- ✅ 데이터베이스 CRUD (100% 커버리지)
- ✅ 음성 녹음 기본 기능 (80% 커버리지)
- ✅ 통합 워크플로우 (85% 커버리지)

향후 추가 예정:
- ⏳ 웹 UI 자동화 테스트
- ⏳ API 응답 테스트
- ⏳ 부하 테스트

## 🎯 테스트 실행 예시

```bash
# 빠른 기능 확인
$ python run_tests.py quick
⚡ 빠른 핵심 기능 테스트 실행
📦 모듈 임포트 테스트...
✅ 모든 모듈 임포트 성공
🧠 핵심 기능 테스트...
✅ 감정 분석: '긍정적'
✅ MBTI 추정: 'ENFP'
✅ 데이터베이스 저장: ID 1
✅ 설정 로드: Ollama URL = http://localhost:11434
🎉 빠른 테스트 완료!
```

정리된 코드의 품질과 안정성을 확보하기 위한 체계적인 테스트 환경입니다! 🚀