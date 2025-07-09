import os
import torch
import requests
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from functools import lru_cache

@lru_cache(maxsize=1)
def download_fasterrcnn_model():
    model_url = "https://huggingface.co/firmanabdlrhmn/fasterrcnn_model/resolve/main/fasterrcnn_best_model.pth"
    model_dir = os.path.join("models")
    model_path = os.path.join(model_dir, "fasterrcnn_best_model.pth")

    if not os.path.exists(model_path):
        os.makedirs(model_dir, exist_ok=True)
        print("Downloading model from Hugging Face...")
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")

    return model_path

@lru_cache(maxsize=1)
def download_yolo_model():
    model_url = "https://huggingface.co/firmanabdlrhmn/yolo_best_model/resolve/main/yolo_best.pt"
    model_dir = os.path.join("models")
    model_path = os.path.join(model_dir, "yolo_best.pt")

    if not os.path.exists(model_path):
        os.makedirs(model_dir, exist_ok=True)
        print("Downloading model from Hugging Face...")
        response = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(response.content)
        print("Download complete.")

    return model_path