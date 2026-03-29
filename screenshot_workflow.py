"""Pearson study screenshot workflow helper for AutoMater.

This module provides a user-triggered screenshot session:
- one-time region selection
- hotkey-driven captures with sequential filenames
- timestamped session folders
- lightweight confirmation and session summary
"""

from __future__ import annotations

import json
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas

import keyboard
import mss
import mss.tools

try:
    import winsound
except ImportError:  # pragma: no cover - winsound is Windows-only
    winsound = None

CONFIG_PATH = Path("config.json")
DEFAULT_OUTPUT_ROOT = Path("captures") / "pearson_study"


@dataclass(frozen=True)
class CaptureConfig:
    capture_hotkey: str = "ctrl+shift+s"
    stop_hotkey: str = "ctrl+shift+e"
    output_root: Path = DEFAULT_OUTPUT_ROOT


@dataclass(frozen=True)
class CaptureRegion:
    left: int
    top: int
    width: int
    height: int


class PearsonScreenshotSession:
    def __init__(self, config: CaptureConfig) -> None:
        self.config = config
        self.region: CaptureRegion | None = None
        self.session_dir: Path | None = None
        self.capture_count = 0
        self._active = False
        self._lock = threading.Lock()

    def run(self) -> int:
        self.region = select_capture_region()
        if self.region is None:
            print("Screenshot session cancelled before region selection completed.")
            return 1

        self.session_dir = self._create_session_dir()
        self._active = True

        print("\nPearson screenshot session started")
        print(f"Region: left={self.region.left}, top={self.region.top}, width={self.region.width}, height={self.region.height}")
        print(f"Save folder: {self.session_dir}")
        print(f"Capture hotkey: {self.config.capture_hotkey}")
        print(f"End session hotkey: {self.config.stop_hotkey}")
        print("Use only on content you are allowed to capture.")

        keyboard.add_hotkey(self.config.capture_hotkey, self.capture)
        keyboard.add_hotkey(self.config.stop_hotkey, self.stop)

        try:
            while self._active:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
        finally:
            keyboard.unhook_all_hotkeys()

        print(f"Session ended. Captures saved: {self.capture_count}")
        if self.session_dir is not None:
            print(f"Session folder: {self.session_dir}")
        return 0

    def capture(self) -> None:
        if not self._active or self.region is None or self.session_dir is None:
            return

        with self._lock:
            self.capture_count += 1
            file_name = f"{self.capture_count:03d}.png"
            output_path = self.session_dir / file_name

            monitor = {
                "left": self.region.left,
                "top": self.region.top,
                "width": self.region.width,
                "height": self.region.height,
            }

            with mss.mss() as sct:
                shot = sct.grab(monitor)
                mss.tools.to_png(shot.rgb, shot.size, output=str(output_path))

            self._confirm_capture(output_path)

    def stop(self) -> None:
        self._active = False

    def _create_session_dir(self) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = self.config.output_root / f"session_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)
        return session_dir

    def _confirm_capture(self, output_path: Path) -> None:
        if winsound is not None:
            winsound.MessageBeep(winsound.MB_OK)
        print(f"Captured {output_path.name}")


def load_capture_config(config_path: Path = CONFIG_PATH) -> CaptureConfig:
    if not config_path.exists():
        return CaptureConfig()

    try:
        with config_path.open("r", encoding="utf-8") as file:
            raw_config = json.load(file)
    except (OSError, json.JSONDecodeError):
        return CaptureConfig()

    workflow = raw_config.get("screenshot_workflow", {})
    capture_hotkey = workflow.get("capture_hotkey", CaptureConfig.capture_hotkey)
    stop_hotkey = workflow.get("stop_hotkey", CaptureConfig.stop_hotkey)
    output_root = Path(workflow.get("output_root", str(DEFAULT_OUTPUT_ROOT)))

    return CaptureConfig(
        capture_hotkey=capture_hotkey,
        stop_hotkey=stop_hotkey,
        output_root=output_root,
    )


def select_capture_region() -> CaptureRegion | None:
    root = Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.25)
    root.config(cursor="crosshair")

    canvas = Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    state: dict[str, int | None] = {"start_x": None, "start_y": None, "rect_id": None}
    selected: dict[str, CaptureRegion | None] = {"region": None}

    def on_mouse_down(event) -> None:
        state["start_x"] = event.x
        state["start_y"] = event.y
        if state["rect_id"] is not None:
            canvas.delete(state["rect_id"])
        state["rect_id"] = canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="red", width=2)

    def on_mouse_drag(event) -> None:
        if state["rect_id"] is None or state["start_x"] is None or state["start_y"] is None:
            return
        canvas.coords(state["rect_id"], state["start_x"], state["start_y"], event.x, event.y)

    def on_mouse_up(event) -> None:
        if state["start_x"] is None or state["start_y"] is None:
            return

        x1, y1 = state["start_x"], state["start_y"]
        x2, y2 = event.x, event.y

        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        if width < 5 or height < 5:
            return

        selected["region"] = CaptureRegion(left=left, top=top, width=width, height=height)
        root.quit()

    def on_escape(_event) -> None:
        selected["region"] = None
        root.quit()

    canvas.create_text(
        20,
        20,
        anchor="nw",
        fill="white",
        text="Drag to select capture region. Release to confirm. Press ESC to cancel.",
        font=("Segoe UI", 14, "bold"),
    )

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)
    root.bind("<Escape>", on_escape)

    root.mainloop()
    root.destroy()

    return selected["region"]


def main() -> int:
    config = load_capture_config()
    session = PearsonScreenshotSession(config)
    return session.run()


if __name__ == "__main__":
    raise SystemExit(main())
