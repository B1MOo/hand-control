import pyautogui

class MouseClicks:
    def __init__(self):
        self.state = "fist"
        self.action_done = False

    def process_clicks(self, finger_states):
        thumb, index, middle, ring, pinky = finger_states
        total_up = sum(finger_states)

        if total_up == 0:
            self.state = "fist"
            self.action_done = False
            return

        if self.state == "fist" and not self.action_done:
            # Only single-finger clicks here
            if index == 1 and total_up == 1:
                pyautogui.click(button='left')  # Left click
                self.state = "left_click"
                self.action_done = True
            elif thumb == 1 and total_up == 1:
                pyautogui.click(button='right')  # Right click
                self.state = "right_click"
                self.action_done = True
