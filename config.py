"""
Configuration settings for ENFP AI Voice Chatbot
"""

# Ollama API 설정
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "phi4:latest"
MAX_TOKENS = 100
TEMPERATURE = 0.7
TOP_K = 50
TOP_P = 0.95

# 음성 녹음 설정
VOICE_DURATION = 5  # seconds
VOICE_SAMPLE_RATE = 44100
VOICE_CHANNELS = 1

# 별칭 (호환성을 위해)
RECORDING_DURATION = VOICE_DURATION
SAMPLE_RATE = VOICE_SAMPLE_RATE
CHANNELS = VOICE_CHANNELS

# 모델 설정
MODEL_CACHE_SIZE = 128
SENTIMENT_MODEL = "beomi/KcELECTRA-base-v2022"

# 데이터베이스 설정
DATABASE_PATH = "conversations.db"

# 오디오 설정
AUDIO_CHUNK_SIZE = 1024
AUDIO_FORMAT = "WAV"

# ngrok 설정
NGROK_PORT = 8501

# 대화 기록 설정
MAX_CONVERSATION_HISTORY = 100

# 디버그 설정
DEBUG_MODE = False
LOG_LEVEL = "INFO"