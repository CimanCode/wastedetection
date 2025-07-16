# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgtk-3-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy project files
COPY . .

# Collect static (optional)
RUN python manage.py collectstatic --noinput || echo "skip collectstatic"

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
