FROM python:3.11-slim

# System deps (optional but handy: curl for debugging, build deps for some wheels)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps first (leverage layer caching)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src ./src

# Default envs (can be overridden by docker-compose or -e)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Run the bot
CMD ["python", "src/main.py"]


