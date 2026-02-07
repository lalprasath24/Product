import redis
import json
import logging
from datetime import datetime, date
from app.core.config import settings

logger = logging.getLogger("remo_ai")

class TokenTrackingService:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=1,  # Different DB for token tracking
            decode_responses=True
        )
    
    def track_tokens(self, input_tokens: int, output_tokens: int):
        """Track token usage for today and current month"""
        try:
            today = date.today().isoformat()
            month = today[:7]  # YYYY-MM format
            
            # Daily tracking
            daily_key = f"tokens:daily:{today}"
            self.redis_client.hincrby(daily_key, "input", input_tokens)
            self.redis_client.hincrby(daily_key, "output", output_tokens)
            self.redis_client.expire(daily_key, 86400 * 32)  # 32 days
            
            # Monthly tracking
            monthly_key = f"tokens:monthly:{month}"
            self.redis_client.hincrby(monthly_key, "input", input_tokens)
            self.redis_client.hincrby(monthly_key, "output", output_tokens)
            self.redis_client.expire(monthly_key, 86400 * 365)  # 1 year
            
        except Exception as e:
            logger.error(f"Failed to track tokens: {str(e)}")
    
    def get_usage_stats(self):
        """Get today and monthly token usage"""
        try:
            today = date.today().isoformat()
            month = today[:7]
            
            daily_key = f"tokens:daily:{today}"
            monthly_key = f"tokens:monthly:{month}"
            
            daily_stats = self.redis_client.hgetall(daily_key)
            monthly_stats = self.redis_client.hgetall(monthly_key)
            
            return {
                "today": {
                    "input": int(daily_stats.get("input", 0)),
                    "output": int(daily_stats.get("output", 0)),
                    "total": int(daily_stats.get("input", 0)) + int(daily_stats.get("output", 0))
                },
                "monthly": {
                    "input": int(monthly_stats.get("input", 0)),
                    "output": int(monthly_stats.get("output", 0)),
                    "total": int(monthly_stats.get("input", 0)) + int(monthly_stats.get("output", 0))
                }
            }
        except Exception as e:
            logger.error(f"Failed to get usage stats: {str(e)}")
            return {"today": {"input": 0, "output": 0, "total": 0}, "monthly": {"input": 0, "output": 0, "total": 0}}

token_tracker = TokenTrackingService()