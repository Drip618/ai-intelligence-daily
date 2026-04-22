FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install playwright
RUN playwright install --with-deps chromium

# Copy application
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Environment variables
ENV PYTHONPATH=/app

# Default command: run once
CMD ["python", "-m", "src.core.agent", "--run-once"]
