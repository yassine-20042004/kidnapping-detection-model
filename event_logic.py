def check_kidnapping(action, car_detected, persons):

    suspicious_actions = [
        "fighting",
        "pushing",
        "dragging"
    ]

    if action in suspicious_actions and car_detected and len(persons) >= 2:
        return True

    return False