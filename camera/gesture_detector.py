"""Rule-based gesture detection for camera hand-tracking."""

from __future__ import annotations

from math import hypot

from .hand_tracker import HandResult


class GestureDetector:
    """Classifies a small, fixed set of gestures from hand landmarks."""

    def classify(self, hands: list[HandResult]) -> tuple[str, float]:
        if not hands:
            return "NONE", 0.0

        hand = max(hands, key=lambda h: h.confidence)
        landmarks = hand.landmarks_norm
        finger_state = self._finger_extended_state(hand)

        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        pinch_distance = hypot(thumb_tip[0] - index_tip[0], thumb_tip[1] - index_tip[1])

        # PINCH: thumb and index fingertips are very close together.
        if pinch_distance < 0.05:
            conf = max(0.0, min(1.0, 1.0 - (pinch_distance / 0.05)))
            return "PINCH", conf

        extended_count = sum(1 for is_extended in finger_state.values() if is_extended)

        # FIST: all fingers folded.
        if extended_count == 0:
            return "FIST", 0.85

        # POINT: only index finger extended.
        if finger_state["index"] and extended_count == 1:
            return "POINT", 0.9

        # OPEN_PALM: most/all fingers extended.
        if extended_count >= 4:
            return "OPEN_PALM", 0.88

        return "UNKNOWN", 0.4

    def _finger_extended_state(self, hand: HandResult) -> dict[str, bool]:
        lm = hand.landmarks_norm
        return {
            "thumb": self._thumb_extended(hand),
            "index": lm[8][1] < lm[6][1],
            "middle": lm[12][1] < lm[10][1],
            "ring": lm[16][1] < lm[14][1],
            "pinky": lm[20][1] < lm[18][1],
        }

    def _thumb_extended(self, hand: HandResult) -> bool:
        lm = hand.landmarks_norm
        tip_x = lm[4][0]
        ip_x = lm[3][0]

        if hand.handedness == "Right":
            return tip_x < ip_x
        if hand.handedness == "Left":
            return tip_x > ip_x

        return abs(tip_x - ip_x) > 0.03
