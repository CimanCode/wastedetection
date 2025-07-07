import os
import torch
import requests
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from functools import lru_cache

@lru_cache(maxsize=1)
def download_fasterrcnn_model():
    model_url = "https://github.com/CimanCode/wastedetection/releases/download/v1.0/fasterrcnn_best_model.pth"
    model_path = "detection/models/fasterrcnn_best_model.pth"

    if not os.path.exists(model_path):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        r = requests.get(model_url)
        with open(model_path, 'wb') as f:
            f.write(r.content)
    
    checkpoint = torch.load(model_path, map_location='cpu')
    model = fasterrcnn_resnet50_fpn(pretrained=False, num_classes=5)
    model.load_state_dict(checkpoint["model"])
    model.eval()
    return model
