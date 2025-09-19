"""
Simple Redis Queue Configuration for Financial Document Analyzer
"""

import os
import redis
from rq import Queue

# Redis connection configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Create Redis connection
try:
    redis_conn = redis.from_url(REDIS_URL)
    # Test connection
    redis_conn.ping()
    print("✅ Redis connection successful")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    print("⚠️ Using in-memory fallback (not recommended for production)")
    redis_conn = None

# Create RQ queue
if redis_conn:
    analysis_queue = Queue('analysis', connection=redis_conn)
else:
    analysis_queue = None

def get_queue():
    """Get the analysis queue"""
    return analysis_queue

def is_redis_available():
    """Check if Redis is available"""
    return redis_conn is not None
