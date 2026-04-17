import time
from fastapi import HTTPException
from app.config import settings

# State quản lý chi phí hàng ngày (Trong production nên dùng Redis để bền vững)
_daily_cost = 0.0
_cost_reset_day = time.strftime("%Y-%m-%d")

def check_and_record_cost(input_tokens: int, output_tokens: int):
    """Theo dõi và giới hạn chi phí sử dụng hàng ngày."""
    global _daily_cost, _cost_reset_day
    today = time.strftime("%Y-%m-%d")
    
    # Reset ngân sách nếu sang ngày mới
    if today != _cost_reset_day:
        _daily_cost = 0.0
        _cost_reset_day = today
        
    if _daily_cost >= settings.daily_budget_usd:
        raise HTTPException(503, "Daily budget exhausted. Try tomorrow.")
        
    # Công thức tính cost giả định (dựa trên token)
    cost = (input_tokens / 1000) * 0.00015 + (output_tokens / 1000) * 0.0006
    _daily_cost += cost
    return _daily_cost

def get_current_cost():
    """Lấy chi phí đã sử dụng hiện tại."""
    return _daily_cost
