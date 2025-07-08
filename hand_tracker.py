import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=2, detection_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=max_num_hands, min_detection_confidence=detection_confidence)
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        return results

    def draw_hands(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
