# 🗑️ Waste Detection System with YOLO + Faster R-CNN (Django)

This project is a trash classification and detection system using YOLOv8 and Faster R-CNN, integrated into a Django web backend. It allows users to upload images of waste, which are then analyzed and classified into waste types such as:

- B3 (Hazardous)
- Elektronik
- Organik
- Anorganik

## 🚀 Features

- Fusion of YOLO and Faster R-CNN predictions
- User-based detection history
- Bounding box drawing and result image storage
- REST API for detection
- Admin interface
- Save and delete detection records
- Deployment ready

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/waste-detection-django.git
cd waste-detection-django

# Create and activate virtual environment
python -m venv env
# On Windows:
.\env\Scripts\activate
# On Unix/Mac:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```
