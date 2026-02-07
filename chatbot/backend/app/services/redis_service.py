import redis
import json
import logging
from typing import List, Dict
from app.core.config import settings

logger = logging.getLogger("remo_ai")

class RedisMemoryService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        self.ttl = 3600  # 1 hour expiry
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for a session"""
        try:
            history = self.redis_client.lrange(f"chat:{session_id}", 0, -1)
            return [json.loads(msg) for msg in history]
        except Exception as e:
            logger.error(f"Failed to get chat history: {str(e)}")
            return []
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to chat history"""
        try:
            key = f"chat:{session_id}"
            message = json.dumps({"role": role, "content": content})
            self.redis_client.rpush(key, message)
            self.redis_client.expire(key, self.ttl)
            
            # Keep only last 10 messages
            self.redis_client.ltrim(key, -10, -1)
        except Exception as e:
            logger.error(f"Failed to add message: {str(e)}")
    
    def clear_history(self, session_id: str):
        """Clear chat history for a session"""
        try:
            self.redis_client.delete(f"chat:{session_id}")
        except Exception as e:
            logger.error(f"Failed to clear history: {str(e)}")

redis_service = RedisMemoryService()
