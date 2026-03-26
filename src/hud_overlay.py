import cv2
import numpy as np

def draw_hud(frame, gesture_name, confidence, fps, finger_states):
    h, w = frame.shape[:2]
    overlay = frame.copy()

    # Semi-transparent top bar
    cv2.rectangle(overlay, (0, 0), (w, 70), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    # FPS
    cv2.putText(frame, f"FPS: {fps:.0f}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)

    # Gesture label + confidence bar
    if gesture_name:
        label = f"{gesture_name.replace('_', ' ').upper()}  {confidence*100:.0f}%"
        cv2.putText(frame, label, (10, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 220, 130), 2)
        bar_w = int(confidence * 200)
        cv2.rectangle(frame, (w-220, 10), (w-20, 30), (50, 50, 50), -1)
        cv2.rectangle(frame, (w-220, 10), (w-220+bar_w, 30), (80, 220, 130), -1)
    else:
        cv2.putText(frame, "No gesture", (10, 52),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (120, 120, 120), 1)

    # Finger state dots
    names   = ["T", "I", "M", "R", "P"]
    colors  = [(0,200,255), (0,255,120), (0,255,120), (0,255,120), (0,255,120)]
    for i, (name, state) in enumerate(zip(names, finger_states)):
        cx = w - 120 + i * 22
        color = colors[i] if state else (60, 60, 60)
        cv2.circle(frame, (cx, 52), 8, color, -1)
        cv2.putText(frame, name, (cx-5, 56),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

    return frame