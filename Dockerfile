# Gunakan image slim yang ringan dan stabil
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Salin dependency dan install requirements
COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-utils \
    curl \
    gcc \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libmysqlclient-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install -r requirements.txt

# Salin semua file project
COPY . .

# Jalankan app
CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
