"""Main entry point for the mouse control application."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from pydantic import BaseModel, Field
from pynput.keyboard import Key

from mouse_controls.models.mouse import Mouse
from mouse_controls.models.mouse_listener import MouseListener

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="[%d-%m-%Y|%H:%M:%S]", level=logging.DEBUG)

LOCK_TOGGLE_BUTTON = Key.ctrl_r
EXIT_BUTTON = Key.end


class Config(BaseModel):
    """Configuration for mouse control."""

    pos_lims: tuple[tuple[int, int], tuple[int, int]] = Field(description="Position limits for the mouse.")
    pos_buffer: int = Field(description="Buffer around the position limits.")
    delay: float = Field(description="Delay between mouse actions.")

    @classmethod
    def from_json_file(cls, file_path: Path) -> Config:
        """Load configuration from a JSON file."""
        with file_path.open() as file:
            data = json.load(file)
        return cls(**data)


def main() -> None:
    """Start the mouse control thread."""
    config = Config.from_json_file(Path("config.json"))
    mouse = Mouse(
        pos_lims=config.pos_lims,
        pos_buffer=config.pos_buffer,
        delay=config.delay,
        lock_toggle_btn=LOCK_TOGGLE_BUTTON,
        exit_btn=EXIT_BUTTON,
    )

    listener = MouseListener(mouse)
    listener.start()
