import time

class TwoHandComboDetector:
    def __init__(self, combo_window=1.5):
        self.combo_window = combo_window  # seconds both hands must be held
        self.hand1_gesture = None
        self.hand2_gesture = None
        self.combo_start   = None

    def update(self, gestures):
        if len(gestures) < 2:
            self.hand1_gesture = None
            self.hand2_gesture = None
            self.combo_start   = None
            return None

        g1, g2 = sorted(gestures[:2])

        # New combo started
        if (g1, g2) != (self.hand1_gesture, self.hand2_gesture):
            self.hand1_gesture = g1
            self.hand2_gesture = g2
            self.combo_start   = time.time()
            return None

        # combo_start is guaranteed not None here
        if self.combo_start is not None and time.time() - self.combo_start >= self.combo_window:
            self.combo_start = time.time()
            return self._resolve(g1, g2)

        return None

    def _resolve(self, g1, g2):
        combos = {
            ("play_pause", "play_pause"): "lock_screen",
            ("scroll_down", "scroll_down"): "close_window",
            ("scroll_up",   "scroll_up"):   "minimize_all",
            ("volume_up",   "volume_up"):   "max_volume",
            ("volume_down", "volume_down"): "mute",
            ("next_slide",  "scroll_up"):   "next_tab",
            ("volume_up",   "volume_down"): "screenshot",
        }
        return combos.get((g1, g2), None)

    def get_progress(self):
        """Returns 0.0 to 1.0 progress toward combo trigger."""
        if self.combo_start is None:
            return 0.0
        return min(1.0, (time.time() - self.combo_start) / self.combo_window)
    