# Gunakan image python non-slim
FROM python:3.11

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libmysqlclient-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# Buat direktori kerja
WORKDIR /app

# Salin requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke image
COPY . .

# Jalankan collectstatic saat build image
RUN python manage.py collectstatic --noinput || true

# Jalankan gunicorn saat container mulai
CMD gunicorn wastedetection.wsgi:application --bind 0.0.0.0:$PORT
