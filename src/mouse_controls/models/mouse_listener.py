"""Mouse listener module for handling mouse events."""

from pynput.keyboard import Key, Listener

from mouse_controls.models.mouse import Mouse


class MouseListener:
    """Listener for mouse control events."""

    def __init__(self, mouse: Mouse) -> None:
        """Initialize the mouse listener with a Mouse instance.

        :param Mouse mouse:
            The Mouse instance to control.
        """
        self.mouse = mouse

    def start(self) -> None:
        """Start the keyboard listener for mouse control."""

        def on_press(key: Key) -> None:
            self.mouse.on_press(key, listener)

        with Listener(on_press=on_press) as listener:
            self.mouse.start()
            listener.join()
