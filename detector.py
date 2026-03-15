# detector.py
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_persons(frame):
    results = model(frame, classes=[0])  # only person
    boxes = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            boxes.append([x1, y1, x2, y2])
    return boxes

def classify_child(box, frame_height):
    x1, y1, x2, y2 = box
    height = y2 - y1
    # Simple heuristic: height smaller than 50% of frame = child
    if height < frame_height * 0.5:
        return True
    return False