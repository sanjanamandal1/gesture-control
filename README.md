# Gesture Control Interface

Control your computer in real-time using hand gestures via webcam — no special hardware needed.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.13-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)


## What it does
A real-time gesture recognition system that lets you control your PC using hand gestures captured from a standard webcam. It includes a custom gesture trainer so you can record and train your own gestures, app-aware mode switching that automatically remaps gestures based on which app is in focus, and two-hand combo gestures for power commands.

## Features
- Real-time hand tracking using MediaPipe (21 landmarks per hand)
- Custom gesture trainer — record and train your own gestures in minutes
- App-aware mode switching — gestures auto-remap for Spotify, Chrome, PowerPoint
- Two-hand combo gestures with visual charging bar
- Live HUD overlay showing gesture name, confidence, finger states and active mode
- Built-in demo GIF recorder (press G)
- Confidence-gated actions to prevent false triggers

## Gestures
| Gesture | Default action |
|---|---|
| Thumbs up | Volume up |
| Thumbs down | Volume down |
| Open palm | Play / Pause |
| Peace sign | Next slide |
| Spread fingers | Scroll up |
| Closed fist | Scroll down |

## Two-hand combos
Hold both hands in the same pose for 1.5 seconds to trigger:

| Left hand | Right hand | Action |
|---|---|---|
| Open palm | Open palm | Lock screen |
| Closed fist | Closed fist | Close window |
| Spread fingers | Spread fingers | Minimize all |
| Thumbs up | Thumbs up | Max volume |
| Thumbs down | Thumbs down | Mute |
| Thumbs up | Thumbs down | Screenshot |

## App-aware modes
Gestures automatically remap when these apps are in focus:

| App | Remapped gestures |
|---|---|
| Spotify | Next slide → Next track, Scroll up → Prev track |
| Chrome | Volume up/down → Scroll up/down, Next slide → Next tab |
| PowerPoint | Volume up/down → Next/Prev slide |

## Project structure
```
gesture-control/
├── src/
│   ├── hand_tracker.py        # MediaPipe hand landmark detection
│   ├── gesture_classifier.py  # Random Forest gesture classifier
│   ├── action_router.py       # Maps gestures to system actions
│   ├── hud_overlay.py         # Live HUD drawn on webcam feed
│   ├── app_mode.py            # App-aware gesture remapping
│   ├── two_hand_combos.py     # Two-hand combo detection
│   └── gif_recorder.py        # Built-in GIF recorder
├── data/gestures/             # Recorded gesture CSVs
├── models/                    # Trained model saved here
├── demos/                     # Recorded GIFs saved here
├── main.py                    # Entry point
└── requirements.txt
```

## Setup
```bash
git clone https://github.com/sanjanamandal1/gesture-control.git
cd gesture-control
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### 1. Record gestures
```bash
python main.py --record volume_up
python main.py --record volume_down
python main.py --record play_pause
python main.py --record next_slide
python main.py --record scroll_up
python main.py --record scroll_down
```

### 2. Train the model
```bash
python main.py --train
```

### 3. Run
```bash
python main.py
```

## Hotkeys
| Key | Action |
|---|---|
| G | Start / stop GIF recording |
| Q | Quit |

## How it works
1. Webcam captures frames at 1280x720
2. MediaPipe detects 21 hand landmarks per hand
3. Landmarks are flattened to a 63-float vector and passed to a Random Forest classifier
4. Predicted gesture is mapped to a system action via the action router
5. App-aware module checks the active window and remaps the action if needed
6. For two hands, combo detector checks if both gestures match a combo pattern for 1.5 seconds

## Tech stack
- MediaPipe — hand landmark detection
- OpenCV — camera feed and HUD overlay
- scikit-learn — Random Forest gesture classifier
- PyAutoGUI — keyboard and mouse control
- pycaw — Windows audio control
- pygetwindow — active window detection
- imageio — GIF recording

## Author
[@sanjanamandal1](https://github.com/sanjanamandal1)