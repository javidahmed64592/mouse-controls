"""Mock implementation of pynput for testing on headless systems."""

import sys
from collections.abc import Callable
from types import TracebackType


class MockKey:
    """Mock implementation of pynput.keyboard.Key."""

    # Key constants
    ctrl_r = "ctrl_r"
    end = "end"

    def __init__(self, name: str) -> None:
        """Initialize mock key with a name."""
        self.name = name

    def __str__(self) -> str:
        """Return string representation of the key."""
        return self.name

    def __repr__(self) -> str:
        """Return string representation of the key."""
        return f"MockKey({self.name})"


class MockListener:
    """Mock implementation of pynput.keyboard.Listener."""

    def __init__(self, on_press: Callable | None = None, on_release: Callable | None = None) -> None:
        """Initialize mock listener."""
        self.on_press = on_press
        self.on_release = on_release
        self._is_running = False

    def start(self) -> None:
        """Start the listener."""
        self._is_running = True

    def stop(self) -> None:
        """Stop the listener."""
        self._is_running = False

    def join(self) -> None:
        """Join the listener thread."""
        pass

    def __enter__(self) -> "MockListener":
        """Enter context manager."""
        self.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager."""
        self.stop()


class MockController:
    """Mock implementation of pynput.mouse.Controller."""

    def __init__(self) -> None:
        """Initialize mock controller."""
        self._position = (0, 0)

    @property
    def position(self) -> tuple[int, int]:
        """Get current position."""
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        """Set current position."""
        self._position = value


# Mock modules
class MockKeyboardModule:
    """Mock implementation of pynput.keyboard module."""

    Key = MockKey
    Listener = MockListener


class MockMouseModule:
    """Mock implementation of pynput.mouse module."""

    Controller = MockController


# Mock pynput package
class MockPynput:
    """Mock implementation of pynput package."""

    keyboard = MockKeyboardModule()
    mouse = MockMouseModule()


def setup_pynput_mock() -> None:
    """Set up pynput mock in sys.modules."""
    # Create mock instances
    mock_pynput = MockPynput()

    # Replace modules in sys.modules
    sys.modules["pynput"] = mock_pynput
    sys.modules["pynput.keyboard"] = mock_pynput.keyboard
    sys.modules["pynput.mouse"] = mock_pynput.mouse

    # Set up Key constants
    mock_pynput.keyboard.Key.ctrl_r = MockKey("ctrl_r")
    mock_pynput.keyboard.Key.end = MockKey("end")
