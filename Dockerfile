# Gunakan Python base image yang ringan
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies OS
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Salin dependensi dan install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Salin seluruh project
COPY . .

# Jalankan collectstatic (kalau perlu)
RUN python manage.py collectstatic --noinput || echo "skip collectstatic"

# Buka port
EXPOSE 8000

# Jalankan server menggunakan Gunicorn
CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
