"""Hand tracking wrapper for Camera Mode."""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import mediapipe as mp


@dataclass(frozen=True)
class HandResult:
    """Single detected hand with pixel and normalized landmarks."""

    landmarks_px: list[tuple[int, int]]
    landmarks_norm: list[tuple[float, float, float]]
    handedness: str
    confidence: float


class HandTracker:
    def __init__(
        self,
        max_num_hands: int = 2,
        min_detection_confidence: float = 0.6,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self._mp_hands = mp.solutions.hands
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def detect(self, frame) -> list[HandResult]:
        """Detect hands in a BGR frame and return HandResult values."""
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._hands.process(frame_rgb)

        if not results.multi_hand_landmarks:
            return []

        frame_h, frame_w = frame.shape[:2]
        detections: list[HandResult] = []
        handedness_data = results.multi_handedness or []

        for index, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = "Unknown"
            confidence = 0.0
            if index < len(handedness_data):
                cls = handedness_data[index].classification[0]
                handedness = cls.label
                confidence = float(cls.score)

            landmarks_norm = [
                (lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark
            ]
            landmarks_px = [
                (int(lm.x * frame_w), int(lm.y * frame_h))
                for lm in hand_landmarks.landmark
            ]

            detections.append(
                HandResult(
                    landmarks_px=landmarks_px,
                    landmarks_norm=landmarks_norm,
                    handedness=handedness,
                    confidence=confidence,
                )
            )

        return detections

    def close(self) -> None:
        self._hands.close()
