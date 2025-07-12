"""Unit tests for the mouse_controls.models.mouse_listener module."""

from unittest.mock import MagicMock

import pytest

from mouse_controls.models.mouse import Mouse
from mouse_controls.models.mouse_listener import MouseListener


class TestMouseListener:
    """Test suite for the MouseListener class."""

    def test_initialization(self, mock_mouse_listener: MouseListener, mock_mouse: Mouse) -> None:
        """Test the initialization of the MouseListener instance."""
        assert mock_mouse_listener.mouse == mock_mouse

    def test_start(
        self,
        caplog: pytest.LogCaptureFixture,
        mock_mouse_listener: MouseListener,
        mock_mouse: Mouse,
        mock_keyboard_listener: MagicMock,
    ) -> None:
        """Test starting the mouse listener."""
        mock_mouse_listener.start()
        assert "Mouse listener started." in caplog.text
        assert (
            f"Press {mock_mouse._lock_toggle_btn.name} to toggle lock, {mock_mouse._exit_btn.name} to exit."
            in caplog.text
        )
        mock_mouse.start.assert_called_once()
        mock_keyboard_listener.__enter__.assert_called_once()

        # join() raises SystemExit so listener thread stops
        assert "Mouse listener stopped by user." in caplog.text
        mock_keyboard_listener.__exit__.assert_called_once()
