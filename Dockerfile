# Base image ringan yang stabil
FROM python:3.11-slim-bullseye

# Set environment variabel untuk non-interaktif install
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Collect static files (optional - safe)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Gunicorn sebagai web server
CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
