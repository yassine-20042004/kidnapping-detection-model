# tracker.py
from deep_sort_realtime.deepsort_tracker import DeepSort

# Initialize tracker
tracker = DeepSort(
    max_age=30,
    n_init=3,
    max_cosine_distance=0.3
)

def update_tracker(person_boxes, frame=None):
    """
    person_boxes format:
    [[x1, y1, x2, y2], ...]
    """

    detections = []

    for box in person_boxes:
        x1, y1, x2, y2 = map(int, box)

        w = x2 - x1
        h = y2 - y1

        # DeepSORT expects [x, y, w, h]
        detections.append(([x1, y1, w, h], 1.0, "person"))

    tracks = tracker.update_tracks(detections, frame=frame)

    tracked_objects = []

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()

        tracked_objects.append({
            "id": track_id,
            "bbox": [int(l), int(t), int(r), int(b)]
        })

    return tracked_objects
