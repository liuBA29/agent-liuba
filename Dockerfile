FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Minimal system deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Optional heavy deps toggle (OFF by default)
ARG WITH_EMBEDDINGS=false
ENV WITH_EMBEDDINGS=${WITH_EMBEDDINGS}

# Install python deps with cache-friendly layering
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Install heavy ML deps only when requested
COPY requirements-embeddings.txt ./
RUN if [ "$WITH_EMBEDDINGS" = "true" ]; then \
      pip install -r requirements-embeddings.txt; \
    else \
      echo "Skipping embeddings deps"; \
    fi

# Copy source
COPY src ./src

# Default run
CMD ["python", "src/main.py"]


