import time
from collections import defaultdict, deque
from fastapi import HTTPException
from app.config import settings

# In-memory storage cho demo (trong production nên dùng Redis)
_rate_windows: dict[str, deque] = defaultdict(deque)

def check_rate_limit(key: str):
    """Kiểm tra giới hạn request của user (Sliding Window)."""
    now = time.time()
    window = _rate_windows[key]
    
    # Xóa các request cũ ngoài cửa sổ 60s
    while window and window[0] < now - 60:
        window.popleft()
        
    if len(window) >= settings.rate_limit_per_minute:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {settings.rate_limit_per_minute} req/min",
            headers={"Retry-After": "60"},
        )
        
    window.append(now)
