FROM python:3.11

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

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
