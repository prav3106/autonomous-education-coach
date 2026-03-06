import time
from collections import deque

# Store the last 200 logs in memory
LOG_CACHE = deque(maxlen=200)

def log_agent(agent_name: str, message: str):
    """
    Appends a log to the in-memory cache.
    """
    log_entry = {
        "timestamp": time.time(),
        "agent": agent_name,
        "payload": message
    }
    LOG_CACHE.append(log_entry)

def get_logs(since: float = 0):
    """
    Returns all logs that occurred after the `since` timestamp.
    """
    return [log for log in LOG_CACHE if log["timestamp"] > since]
