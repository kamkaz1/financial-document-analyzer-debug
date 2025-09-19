"""
Simple Redis Queue Worker for Financial Document Analyzer
"""

from queue_config import get_queue, is_redis_available

def start_worker():
    """Start the Redis queue worker"""
    if not is_redis_available():
        print("❌ Redis is not available. Cannot start worker.")
        return
    
    queue = get_queue()
    print("🚀 Starting Redis queue worker...")
    print("📋 Queue: analysis")
    print("⏳ Waiting for jobs...")
    
    # Start worker
    worker = queue.worker()
    worker.work()

if __name__ == "__main__":
    start_worker()
