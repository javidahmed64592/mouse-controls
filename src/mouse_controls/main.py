"""Main entry point for the mouse control application."""

from pynput.keyboard import Key, Listener

from mouse_controls.models.mouse import Mouse

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

    def on_press(key: Key) -> None:
        mouse.on_press(key, listener)

    mouse.start()
    with Listener(on_press=on_press) as listener:
        listener.join()
