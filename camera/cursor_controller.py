"""Mouse cursor control for Camera Mode hand tracking."""

from __future__ import annotations

from dataclasses import dataclass

import pyautogui

try:
    from pynput.mouse import Controller as PynputMouseController
except Exception:  # pragma: no cover - optional dependency at runtime
    PynputMouseController = None

# Cursor tuning constants
EMA_ALPHA = 0.3
DEADZONE_PIXELS = 8
SPEED_SCALE = 1.0

INDEX_TIP_ID = 8
PALM_CENTER_IDS = (0, 5, 9, 13, 17)


@dataclass
class _Point:
    x: float
    y: float


class CursorController:
    """Maps hand landmarks to smooth system cursor movement."""

    def __init__(self) -> None:
        self._locked = False
        self._prev_smoothed: _Point | None = None

        self._screen_width, self._screen_height = self._get_screen_size()

        self._mouse = PynputMouseController() if PynputMouseController else None

    @property
    def locked(self) -> bool:
        return self._locked

    def set_locked(self, value: bool) -> None:
        self._locked = bool(value)

    def toggle_locked(self) -> bool:
        self._locked = not self._locked
        return self._locked

    def update(self, hand_result, frame_w: int, frame_h: int) -> None:
        if self._locked:
            return

        control_point = self._get_control_point(hand_result)
        if control_point is None or frame_w <= 0 or frame_h <= 0:
            return

        target = self._map_to_screen(control_point, frame_w=frame_w, frame_h=frame_h)

        if self._prev_smoothed is None:
            self._prev_smoothed = target
            self._move_cursor(target)
            return

        delta_x = target.x - self._prev_smoothed.x
        delta_y = target.y - self._prev_smoothed.y
        if abs(delta_x) < DEADZONE_PIXELS and abs(delta_y) < DEADZONE_PIXELS:
            return

        smoothed = _Point(
            x=(EMA_ALPHA * target.x) + ((1.0 - EMA_ALPHA) * self._prev_smoothed.x),
            y=(EMA_ALPHA * target.y) + ((1.0 - EMA_ALPHA) * self._prev_smoothed.y),
        )
        self._prev_smoothed = smoothed
        self._move_cursor(smoothed)

    def _get_control_point(self, hand_result) -> _Point | None:
        landmarks = getattr(hand_result, "landmarks_px", None)
        if not landmarks:
            return None

        if len(landmarks) > INDEX_TIP_ID:
            tip_x, tip_y = landmarks[INDEX_TIP_ID]
            return _Point(float(tip_x), float(tip_y))

        palm_points = [landmarks[i] for i in PALM_CENTER_IDS if i < len(landmarks)]
        if not palm_points:
            return None

        avg_x = sum(pt[0] for pt in palm_points) / len(palm_points)
        avg_y = sum(pt[1] for pt in palm_points) / len(palm_points)
        return _Point(avg_x, avg_y)

    def _map_to_screen(self, point: _Point, frame_w: int, frame_h: int) -> _Point:
        normalized_x = min(max(point.x / frame_w, 0.0), 1.0)
        normalized_y = min(max(point.y / frame_h, 0.0), 1.0)

        mirrored_x = 1.0 - normalized_x

        mapped_x = mirrored_x * self._screen_width * SPEED_SCALE
        mapped_y = normalized_y * self._screen_height * SPEED_SCALE

        clamped_x = min(max(mapped_x, 0.0), float(self._screen_width - 1))
        clamped_y = min(max(mapped_y, 0.0), float(self._screen_height - 1))
        return _Point(clamped_x, clamped_y)

    def _move_cursor(self, point: _Point) -> None:
        x, y = int(point.x), int(point.y)
        if self._mouse is not None:
            self._mouse.position = (x, y)
            return

        pyautogui.moveTo(x, y)

    def _get_screen_size(self) -> tuple[int, int]:
        try:
            size = pyautogui.size()
            return int(size.width), int(size.height)
        except Exception:
            return 1920, 1080
