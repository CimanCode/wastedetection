FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libgl1 \
    libglib2.0-0 \
    gfortran \
    libatlas-base-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

# Pisahkan installasi agar lebih mudah identifikasi error
RUN pip install Django==5.2.4
RUN pip install djangorestframework==3.16.0
RUN pip install gunicorn==23.0.0
RUN pip install psycopg2-binary==2.9.10
RUN pip install opencv-python-headless==4.11.0.86
RUN pip install torch==2.7.1 torchvision==0.22.1 --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "wastedetection.wsgi:application", "--bind", "0.0.0.0:8000"]
