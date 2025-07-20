# model_loader.py
import os
import requests
from functools import lru_cache

@lru_cache(maxsize=1)
def download_fasterrcnn_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "models")
    model_path = os.path.join(model_dir, "fasterrcnn_best_model.pth")

    if not os.path.exists(model_path):
        os.makedirs(model_dir, exist_ok=True)
        print("Downloading Faster R-CNN...")
        r = requests.get("https://huggingface.co/firmanabdlrhmn/fasterrcnn_model/resolve/main/fasterrcnn_best_model.pth")
        r.raise_for_status()
        with open(model_path, 'wb') as f:
            f.write(r.content)

    return model_path

@lru_cache(maxsize=1)
def download_yolo_model():
    model_url = "https://huggingface.co/firmanabdlrhmn/yolo_best_model/resolve/main/yolo_best.pt"
    model_dir = "models"
    model_path = os.path.join(model_dir, "yolo_best.pt")
    if not os.path.exists(model_path):
        os.makedirs(model_dir, exist_ok=True)
        print("Downloading YOLO...")
        r = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(r.content)
    return model_path
