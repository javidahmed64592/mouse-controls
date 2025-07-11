"""Main entry point for the mouse control application."""

import logging

from pynput.keyboard import Key

from mouse_controls.models.mouse import Mouse
from mouse_controls.models.mouse_listener import MouseListener

logging.basicConfig(format="%(asctime)s %(message)s", datefmt="[%d-%m-%Y|%I:%M:%S]", level=logging.DEBUG)

DELTA_TIME = 0.001
LOCK_TOGGLE_BUTTON = Key.ctrl_r
EXIT_BUTTON = Key.end


def main() -> None:
    """Start the mouse control thread."""
    mouse = Mouse(
        pos_lims=((0, 1920), (0, 1080)),
        pos_buffer=10,
        delay=DELTA_TIME,
        lock_toggle_btn=LOCK_TOGGLE_BUTTON,
        exit_btn=EXIT_BUTTON,
    )

    listener = MouseListener(mouse)
    listener.start()
