# Gunakan image dasar Python
FROM python:3.10-slim

# Install system dependencies (penting untuk opencv, torch, dsb)
RUN apt-get update && apt-get install -y \
    gcc \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Atur direktori kerja
WORKDIR /app

# Salin file
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Jalankan server menggunakan gunicorn
CMD gunicorn wastedetection.wsgi:application --bind 0.0.0.0:$PORT
