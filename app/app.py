import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import time
import os
import sys
from dotenv import load_dotenv
import logging
from pyngrok import ngrok
import ollama
import uuid
from datetime import datetime

# Add parent directory to path for config import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

from components.analyzer import analyze_sentiment, estimate_mbti
from components.voice_recorder import VoiceRecorder
from components.database import ConversationDB

# Logging setup with config
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize database
db = ConversationDB()

# Initialize session ID
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Ngrok setup (optional)
enable_ngrok = os.getenv("ENABLE_NGROK", "false").lower() == "true"
if enable_ngrok:
    try:
        ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN"))
        http_tunnel = ngrok.connect(config.NGROK_PORT)
        st.success(f"🌐 Public URL: {http_tunnel.public_url}")
    except Exception as e:
        st.warning(f"⚠️ Ngrok 연결 실패: {e}")
        st.info("🏠 로컬 모드로 실행됩니다")
else:
    st.info("🏠 로컬 전용 모드로 실행 중")

# Initialize tools
# pygame mixer 초기화 (macOS 호환성 개선)
try:
    pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
    pygame.mixer.init()
    logger.info("Audio mixer initialized successfully")
except Exception as e:
    logger.error(f"Audio mixer initialization failed: {e}")
    st.warning("⚠️ 오디오 시스템 초기화 실패 - 음성 출력이 제한될 수 있습니다")

recognizer = sr.Recognizer()
recorder = VoiceRecorder(
    sample_rate=config.VOICE_SAMPLE_RATE,
    channels=config.VOICE_CHANNELS
)

# Parameters
recognizer.pause_threshold = 1.5

def play_speech(text):
    """Convert text to speech and play it."""
    try:
        if not text.strip():
            return
            
        # gTTS로 음성 생성
        tts = gTTS(text=text, lang='ko', slow=False)
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        # pygame mixer로 재생
        pygame.mixer.music.load(mp3_fp)
        pygame.mixer.music.play()
        
        # 재생 완료까지 대기
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        mp3_fp.close()
        logger.info(f"Speech played successfully: {text[:50]}...")
        
    except Exception as e:
        logger.error(f"Speech playback error: {str(e)}")
        st.error(f"🔊 음성 출력 오류: {str(e)}")
        # 대안으로 텍스트만 표시
        st.info(f"🗣️ AI 응답: {text}")

def process_voice_input():
    """Process voice input and return transcribed text."""
    try:
        # 상태 표시를 위한 플레이스홀더
        status_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        recorder.start_recording()
        status_placeholder.info("🎤 음성을 듣고 있습니다... (5초간)")
        
        # 프로그레스 바 애니메이션
        for i in range(config.VOICE_DURATION):
            time.sleep(1)
            progress_bar.progress((i + 1) / config.VOICE_DURATION)
        
        wav_path = recorder.stop_recording()
        status_placeholder.info("🔄 음성을 처리하고 있습니다...")
        progress_bar.empty()
        
        if not wav_path:
            status_placeholder.error("❌ 녹음 파일을 생성할 수 없습니다.")
            return None
        
        with sr.AudioFile(wav_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio, language='ko-KR')
        
        os.remove(wav_path)  # Clean up temporary file
        status_placeholder.success(f"✅ 인식 완료: {text}")
        time.sleep(1)
        status_placeholder.empty()
        return text
    except sr.UnknownValueError:
        status_placeholder.error("❌ 음성을 인식할 수 없습니다.")
        return None
    except sr.RequestError as e:
        status_placeholder.error(f"❌ 음성 인식 서비스 오류: {str(e)}")
        return None
    except Exception as e:
        status_placeholder.error(f"❌ 오류 발생: {str(e)}")
        return None

