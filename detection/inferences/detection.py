# import os
# import uuid
# import io
# import time
# import numpy as np
# from PIL import Image, ImageDraw, ImageFont
# import torch
# from torchvision import transforms as T
# from torchvision.ops import nms
# from django.conf import settings
# from django.utils.timezone import now
# from .yolo import run_yolo  # Assume initialized YOLO model from your integration
# from .faster_rcnn import vote_fusion
# from torchvision.ops import batched_nms
# from api.models import TrashInfo, Detection, History
# from django.utils import timezone

# def detect_and_map(image_file, user=None):
#     start_time = time.time()
#     image_bytes = image_file.read()
#     pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     tmp_path = os.path.join(settings.MEDIA_ROOT, f"temp_{uuid.uuid4().hex}.jpg")
#     pil_img.save(tmp_path)

#     yolo_results = run_yolo(tmp_path, conf=0.25)
#     if not yolo_results or len(yolo_results) == 0:
#         return {
#             "detections": [], "count": 0, "average_confidence": 0,
#             "detection_speed": 0, "saved": False,
#             "image_url": None, "result_image_url": None
#         }

#     yolo_result = yolo_results[0]
#     boxes = yolo_result.boxes
#     if boxes is None or boxes.shape[0] == 0:
#         return {
#             "detections": [], "count": 0, "average_confidence": 0,
#             "detection_speed": 0, "saved": False,
#             "image_url": None, "result_image_url": None
#         }

#     yolo_boxes = yolo_result.boxes.xyxy.cpu().numpy()
#     yolo_confs = yolo_result.boxes.conf.cpu().numpy()
#     yolo_classes = yolo_result.boxes.cls.cpu().numpy()

#     combined_boxes, combined_labels, combined_scores = [], [], []

#     for box, conf, cls in zip(yolo_boxes, yolo_confs, yolo_classes):
#         voted_results = vote_fusion(box, conf, cls, pil_img)
#         if voted_results and voted_results["label"]:
#             combined_boxes.append([int(b) for b in box])
#             combined_labels.append(voted_results["label"])
#             combined_scores.append(voted_results["score"])


#     os.remove(tmp_path)

#     if combined_boxes:
#         import torch
#         boxes_tensor = torch.tensor(combined_boxes).float()
#         scores_tensor = torch.tensor(combined_scores).float()

#         label_to_idx = {label: i for i, label in enumerate(set(combined_labels))}
#         class_tensor = torch.tensor([label_to_idx[lbl] for lbl in combined_labels])

#         keep = batched_nms(boxes_tensor, scores_tensor, class_tensor, iou_threshold=0.7)

#         refined_boxes = [combined_boxes[i] for i in keep]
#         refined_labels = [combined_labels[i] for i in keep]
#         refined_scores = [combined_scores[i] for i in keep]
#     else:
#         refined_boxes, refined_labels, refined_scores = [], [], []

#     draw_img = pil_img.copy()
#     draw = ImageDraw.Draw(draw_img)
#     try:
#         font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
#     except:
#         font = ImageFont.load_default()

#     results = []
#     total_conf = 0
#     detection_time = now()

#     for label_str, conf, bbox in zip(refined_labels, refined_scores, refined_boxes):
#         try:
#             info = TrashInfo.objects.get(label=label_str)
#         except TrashInfo.DoesNotExist:
#             print(f"[WARNING] Label '{label_str}' tidak ditemukan di TrashInfo DB.")
#             continue

#         results.append({
#             "label": info.label,
#             "confidence": round(conf, 3),
#             "bbox": [round(b, 2) for b in bbox],
#             "danger_level": info.danger_level,
#             "description": info.description,
#             "mitigation": info.mitigation
#         })

#         draw.rectangle(bbox, outline="lime", width=3)
#         text = f"{info.label} ({conf:.2f})"
#         try:
#             bbox_text = font.getbbox(text)
#             text_width = bbox_text[2] - bbox_text[0]
#             text_height = bbox_text[3] - bbox_text[1]
#         except AttributeError:
#             text_width, text_height = font.getsize(text)

