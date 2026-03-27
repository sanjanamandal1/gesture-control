import pygetwindow as gw

# Define gesture mappings per app
APP_MODES = {
    "spotify": {
        "volume_up":    "volume_up",
        "volume_down":  "volume_down",
        "play_pause":   "play_pause",
        "next_slide":   "next_track",
        "scroll_up":    "prev_track",
        "scroll_down":  "play_pause",
    },
    "chrome": {
        "volume_up":    "scroll_up",
        "volume_down":  "scroll_down",
        "play_pause":   "play_pause",
        "next_slide":   "next_tab",
        "scroll_up":    "scroll_up",
        "scroll_down":  "scroll_down",
    },
    "powerpoint": {
        "volume_up":    "next_slide",
        "volume_down":  "prev_slide",
        "play_pause":   "play_pause",
        "next_slide":   "next_slide",
        "scroll_up":    "prev_slide",
        "scroll_down":  "next_slide",
    },
    "default": {
        "volume_up":    "volume_up",
        "volume_down":  "volume_down",
        "play_pause":   "play_pause",
        "next_slide":   "next_slide",
        "scroll_up":    "scroll_up",
        "scroll_down":  "scroll_down",
    }
}

def get_active_app():
    """Returns lowercase name of currently focused app."""
    try:
        win = gw.getActiveWindow()
        if win is None:
            return "default"
        title = win.title.lower()
        if "spotify" in title:
            return "spotify"
        elif "chrome" in title or "firefox" in title or "edge" in title:
            return "chrome"
        elif "powerpoint" in title:
            return "powerpoint"
        else:
            return "default"
    except Exception:
        return "default"

def get_mapped_action(gesture_name, app=None):
    """Returns the correct action for a gesture based on active app."""
    if app is None:
        app = get_active_app()
    mode = APP_MODES.get(app, APP_MODES["default"])
    return mode.get(gesture_name, gesture_name)