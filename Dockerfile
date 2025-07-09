FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS-level dependencies
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

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Gunakan whitenoise jika collectstatic butuh
RUN python manage.py collectstatic --noinput || echo "Collectstatic failed (skip in dev)"

# Expose port for Gunicorn
EXPOSE 8000

# Start server
CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]