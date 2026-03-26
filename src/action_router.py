import pyautogui, time, platform

# Windows-only volume control
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
    HAS_VOLUME = True
except Exception:
    HAS_VOLUME = False

pyautogui.FAILSAFE = False
_last_action_time = {}
COOLDOWN = 0.8  # seconds between same action

def _can_fire(action_name):
    now = time.time()
    if now - _last_action_time.get(action_name, 0) > COOLDOWN:
        _last_action_time[action_name] = now
        return True
    return False

GESTURE_MAP = {
    "volume_up":    lambda: _volume_up(),
    "volume_down":  lambda: _volume_down(),
    "next_slide":   lambda: pyautogui.press("right"),
    "prev_slide":   lambda: pyautogui.press("left"),
    "play_pause":   lambda: pyautogui.press("space"),
    "screenshot":   lambda: pyautogui.hotkey("ctrl", "shift", "s"),
    "scroll_up":    lambda: pyautogui.scroll(5),
    "scroll_down":  lambda: pyautogui.scroll(-5),
}

def _volume_up():
    if HAS_VOLUME:
        vol = volume_ctrl.GetMasterVolumeLevelScalar()
        volume_ctrl.SetMasterVolumeLevelScalar(min(1.0, vol + 0.05), None)
    else:
        pyautogui.hotkey("volumeup")

def _volume_down():
    if HAS_VOLUME:
        vol = volume_ctrl.GetMasterVolumeLevelScalar()
        volume_ctrl.SetMasterVolumeLevelScalar(max(0.0, vol - 0.05), None)
    else:
        pyautogui.hotkey("volumedown")

def execute(gesture_name):
    if gesture_name in GESTURE_MAP and _can_fire(gesture_name):
        GESTURE_MAP[gesture_name]()
        return True
    return False