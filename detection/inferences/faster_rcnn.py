import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision import transforms as T
import os
from collections import defaultdict

# Mapping label string untuk masing-masing model
YOLO_LABEL_MAP = {
    0: "sampah-B3",
    1: "sampah-Elektronik",
    2: "sampah-anorganik",
    3: "sampah-organik",
}

FRCNN_LABEL_MAP = {
    1: "sampah-B3",
    2: "sampah-Elektronik",
    3: "sampah-anorganik",
    4: "sampah-organik",
}


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "../models/fasterrcnn_best_model.pth")
faster_rcnn = fasterrcnn_resnet50_fpn(pretrained=False, num_classes=5)
checkpoint = torch.load(model_path, map_location=device)
faster_rcnn.load_state_dict(checkpoint["model"])
faster_rcnn.eval().to(device)

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

def vote_fusion(yolo_box, yolo_conf, yolo_cls, pil_img):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Transform image once before passing to FRCNN
    tensor_img = transform(pil_img).to(device)
    frcnn_output = faster_rcnn([tensor_img])[0] 

    # Ambil prediksi dari output FRCNN
    frcnn_preds = []
    for label_id, score in zip(frcnn_output['labels'], frcnn_output['scores']):
        if score.item() > 0.3:
            frcnn_preds.append({
                "label": FRCNN_LABEL_MAP.get(label_id.item(), "unknown"),
                "score": score.item()
            })

    # Voting
    vote_counter = defaultdict(float)
    weight_sum = defaultdict(float)

    yolo_label = YOLO_LABEL_MAP.get(int(yolo_cls), "unknown")
    vote_counter[yolo_label] += yolo_conf
    weight_sum[yolo_label] += 1

    for pred in frcnn_preds:
        label = pred["label"]
        score = pred["score"]
        vote_counter[label] += score
        weight_sum[label] += 1

    final_label = max(vote_counter.items(), key=lambda x: x[1])[0]
    final_score = vote_counter[final_label] / weight_sum[final_label]

    return {
        "label": final_label,
        "score": final_score,
        "box": yolo_box.tolist()
    }