#         text_bg = [bbox[0], bbox[1] - text_height - 4, bbox[0] + text_width + 6, bbox[1]]
#         draw.rectangle(text_bg, fill="black")
#         draw.text((bbox[0] + 3, bbox[1] - text_height - 2), text, fill="lime", font=font)
#         total_conf += conf

#     image_path, result_image_path = None, None
#     if user and user.is_authenticated and results:
#         save_dir = os.path.join(settings.MEDIA_ROOT, "detections")
#         os.makedirs(save_dir, exist_ok=True)

#         unique_id = uuid.uuid4().hex
#         img_filename = f"{user.username}_{unique_id}.jpg"
#         result_filename = f"{user.username}_{unique_id}_result.jpg"

#         image_path = os.path.join("detections", img_filename)
#         result_image_path = os.path.join("detections", result_filename)

#         pil_img.save(os.path.join(settings.MEDIA_ROOT, image_path))
#         draw_img.save(os.path.join(settings.MEDIA_ROOT, result_image_path))

#         for det in results:
#             try:
#                 label_obj = TrashInfo.objects.get(label=det["label"])
#             except TrashInfo.DoesNotExist:
#                 print(f"[ERROR] Label '{det['label']}' hilang saat save ke DB. Dilewati.")
#                 continue
#             detection_obj = Detection.objects.create(
#                 user=user,
#                 label=label_obj,
#                 image_path=image_path,
#                 result_image_path=result_image_path,
#                 detection_time=detection_time,
#                 detection_speed=round(time.time() - start_time, 3),
#                 total_confidence=det["confidence"]
#             )

#             History.objects.create(
#                 user=user,
#                 detection=detection_obj,
#                 save_at=timezone.now()
#             )

#     return {
#         "detections": results,
#         "count": len(results),
#         "average_confidence": round(total_conf / len(results), 3) if results else 0,
#         "detection_speed": round(time.time() - start_time, 3),
#         "saved": bool(user and user.is_authenticated and results),
#         "image_url": settings.MEDIA_URL + image_path if image_path else None,
#         "result_image_url": settings.MEDIA_URL + result_image_path if result_image_path else None,
#     }

import os
import uuid
import io
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import torch
from torchvision.ops import batched_nms
from django.conf import settings
from django.utils.timezone import now
from api.models import TrashInfo, Detection, History
from .yolo import run_yolo
from .faster_rcnn import vote_fusion
from django.utils import timezone
from rest_framework.exceptions import ValidationError

ALLOWED_IMAGE_FORMATS = ['jpeg', 'jpg', 'png']

def validate_image_format(pil_img):
    if pil_img.format not in ALLOWED_IMAGE_FORMATS:
        raise ValidationError("File harus dalam format JPG, JPEG, atau PNG.")

def draw_detection(draw, bbox, label, conf, font):
    draw.rectangle(bbox, outline="lime", width=3)
    text = f"{label} ({conf:.2f})"
    try:
        bbox_text = font.getbbox(text)
        text_width = bbox_text[2] - bbox_text[0]
        text_height = bbox_text[3] - bbox_text[1]
    except AttributeError:
        text_width, text_height = font.getsize(text)

    text_bg = [bbox[0], bbox[1] - text_height - 4, bbox[0] + text_width + 6, bbox[1]]
    draw.rectangle(text_bg, fill="black")
    draw.text((bbox[0] + 3, bbox[1] - text_height - 2), text, fill="lime", font=font)

