"""Mouse control module for locking the mouse position within specified limits."""

import logging
import threading
import time

import numpy as np
from pynput.keyboard import Key, Listener
from pynput.mouse import Controller

logger = logging.getLogger(__name__)


class Mouse(threading.Thread):
    """Threaded mouse controller that locks the mouse position to a specific area."""

    def __init__(
        self,
        pos_lims: tuple[tuple[int, int], tuple[int, int]],
        pos_buffer: int,
        delay: float,
        lock_toggle_btn: Key,
        exit_btn: Key,
    ) -> None:
        """Initialize the mouse controller with position limits, delay, and control keys.

        :param tuple[tuple[int, int], tuple[int, int]] pos_lims:
            Position limits for the mouse.
        :param int pos_buffer:
            Buffer zone around the position limits.
        :param float delay:
            Delay between position updates.
        :param Key lock_toggle_btn:
            Keyboard key to toggle mouse locking.
        :param Key exit_btn:
            Keyboard key to exit the program.
        """
        super().__init__()
        self._pos_lims = pos_lims
        self._pos_buffer = pos_buffer
        self._delay = delay
        self._lock_toggle_btn = lock_toggle_btn
        self._exit_btn = exit_btn

        self._mouse = Controller()
        self._mouse_locked = False
        self._running = True

    def toggle_mouse_lock(self) -> None:
        """Toggle the mouse lock state."""
        self._mouse_locked = not self._mouse_locked
        logger.info(
            "Mouse lock toggled. Current state: %s",
            "Locked" if self._mouse_locked else "Unlocked",
        )

    def exit(self) -> None:
        """Unlock the mouse and stop the thread."""
        logger.info("Attempting to shut down...")
        self._mouse_locked = False
        self._running = False

    def on_press(self, key: Key, listener: Listener) -> None:
        """Handle key press events to toggle mouse lock or exit the program.

        :param Key key:
            The key that was pressed.
        :param Listener listener:
            The keyboard listener instance.
        """
        if key == self._lock_toggle_btn:
            self.toggle_mouse_lock()
        elif key == self._exit_btn:
            self.exit()
            listener.stop()

    def run(self) -> None:
        """Run the mouse control thread."""
        logger.info("Mouse control thread started.")
        while self._running:
            if self._mouse_locked:
                x = np.clip(
                    self._mouse.position[0],
                    self._pos_lims[0][0] + self._pos_buffer,
                    self._pos_lims[0][1] - self._pos_buffer,
                )
                y = np.clip(
                    self._mouse.position[1],
                    self._pos_lims[1][0] + self._pos_buffer,
                    self._pos_lims[1][1] - self._pos_buffer,
                )
                self._mouse.position = (x, y)
            time.sleep(self._delay)