def generate_response(text):
    """Generate response using Ollama phi4:latest model."""
    try:
        sentiment = analyze_sentiment(text)
        prompt = f"""당신은 ENFP 성격의 AI 어시스턴트입니다. 사용자의 감정은 {sentiment}입니다. 
다음 질문에 한국어로 친근하고 공감적으로 답변해주세요: {text}
항상 긍정적이고 열정적인 ENFP의 성격을 반영하여 답변하세요."""
        
        response = ollama.generate(
            model=config.OLLAMA_MODEL,
            prompt=prompt,
            options={
                "max_tokens": config.MAX_TOKENS,
                "temperature": config.TEMPERATURE,
                "top_k": config.TOP_K,
                "top_p": config.TOP_P
            }
        )['response']
        return response
    except Exception as e:
        logger.error(f"Response generation error: {str(e)}")
        st.error(f"응답 생성 오류: {str(e)}")
        return "죄송합니다, 응답을 생성할 수 없습니다."

def main():
    """Main Streamlit application with database integration."""
    # 페이지 설정
    st.set_page_config(
        page_title="ENFP AI Voice Chatbot",
        page_icon="🌟",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 커스텀 CSS 스타일
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #2196f3;
    }
    .ai-message {
        background-color: #f3e5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        border-left: 4px solid #9c27b0;
    }
    .input-container {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="main-header">🌟 ENFP AI Voice Chatbot 🌟</h1>', unsafe_allow_html=True)
    
    # Session state for conversation history
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    
    # 사이드바 설정
    with st.sidebar:
        st.header("🎛️ 설정 & 정보")
        
        # 음성 출력 설정
        if "enable_speech" not in st.session_state:
            st.session_state.enable_speech = True
        
        st.session_state.enable_speech = st.checkbox(
            "🔊 음성 출력 활성화", 
            value=st.session_state.enable_speech,
            help="AI 응답을 음성으로 재생합니다"
        )
        
        st.divider()
        
        # 세션 정보
        st.info(f"**세션 ID**: {st.session_state.session_id[:8]}...")
        
        # 대화 기록 내보내기
        if st.button("📄 대화 기록 내보내기", use_container_width=True):
            export_data = db.export_conversations(st.session_state.session_id, 'json')
            st.download_button(
                label="📥 JSON 다운로드",
                data=export_data,
                file_name=f"conversation_{st.session_state.session_id}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # 세션 통계 (사이드바로 이동)
        if st.session_state.conversation:
            stats = db.get_session_stats(st.session_state.session_id)
            if stats:
                st.header("📊 세션 통계")
                st.metric("총 메시지", stats['total_messages'])
                st.metric("추정 MBTI", stats.get('final_mbti', 'N/A'))
                sentiment_dist = stats.get('sentiment_distribution', {})
                if sentiment_dist:
                    dominant_sentiment = max(sentiment_dist.keys(), key=lambda x: sentiment_dist[x])
                    st.metric("주요 감정", dominant_sentiment)
        
        # 도움말
        st.header("❓ 사용법")
        st.markdown("""
        1. **음성 입력**: 🎤 버튼을 클릭하여 5초간 음성 녹음
        2. **텍스트 입력**: 아래 입력창에 직접 타이핑
        3. **MBTI 분석**: 🧠 버튼으로 성격 분석
        4. **음성 재생**: 🔊 버튼으로 AI 응답 듣기
        """)
    
    # 메인 컨텐츠 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 대화하기")
        
        # 입력 방식 선택
        input_method = st.radio(
            "입력 방식을 선택하세요:",
            ["🎤 음성 입력", "⌨️ 텍스트 입력"],
            horizontal=True
        )
        
        user_input = None
        
        if input_method == "🎤 음성 입력":
            # 음성 입력 컨테이너
            with st.container():
                st.markdown('<div class="input-container">', unsafe_allow_html=True)
                st.markdown("**🎤 음성으로 대화하세요**")
                st.caption("버튼을 클릭하면 5초간 음성을 녹음합니다.")
                
                if st.button("🎤 음성 입력 시작", use_container_width=True, type="primary"):
                    user_input = process_voice_input()
                st.markdown('</div>', unsafe_allow_html=True)
                
        else:  # 텍스트 입력
            with st.container():
                st.markdown('<div class="input-container">', unsafe_allow_html=True)
                st.markdown("**⌨️ 텍스트로 대화하세요**")
                
                # 텍스트 입력 폼
                with st.form(key="text_input_form", clear_on_submit=True):
                    text_input = st.text_area(
                        "메시지를 입력하세요:",
                        placeholder="안녕하세요! 오늘 기분이 어떠세요?",
                        height=100
                    )
                    col_text1, col_text2 = st.columns([1, 4])
                    with col_text1:
                        submit_button = st.form_submit_button("💬 전송", use_container_width=True, type="primary")
                    with col_text2:
                        if submit_button and text_input.strip():
                            user_input = text_input.strip()
                st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.header("🛠️ 기능")
        
        # MBTI 분석 버튼
        if st.button("🧠 MBTI 분석", use_container_width=True):
            if st.session_state.conversation:
                last_user_input = next((msg for sender, msg in reversed(st.session_state.conversation) if sender == "User"), None)
                if last_user_input:
                    mbti = estimate_mbti(last_user_input)
                    sentiment = analyze_sentiment(last_user_input)
                    st.success(f"**추정된 MBTI**: {mbti}")
                    st.info(f"**감정 상태**: {sentiment}")
                else:
                    st.error("MBTI 분석을 위한 사용자 입력이 없습니다.")
            else:
                st.error("대화 기록이 없어 MBTI 분석을 할 수 없습니다.")
        
        # 대화 종료 버튼
        if st.button("🚪 대화 종료", use_container_width=True):
            db.end_session(st.session_state.session_id)
            st.session_state.conversation = []
            st.success("대화가 종료되었습니다.")
            time.sleep(1)
            st.rerun()
    
    # 사용자 입력 처리
    if user_input:
        if user_input.lower() in ["종료", "exit", "quit", "끝"]:
            st.write("대화를 종료합니다...")
            db.end_session(st.session_state.session_id)
            return
        
        # 대화 기록에 추가
        st.session_state.conversation.append(("User", user_input))
        
        # 감정 분석 및 MBTI 추정
        with st.spinner("� 생각하는 중..."):
            sentiment = analyze_sentiment(user_input)
            mbti = estimate_mbti(user_input)
            response = generate_response(user_input)
        
        st.session_state.conversation.append(("AI", response))
        
        # 데이터베이스에 저장
        db.save_conversation(
            session_id=st.session_state.session_id,
            user_input=user_input,
            ai_response=response,
            sentiment=sentiment,
            mbti=mbti
        )
        
        # 성공 메시지
        st.success("✅ 응답이 생성되었습니다!")
        
        # 자동 음성 재생 (설정이 활성화된 경우)
        if st.session_state.enable_speech:
            try:
                with st.spinner("🔊 음성 재생 중..."):
                    play_speech(response)
            except Exception as e:
                st.error(f"음성 재생 오류: {str(e)}")
        
        # 음성 재생 옵션
        col_audio1, col_audio2 = st.columns([1, 3])
        with col_audio1:
            if st.button("🔊 다시 재생"):
                if st.session_state.enable_speech:
                    play_speech(response)
                else:
                    st.warning("음성 출력이 비활성화되어 있습니다. 사이드바에서 활성화하세요.")
    
    # 대화 기록 표시
    st.header("📜 대화 기록")
    
    if st.session_state.conversation:
        # 최근 대화부터 표시 (역순)
        conversation_container = st.container()
        
        with conversation_container:
            for i, (sender, message) in enumerate(reversed(st.session_state.conversation[-config.MAX_CONVERSATION_HISTORY:])):
                if sender == "User":
                    st.markdown(f'<div class="user-message"><b>👤 사용자:</b><br>{message}</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="ai-message"><b>🤖 ENFP AI:</b><br>{message}</div>', 
                              unsafe_allow_html=True)
                
                # 구분선
                if i < len(st.session_state.conversation[-config.MAX_CONVERSATION_HISTORY:]) - 1:
                    st.markdown("---")
    else:
        st.info("💡 대화를 시작해보세요! 음성 또는 텍스트로 입력할 수 있습니다.")

if __name__ == "__main__":
    main()
    pygame.mixer.quit()