FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    libmysqlclient-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip dan wheel
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Gunicorn sebagai web server
CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
