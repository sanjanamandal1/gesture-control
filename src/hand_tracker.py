import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import landmark_pb2

class HandTracker:
    def __init__(self, max_hands=2, detection_confidence=0.75, tracking_confidence=0.75):
        self.mp_hands = mp.solutions.hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_connections = mp.solutions.hands.HAND_CONNECTIONS

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(rgb)
        all_landmarks = []

        if results.multi_hand_landmarks:
            for hand_lm in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_lm, self.mp_connections
                )
                lm_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_lm.landmark]).flatten()
                all_landmarks.append(lm_array)

        return frame, all_landmarks

    def get_finger_states(self, landmarks):
        if len(landmarks) == 0:
            return []
        lm = landmarks.reshape(21, 3)
        tips = [4, 8, 12, 16, 20]
        pip  = [3, 6, 10, 14, 18]
        states = []
        states.append(lm[tips[0]][0] < lm[pip[0]][0])
        for i in range(1, 5):
            states.append(lm[tips[i]][1] < lm[pip[i]][1])
        return states