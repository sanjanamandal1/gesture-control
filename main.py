import warnings
warnings.filterwarnings("ignore")
import cv2, time, sys
from src.hand_tracker import HandTracker
from src.gesture_classifier import GestureClassifier, record_gesture, train_model
from src.action_router import execute
from src.hud_overlay import draw_hud
from src.app_mode import get_active_app, get_mapped_action
from src.gif_recorder import GifRecorder
from src.two_hand_combos import TwoHandComboDetector

RECORD_MODE    = "--record" in sys.argv
TRAIN_MODE     = "--train"  in sys.argv
GESTURE_LABEL  = sys.argv[2] if RECORD_MODE and len(sys.argv) > 2 else "gesture"
SAMPLES_NEEDED = 200

def main():
    if TRAIN_MODE:
        train_model()
        return

    tracker         = HandTracker()
    classifier      = GestureClassifier()
    cap             = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cv2.namedWindow("Gesture Control", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gesture Control", 1280, 720)
    prev_time       = time.time()
    samples         = 0
    countdown_start = time.time()
    recorder        = GifRecorder(fps=10, max_seconds=5)
    combo_detector  = TwoHandComboDetector(combo_window=1.5)
    COUNTDOWN       = 3

    if RECORD_MODE:
        print(f"Recording gesture: '{GESTURE_LABEL}' — get ready, positioning in 3 seconds!")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Camera read failed!")
            break

        frame    = cv2.flip(frame, 1)
        frame, all_lm = tracker.process(frame)
        elapsed  = time.time() - countdown_start
        gesture, conf = None, 0.0
        finger_states = []

        if RECORD_MODE:
            if elapsed < COUNTDOWN:
                remaining = int(COUNTDOWN - elapsed) + 1
                cv2.putText(frame, f"Get ready... {remaining}",
                            (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 140, 255), 3)
            elif all_lm:
                if samples < SAMPLES_NEEDED:
                    samples = record_gesture(GESTURE_LABEL, all_lm[0], samples)
                    cv2.putText(frame, f"Recording... {samples}/{SAMPLES_NEEDED}",
                                (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 140, 255), 2)
                else:
                    cv2.putText(frame, "Done! Press Q to quit.",
                                (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (80, 220, 130), 2)
            else:
                cv2.putText(frame, f"No hand detected! {samples}/{SAMPLES_NEEDED}",
                            (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        else:
            if all_lm:
                # Single hand
                lm            = all_lm[0]
                finger_states = tracker.get_finger_states(lm)
                gesture, conf = classifier.predict(lm)

                # Two hand combo detection
                if len(all_lm) == 2:
                    g1, c1 = classifier.predict(all_lm[0])
                    g2, c2 = classifier.predict(all_lm[1])
                    
                    # Use lower threshold for combos
                    COMBO_THRESHOLD = 0.35
                    g1 = g1 if c1 >= COMBO_THRESHOLD else None
                    g2 = g2 if c2 >= COMBO_THRESHOLD else None
                    
                    
                    detected = [g for g in [g1, g2] if g]
                    combo = combo_detector.update(detected)
                    if combo:
                        execute(combo, bypass_cooldown=True)
                        cv2.putText(frame, f"COMBO: {combo.replace('_',' ').upper()}!",
                                    (10, 210), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 200), 2)
                    # Show combo progress bar
                    progress = combo_detector.get_progress()
                    if progress > 0:
                        bar_w = int(progress * 200)
                        cv2.rectangle(frame, (10, 170), (210, 188), (50, 50, 50), -1)
                        cv2.rectangle(frame, (10, 170), (10 + bar_w, 188), (255, 100, 0), -1)
                        cv2.putText(frame, "Combo charging...",
                                    (10, 165), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5, (255, 100, 0), 1)
                    if combo:
                        execute(combo)
                        cv2.putText(frame, f"COMBO: {combo.replace('_',' ').upper()}!",
                                    (10, 210), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.8, (0, 255, 200), 2)
                else:
                    combo_detector.update([])

                if gesture and len(all_lm) == 1:
                    active_app    = get_active_app()
                    mapped_action = get_mapped_action(gesture, active_app)
                    execute(gesture, mapped_action)
                    cv2.putText(frame, f"Mode: {active_app}",
                                (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (255, 200, 0), 2)

        fps       = 1.0 / max(time.time() - prev_time, 1e-5)
        prev_time = time.time()
        frame     = draw_hud(frame, gesture, conf, fps, finger_states)

        # GIF recording overlay
        if recorder.is_recording():
            remaining = recorder.max_frames_count() - recorder.frame_count()
            secs_left = remaining // recorder.fps
            cv2.putText(frame, f"REC {secs_left}s",
                        (10, 160), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 255), 2)
            cv2.circle(frame, (200, 155), 8, (0, 0, 255), -1)

        recorder.capture(frame)

        display_frame = cv2.resize(frame, (1280, 720))
        cv2.imshow("Gesture Control", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("g"):
            recorder.toggle()
            if recorder.is_recording():
                print("Recording GIF — perform your gestures!")
            else:
                print("GIF recording stopped.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()