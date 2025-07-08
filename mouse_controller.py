import pyautogui

class MouseController:
    def __init__(self, smoothing=0.2):
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x = 0
        self.prev_y = 0
        self.smoothing = smoothing  # 0..1, higher = smoother (slower)

        # Define active box as fraction of webcam frame (x_start, y_start, width, height)
        # For example, center 50% area: from 25% to 75% horizontally and vertically
        self.active_box = (0.25, 0.25, 0.5, 0.5)

    def move_cursor(self, x, y, frame_width, frame_height):
        box_x, box_y, box_w, box_h = self.active_box

        # Normalize x,y to [0..1]
        norm_x = x / frame_width
        norm_y = y / frame_height

        # Clamp coordinates to active box limits
        norm_x_clamped = min(max(norm_x, box_x), box_x + box_w)
        norm_y_clamped = min(max(norm_y, box_y), box_y + box_h)

        # Map clamped coords to [0..1] inside the box
        relative_x = (norm_x_clamped - box_x) / box_w
        relative_y = (norm_y_clamped - box_y) / box_h

        # Map relative coordinates to screen pixels
        target_x = relative_x * self.screen_width
        target_y = relative_y * self.screen_height

        # Smooth the movement
        smooth_x = self.prev_x * (1 - self.smoothing) + target_x * self.smoothing
        smooth_y = self.prev_y * (1 - self.smoothing) + target_y * self.smoothing

        self.prev_x, self.prev_y = smooth_x, smooth_y

        pyautogui.moveTo(int(smooth_x), int(smooth_y))
