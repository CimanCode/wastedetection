from ultralytics import YOLO
from PIL import Image
import numpy as np
import io
import os
from rest_framework.exceptions import APIException
from ..model_loader import download_yolo_model


model_path = download_yolo_model()
# Load YOLO model sekali
# model_path = os.path.join(os.path.dirname(__file__), '../models/yolo_best.pt')
model = YOLO(model_path)

def preprocess_image(img_bytes, input_size=(416, 416)):
    try:
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        resized = image.resize(input_size)
        return np.array(resized)
    except Exception as e:
        raise APIException(f"Image preprocessing error: {str(e)}")

def scale_bbox(bbox, input_size=(416, 416), output_size=(640, 480)):
    scale_x = output_size[0] / input_size[0]
    scale_y = output_size[1] / input_size[1]
    x1, y1, x2, y2 = bbox
    return [x1 * scale_x, y1 * scale_y, x2 * scale_x, y2 * scale_y]

def predict_yolo_from_bytes(img_bytes, conf_threshold=0.25, input_size=(416, 416), output_size=(640, 480)):
    try:
        image_np = preprocess_image(img_bytes, input_size)

        results = model.predict(image_np, imgsz=input_size[0], conf=conf_threshold, verbose=False)

        detections = []
        for result in results:
            for box in result.boxes:
                bbox = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                label = model.names[class_id]

                scaled = scale_bbox(bbox, input_size, output_size)

                detections.append({
                    "label": label,
                    "confidence": confidence,
                    "bbox": scaled
                })

        return detections

    except Exception as e:
        raise APIException(f"Prediction failed: {str(e)}")

def run_yolo(image_path: str, conf: float = 0.25):
    results = model(image_path, conf=conf)
    
    for i, result in enumerate(results):
        print(f"[YOLO DEBUG] Image {i} - {len(result.boxes)} boxes detected")
        for j, box in enumerate(result.boxes):
            cls = int(box.cls.cpu().numpy())
            conf_score = float(box.conf.cpu().numpy())
            print(f"  Box {j}: class={cls}, conf={conf_score}")
    
    return results

