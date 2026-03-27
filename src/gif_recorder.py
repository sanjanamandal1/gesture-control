import imageio
import numpy as np
import cv2
import time
import os

os.makedirs("demos", exist_ok=True)

class GifRecorder:
    def __init__(self, fps=10, max_seconds=5):
        self.fps         = fps
        self.max_frames  = fps * max_seconds
        self.frames      = []
        self.recording   = False
        self.last_capture = time.time()

    def toggle(self):
        if self.recording:
            self.stop()
        else:
            self.start()

    def start(self):
        self.frames    = []
        self.recording = True
        print("GIF recording started...")

    def stop(self):
        self.recording = False
        if self.frames:
            self._save()
        self.frames = []

    def capture(self, frame):
        """Call every loop iteration — only captures at target FPS."""
        if not self.recording:
            return
        now = time.time()
        if now - self.last_capture < 1.0 / self.fps:
            return
        self.last_capture = now

        # Resize to keep GIF small
        small = cv2.resize(frame, (480, 360))
        rgb   = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
        self.frames.append(rgb)

        if len(self.frames) >= self.max_frames:
            self.stop()

    def _save(self):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        path      = f"demos/gesture_demo_{timestamp}.gif"
        imageio.mimsave(path, self.frames, fps=self.fps)
        print(f"GIF saved to {path}")

    def is_recording(self):
        return self.recording

    def frame_count(self):
        return len(self.frames)

    def max_frames_count(self):
        return self.max_frames