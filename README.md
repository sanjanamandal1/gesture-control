# Gesture Control Interface

Control your computer using hand gestures via webcam — no special hardware needed.

## Features
- Real-time hand tracking with MediaPipe (21 landmarks)
- Custom gesture trainer — record and train your own gestures
- System actions: volume, media playback, slides, scrolling
- Live HUD overlay with gesture name, confidence bar, finger states
- Confidence-gated actions (no false triggers)
- Two-hand support

## Demo gestures
| Gesture | Action |
|---|---|
| Thumbs up | Volume up |
| Thumbs down | Volume down |
| Open palm | Play / Pause |
| Swipe right | Next slide |
| Two fingers up | Screenshot |

## Setup
```bash
pip install -r requirements.txt
```

## Usage
```bash
# Record gestures (150 samples each)
python main.py --record volume_up

# Train model
python main.py --train

# Run
python main.py
```

## Tech stack
MediaPipe · OpenCV · scikit-learn · PyAutoGUI · pycaw

## Author
[@sanjanamandal1](https://github.com/sanjanamandal1)