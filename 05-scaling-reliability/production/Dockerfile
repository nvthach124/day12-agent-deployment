FROM python:3.11-slim

WORKDIR /app

# Cài đặt các thư viện
COPY 02-docker/production/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt redis

# Copy toàn bộ code
COPY . .

# Set PYTHONPATH để code nhận diện được folder utils từ thư mục gốc
ENV PYTHONPATH=/app

# Chạy từ thư mục chứa app.py để uvicorn tìm thấy module "app"
WORKDIR /app/05-scaling-reliability/production
CMD ["python", "app.py"]
