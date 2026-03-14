# WAIQ Knuckle - Deliberately vulnerable training app
FROM python:3.11-slim

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app (includes pre-built app/static/js from npm run build)
COPY app/ ./app/
COPY exploit_test.py .

# Create data dir for SQLite
RUN mkdir -p /app/data

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
ENV APP_PORT=5000

CMD ["python", "app/app.py"]
