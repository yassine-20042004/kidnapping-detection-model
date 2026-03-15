import imageio
import numpy as np
import cv2

from detector import detect_persons, classify_child
from tracker import update_tracker

reader = imageio.get_reader('video.mp4')

frame_count = 0
boxes = []

kidnapping_frames_remaining = 0
KIDNAPPING_DISPLAY_FRAMES = 30  

for frame in reader:
    frame_count += 1
    frame_np = np.array(frame)

    if frame_count % 3 == 0:
        boxes = detect_persons(frame_np)

    tracked = update_tracker(boxes, frame_np)

    child_detected = False
    adult_detected = False

    for obj in tracked:
        track_id = obj["id"]
        x1, y1, x2, y2 = obj["bbox"]

        cv2.rectangle(frame_np, (x1, y1), (x2, y2), (0,255,0), 2)

        cv2.putText(frame_np, f"ID {track_id}",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2)

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        if len(boxes) == 0:
            continue

        closest_box = min(
            boxes,
            key=lambda b: ((b[0]+b[2])/2 - cx)**2 + ((b[1]+b[3])/2 - cy)**2
        )

        is_child = classify_child(closest_box, frame_np.shape[0])

        if is_child:
            child_detected = True
        else:
            adult_detected = True

    if child_detected and adult_detected:
        kidnapping_frames_remaining = KIDNAPPING_DISPLAY_FRAMES
    
    if kidnapping_frames_remaining > 0:

        overlay = frame_np.copy()
        cv2.rectangle(overlay, (30, 30), (600, 80), (0, 0, 255), -1)
        cv2.addWeighted(overlay, 0.3, frame_np, 0.7, 0, frame_np)
        
        cv2.putText(frame_np,
                    "🚨 POSSIBLE KIDNAPPING DETECTED 🚨",
                    (50, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),  
                    3)
        
        cv2.putText(frame_np,
                    f"({kidnapping_frames_remaining})",
                    (550, 65),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2)
        
        kidnapping_frames_remaining -= 1  

    cv2.imshow("Kidnapping Detection", frame_np)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("Done processing video!")