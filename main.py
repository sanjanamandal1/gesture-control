import cv2, time, sys
from src.hand_tracker import HandTracker
from src.gesture_classifier import GestureClassifier, record_gesture, train_model
from src.action_router import execute
from src.hud_overlay import draw_hud
from src.app_mode import get_active_app, get_mapped_action
from src.gif_recorder import GifRecorder

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
    prev_time       = time.time()
    samples         = 0
    countdown_start = time.time()
    recorder        = GifRecorder(fps=10, max_seconds=5)
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
                lm            = all_lm[0]
                finger_states = tracker.get_finger_states(lm)
                gesture, conf = classifier.predict(lm)
                if gesture:
                    active_app     = get_active_app()
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