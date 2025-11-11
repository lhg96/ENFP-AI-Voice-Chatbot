"""
Database module for storing conversation history and analysis results.
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import os

logger = logging.getLogger(__name__)

class ConversationDB:
    """Database handler for conversation history."""
    
    def __init__(self, db_path: str = "conversations.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Conversations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_input TEXT NOT NULL,
                        ai_response TEXT,
                        sentiment TEXT,
                        mbti TEXT,
                        confidence_score REAL
                    )
                ''')
                
                # Sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                        end_time DATETIME,
                        total_messages INTEGER DEFAULT 0,
                        avg_sentiment TEXT,
                        final_mbti TEXT
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
    
    def save_conversation(self, session_id: str, user_input: str, 
                         ai_response: str = None, sentiment: str = None, 
                         mbti: str = None, confidence_score: float = 0.0):
        """Save a conversation turn to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO conversations 
                    (session_id, user_input, ai_response, sentiment, mbti, confidence_score)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (session_id, user_input, ai_response, sentiment, mbti, confidence_score))
                
                # Update session stats
                cursor.execute('''
                    INSERT OR IGNORE INTO sessions (session_id, total_messages)
                    VALUES (?, 1)
                ''', (session_id,))
                
                cursor.execute('''
                    UPDATE sessions 
                    SET total_messages = total_messages + 1,
                        final_mbti = COALESCE(?, final_mbti)
                    WHERE session_id = ?
                ''', (mbti, session_id))
                
                conn.commit()
                logger.info(f"Conversation saved for session {session_id}")
                
        except Exception as e:
            logger.error(f"Failed to save conversation: {str(e)}")
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict]:
        """Get conversation history for a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT timestamp, user_input, ai_response, sentiment, mbti
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                ''', (session_id, limit))
                
                results = cursor.fetchall()
                
                conversations = []
                for row in results:
                    conversations.append({
                        'timestamp': row[0],
                        'user_input': row[1],
                        'ai_response': row[2],
                        'sentiment': row[3],
                        'mbti': row[4]
                    })
                
                return conversations[::-1]  # Reverse to get chronological order
                
        except Exception as e:
            logger.error(f"Failed to get conversation history: {str(e)}")
            return []
    
    def get_session_stats(self, session_id: str) -> Optional[Dict]:
        """Get statistics for a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Session basic stats
                cursor.execute('''
                    SELECT start_time, total_messages, final_mbti
                    FROM sessions
                    WHERE session_id = ?
                ''', (session_id,))
                
                session_data = cursor.fetchone()
                if not session_data:
                    return None
                
                # Sentiment distribution
                cursor.execute('''
                    SELECT sentiment, COUNT(*) as count
                    FROM conversations
                    WHERE session_id = ? AND sentiment IS NOT NULL
                    GROUP BY sentiment
                ''', (session_id,))
                
                sentiment_data = cursor.fetchall()
                
                stats = {
                    'session_id': session_id,
                    'start_time': session_data[0],
                    'total_messages': session_data[1],
                    'final_mbti': session_data[2],
                    'sentiment_distribution': dict(sentiment_data)
                }
                
                return stats
                
        except Exception as e:
            logger.error(f"Failed to get session stats: {str(e)}")
            return None
    
    def end_session(self, session_id: str):
        """Mark a session as ended."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    UPDATE sessions
                    SET end_time = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                ''', (session_id,))
                
                conn.commit()
                logger.info(f"Session {session_id} ended")
                
        except Exception as e:
            logger.error(f"Failed to end session: {str(e)}")
    
    def cleanup_old_sessions(self, days_old: int = 30):
        """Remove sessions older than specified days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    DELETE FROM conversations
                    WHERE session_id IN (
                        SELECT session_id FROM sessions
                        WHERE start_time < datetime('now', '-{} days')
                    )
                '''.format(days_old))
                
                cursor.execute('''
                    DELETE FROM sessions
                    WHERE start_time < datetime('now', '-{} days')
                '''.format(days_old))
                
                conn.commit()
                logger.info(f"Cleaned up sessions older than {days_old} days")
                
        except Exception as e:
            logger.error(f"Failed to cleanup old sessions: {str(e)}")
    
    def export_conversations(self, session_id: str = None, format: str = 'json') -> str:
        """Export conversations to JSON or CSV format."""
        try:
            conversations = []
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if session_id:
                    cursor.execute('''
                        SELECT * FROM conversations WHERE session_id = ?
                        ORDER BY timestamp
                    ''', (session_id,))
                else:
                    cursor.execute('''
                        SELECT * FROM conversations ORDER BY timestamp
                    ''')
                
                columns = [description[0] for description in cursor.description]
                for row in cursor.fetchall():
                    conversations.append(dict(zip(columns, row)))
            
            if format.lower() == 'json':
                return json.dumps(conversations, indent=2, default=str)
            elif format.lower() == 'csv':
                import csv
                import io
                
                output = io.StringIO()
                if conversations:
                    writer = csv.DictWriter(output, fieldnames=conversations[0].keys())
                    writer.writeheader()
                    writer.writerows(conversations)
                
                return output.getvalue()
            
        except Exception as e:
            logger.error(f"Failed to export conversations: {str(e)}")
            return ""