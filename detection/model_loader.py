# model_loader.py
import os
import requests
from functools import lru_cache
from tqdm import tqdm

@lru_cache(maxsize=1)
def download_fasterrcnn_model():
    model_url = "https://huggingface.co/firmanabdlrhmn/fasterrcnn_model/resolve/main/fasterrcnn_best_model.pth"
    model_dir = "models"
    model_path = os.path.join(model_dir, "fasterrcnn_best_model.pth")

    if not os.path.exists(model_path):
        os.makedirs(model_dir, exist_ok=True)
        print("Downloading Faster R-CNN model...")

        response = requests.get(model_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024

        if response.status_code != 200:
            raise Exception(f"Download failed with status code {response.status_code}")

        with open(model_path, 'wb') as f, tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading') as bar:
            for data in response.iter_content(block_size):
                f.write(data)
                bar.update(len(data))

        print("Download complete.")
    else:
        print("Model already exists, skipping download.")

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
