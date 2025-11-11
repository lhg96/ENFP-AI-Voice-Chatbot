"""
Simple analyzer module for sentiment analysis and MBTI estimation
"""
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

# Initialize Korean sentiment analysis pipeline with error handling
try:
    sentiment_pipeline = pipeline(
        task="text-classification",
        model="beomi/KcELECTRA-base-v2022",
        tokenizer="beomi/KcELECTRA-base-v2022"
    )
    logger.info("Sentiment analysis model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load sentiment model: {str(e)}")
    sentiment_pipeline = None

def analyze_sentiment(text):
    """Analyze the sentiment of the given text."""
    try:
        if not text:
            return "분석할 텍스트가 없습니다"
        
        if sentiment_pipeline is None:
            return "감정 분석 모델이 로드되지 않았습니다"
        
        result = sentiment_pipeline(text)[0]
        label = result['label']
        
        # 한국어 결과로 변환
        if label == 'positive':
            return "긍정적"
        elif label == 'negative':
            return "부정적"
        else:
            return "중립"
            
    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        return f"감정 분석 실패: {str(e)}"

def estimate_mbti(text):
    """Estimate MBTI based on text input."""
    try:
        if not text:
            return "분석할 텍스트가 없습니다"

        # 한국어 키워드
        traits = {
            'E': ['우리', '함께', '만나다', '사람들', '대화', '활동', '밖에서', '모임', '친구', '파티'],
            'I': ['혼자', '조용히', '생각', '내면', '집중', '독서', '관찰', '개인적', '혼자만의'],
            'S': ['현재', '실제', '경험', '사실', '구체적', '현실적', '실천', '세부사항', '실용적'],
            'N': ['미래', '가능성', '상상', '아이디어', '직관', '영감', '창의', '추상적', '개념'],
            'T': ['분석', '논리', '객관적', '원칙', '효율', '합리적', '이성', '결과', '사실'],
            'F': ['감정', '공감', '조화', '가치', '배려', '이해', '느낌', '관계', '마음'],
            'J': ['계획', '체계', '정리', '결정', '목표', '기한', '완성', '규칙', '구조'],
            'P': ['유연', '적응', '자유', '탐색', '변화', '즉흥', '개방', '선택지', '유동적']
        }

        scores = {trait: 0 for trait in 'EISNTFJP'}
        words = text.split()
        
        # 키워드 매칭
        for trait, keywords in traits.items():
            for word in words:
                for keyword in keywords:
                    if keyword in word:
                        scores[trait] += 1

        # MBTI 구성
        mbti = ''
        mbti += 'E' if scores['E'] >= scores['I'] else 'I'
        mbti += 'S' if scores['S'] >= scores['N'] else 'N'
        mbti += 'T' if scores['T'] >= scores['F'] else 'F'
        mbti += 'J' if scores['J'] >= scores['P'] else 'P'

        return mbti

    except Exception as e:
        logger.error(f"MBTI estimation error: {str(e)}")
        return f"MBTI 추정 실패: {str(e)}"