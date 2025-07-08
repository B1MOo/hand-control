import pyautogui

class GestureShortcuts:
    def __init__(self):
        self.last_action = None

    def process_shortcut(self, finger_states):
        # Reset when fist
        if sum(finger_states) == 0:
            self.last_action = None
            return

        if finger_states == [0, 1, 1, 0, 0] and self.last_action != "copy":
            pyautogui.hotkey("ctrl", "c")
            self.last_action = "copy"

        elif finger_states == [1, 1, 0, 0, 0] and self.last_action != "paste":
            pyautogui.hotkey("ctrl", "v")
            self.last_action = "paste"
