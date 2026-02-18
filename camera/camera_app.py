"""Standalone Camera Mode app with hand tracking and gesture stability."""

from __future__ import annotations

import sys
import time
from collections import Counter, deque

import cv2

from .cursor_controller import CursorController
from .gesture_detector import GestureDetector
from .hand_tracker import HandTracker

WINDOW_NAME = "AutoMater Camera Mode"
OVERLAY_ENABLED = True

# Stability settings
GESTURE_WINDOW_SIZE = 10
GESTURE_CONFIRM_THRESHOLD = 6
GESTURE_COOLDOWN_SECONDS = 0.5
FIST_LOCK_TOGGLE_COOLDOWN_SECONDS = 1.0

HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20),
)


def draw_landmarks(frame, hands) -> None:
    for hand in hands:
        for point in hand.landmarks_px:
            cv2.circle(frame, point, 3, (0, 255, 0), -1)
        for a, b in HAND_CONNECTIONS:
            cv2.line(frame, hand.landmarks_px[a], hand.landmarks_px[b], (255, 180, 0), 2)


def confirm_stable_gesture(
    history: deque[str],
    last_trigger_times: dict[str, float],
    now: float,
) -> str:
    if not history:
        return "NONE"

    counts = Counter(history)
    gesture, count = counts.most_common(1)[0]
    if gesture in {"NONE", "UNKNOWN"}:
        return "NONE"

    if count < GESTURE_CONFIRM_THRESHOLD:
        return "NONE"

    last_seen = last_trigger_times.get(gesture, 0.0)
    if now - last_seen < GESTURE_COOLDOWN_SECONDS:
        return "NONE"

    last_trigger_times[gesture] = now
    return gesture


def main() -> int:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(
            "Error: Could not open default camera (index 0). "
            "Check camera permissions and whether another app is using it.",
            file=sys.stderr,
        )
        return 1

    tracker = None
    detector = GestureDetector()
    cursor = CursorController()

    gesture_history: deque[str] = deque(maxlen=GESTURE_WINDOW_SIZE)
    last_trigger_times: dict[str, float] = {}
    confirmed_gesture = "NONE"
    raw_gesture = "NONE"
    raw_confidence = 0.0
    last_lock_toggle_time = 0.0

    fps = 0.0
    frame_counter = 0
    last_fps_time = time.monotonic()

    try:
        tracker = HandTracker()
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Error: Failed to read a frame from the camera.", file=sys.stderr)
                return 1

            frame_h, frame_w = frame.shape[:2]
            hands = tracker.detect(frame)
            draw_landmarks(frame, hands)

            raw_gesture, raw_confidence = detector.classify(hands)
            gesture_history.append(raw_gesture)

            now = time.monotonic()
            maybe_confirmed = confirm_stable_gesture(
                history=gesture_history,
                last_trigger_times=last_trigger_times,
                now=now,
            )
            if maybe_confirmed != "NONE":
                confirmed_gesture = maybe_confirmed

            if (
                maybe_confirmed == "FIST"
                and now - last_lock_toggle_time >= FIST_LOCK_TOGGLE_COOLDOWN_SECONDS
            ):
                cursor.toggle_locked()
                last_lock_toggle_time = now

            if hands:
                primary_hand = max(hands, key=lambda hand: hand.confidence)
                cursor.update(primary_hand, frame_w=frame_w, frame_h=frame_h)

            frame_counter += 1
            elapsed = now - last_fps_time
            if elapsed >= 1.0:
                fps = frame_counter / elapsed
                frame_counter = 0
                last_fps_time = now

            if OVERLAY_ENABLED:
                cv2.putText(
                    frame,
                    f"Raw: {raw_gesture} ({raw_confidence:.2f})",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2,
                )
                cv2.putText(
                    frame,
                    f"Confirmed: {confirmed_gesture}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 200, 0),
                    2,
                )
                cv2.putText(
                    frame,
                    f"FPS: {fps:.1f}",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )
                lock_text = "LOCKED" if cursor.locked else "UNLOCKED"
                lock_color = (0, 0, 255) if cursor.locked else (0, 255, 0)
                cv2.putText(
                    frame,
                    f"Cursor: {lock_text}",
                    (10, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    lock_color,
                    2,
                )

            cv2.imshow(WINDOW_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key in (27, ord("q"), ord("Q")):
                break

            if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
                break

        return 0
    except Exception as exc:
        print(f"Camera Mode crashed: {exc}", file=sys.stderr)
        return 1
    finally:
        if tracker is not None:
            tracker.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    raise SystemExit(main())
