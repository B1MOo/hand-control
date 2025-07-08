import cv2
import mediapipe as mp
from mouse_controller import MouseController
from mouse_clicks import MouseClicks
from shortcuts import GestureShortcuts  # Your copy/paste handler

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Setup webcam
cap = cv2.VideoCapture(0)

# Finger tip landmark indices
finger_tips = [4, 8, 12, 16, 20]

mouse = MouseController()
clicks = MouseClicks()
shortcuts = GestureShortcuts()

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)  # Mirror for natural movement
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    hand_results = {}
    landmark_map = {}

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            hand_type = handedness.classification[0].label  # "Left" or "Right"
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            landmark_map[hand_type] = landmarks

            finger_states = []

            # Thumb detection depends on hand side
            if hand_type == "Right":
                finger_states.append(1 if landmarks[4].x < landmarks[3].x else 0)
            else:
                finger_states.append(1 if landmarks[4].x > landmarks[3].x else 0)

            # Other fingers
            for tip in finger_tips[1:]:
                finger_states.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)

            hand_results[hand_type] = finger_states

    right_fingers = hand_results.get("Right", [])
    left_fingers = hand_results.get("Left", [])

    right_index_only = (right_fingers == [0, 1, 0, 0, 0])
    left_present = len(left_fingers) == 5
    right_present = len(right_fingers) == 5

    # Move mouse only if right index finger is up alone and left hand present
    if right_index_only and left_present:
        h, w, _ = img.shape
        right_landmarks = landmark_map.get("Right")
        if right_landmarks:
            index_tip = right_landmarks[8]
            x_px = int(index_tip.x * w)
            y_px = int(index_tip.y * h)
            mouse.move_cursor(x_px, y_px, w, h)

    # Run shortcuts anytime left hand is present
    if left_present:
        shortcuts.process_shortcut(left_fingers)

        # Run clicks only if right hand is also present
        if right_present:
            clicks.process_clicks(left_fingers)

    print(f"Left fingers: {left_fingers} | Right fingers: {right_fingers}")

    cv2.imshow("Hand Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
