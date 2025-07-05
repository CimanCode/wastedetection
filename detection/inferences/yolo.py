from ultralytics import YOLO
import cv2
import numpy as np
import os
from PIL import Image
import io

# Load YOLO model sekali
model_path = os.path.join(os.path.dirname(__file__), '../models/yolo_best.pt')
model = YOLO(model_path)

def predict_yolo_from_bytes(img_bytes):
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    original_size = image.size 

    # Resize image to model input (416x416)
    resized = image.resize((416, 416))
    results = model.predict(np.array(resized), imgsz=416, conf=0.3, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = model.names[cls]

            # Konversi koordinat bbox ke ukuran canvas (640x480)
            scale_x = 640 / 416
            scale_y = 480 / 416
            detections.append({
                "label": label,
                "confidence": conf,
                "bbox": [x1 * scale_x, y1 * scale_y, x2 * scale_x, y2 * scale_y]
            })

    return detections
def run_yolo(image_path: str, conf: float = 0.25):
    results = model(image_path, conf=conf)
    
    for i, result in enumerate(results):
        print(f"[YOLO DEBUG] Image {i} - {len(result.boxes)} boxes detected")
        for j, box in enumerate(result.boxes):
            cls = int(box.cls.cpu().numpy())
            conf_score = float(box.conf.cpu().numpy())
            print(f"  Box {j}: class={cls}, conf={conf_score}")
    
    return results