def detect_and_map(image_file, user=None):
    start_time = time.time()

    try:
        image_bytes = image_file.read()
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        validate_image_format(pil_img)
    except UnidentifiedImageError:
        raise ValidationError("File tidak dapat dibaca sebagai gambar.")
    except ValidationError as ve:
        raise ve
    except Exception as e:
        raise ValidationError(f"Gagal membuka gambar: {str(e)}")

    tmp_path = os.path.join(settings.MEDIA_ROOT, f"temp_{uuid.uuid4().hex}.jpg")
    pil_img.save(tmp_path)

    try:
        yolo_results = run_yolo(tmp_path, conf=0.25)
    except Exception as e:
        os.remove(tmp_path)
        raise ValidationError(f"YOLO inference gagal: {str(e)}")

    os.remove(tmp_path)

    if not yolo_results or not yolo_results[0].boxes:
        return {
            "detections": [],
            "count": 0,
            "average_confidence": 0,
            "detection_speed": round(time.time() - start_time, 3),
            "saved": False,
            "image_url": None,
            "result_image_url": None,
            "message": "Tidak ada objek terdeteksi."
        }

    yolo_result = yolo_results[0]
    boxes = yolo_result.boxes.xyxy.cpu().numpy()
    confs = yolo_result.boxes.conf.cpu().numpy()
    classes = yolo_result.boxes.cls.cpu().numpy()

    combined_boxes, combined_labels, combined_scores = [], [], []
    for box, conf, cls in zip(boxes, confs, classes):
        result = vote_fusion(box, conf, cls, pil_img)
        if result and result["label"]:
            combined_boxes.append([int(b) for b in box])
            combined_labels.append(result["label"])
            combined_scores.append(result["score"])

    if not combined_boxes:
        return {
            "detections": [],
            "count": 0,
            "average_confidence": 0,
            "detection_speed": round(time.time() - start_time, 3),
            "saved": False,
            "image_url": None,
            "result_image_url": None,
            "message": "Tidak ada objek terdeteksi setelah voting."
        }

    boxes_tensor = torch.tensor(combined_boxes).float()
    scores_tensor = torch.tensor(combined_scores).float()
    label_to_idx = {label: i for i, label in enumerate(set(combined_labels))}
    class_tensor = torch.tensor([label_to_idx[lbl] for lbl in combined_labels])
    keep = batched_nms(boxes_tensor, scores_tensor, class_tensor, iou_threshold=0.7)

    refined_boxes = [combined_boxes[i] for i in keep]
    refined_labels = [combined_labels[i] for i in keep]
    refined_scores = [combined_scores[i] for i in keep]

    draw_img = pil_img.copy()
    draw = ImageDraw.Draw(draw_img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except:
        font = ImageFont.load_default()

    results, total_conf, detection_time = [], 0, now()

    for label, conf, bbox in zip(refined_labels, refined_scores, refined_boxes):
        try:
            info = TrashInfo.objects.get(label=label)
        except TrashInfo.DoesNotExist:
            continue

        results.append({
            "label": info.label,
            "confidence": round(conf, 3),
            "bbox": [round(b, 2) for b in bbox],
            "danger_level": info.danger_level,
            "description": info.description,
            "mitigation": info.mitigation
        })

        draw_detection(draw, bbox, info.label, conf, font)
        total_conf += conf

    image_path, result_image_path = None, None
    if user and user.is_authenticated and results:
        save_dir = os.path.join(settings.MEDIA_ROOT, "detections")
        os.makedirs(save_dir, exist_ok=True)

        unique_id = uuid.uuid4().hex
        image_path = os.path.join("detections", f"{user.username}_{unique_id}.jpg")
        result_image_path = os.path.join("detections", f"{user.username}_{unique_id}_result.jpg")

        pil_img.save(os.path.join(settings.MEDIA_ROOT, image_path))
        draw_img.save(os.path.join(settings.MEDIA_ROOT, result_image_path))

        for det in results:
            try:
                label_obj = TrashInfo.objects.get(label=det["label"])
            except TrashInfo.DoesNotExist:
                continue
            detection = Detection.objects.create(
                user=user,
                label=label_obj,
                image_path=image_path,
                result_image_path=result_image_path,
                detection_time=detection_time,
                detection_speed=round(time.time() - start_time, 3),
                total_confidence=det["confidence"]
            )
            History.objects.create(user=user, detection=detection, save_at=timezone.now())

    return {
        "detections": results,
        "count": len(results),
        "average_confidence": round(total_conf / len(results), 3) if results else 0,
        "detection_speed": round(time.time() - start_time, 3),
        "saved": bool(user and user.is_authenticated and results),
        "image_url": settings.MEDIA_URL + image_path if image_path else None,
        "result_image_url": settings.MEDIA_URL + result_image_path if result_image_path else None,
        "message": "Deteksi berhasil." if results else "Tidak ada objek terdeteksi."
    }
