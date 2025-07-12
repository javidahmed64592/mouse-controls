"""Unit tests for the mouse_controls.models.mouse module."""

from unittest.mock import MagicMock

import pytest

from mouse_controls.models.mouse import Mouse


class TestMouse:
    """Test suite for the Mouse class."""

    def test_initialization(self, mock_mouse: Mouse, mock_mouse_data: dict) -> None:
        """Test the initialization of the Mouse instance."""
        assert mock_mouse._pos_lims == mock_mouse_data["pos_lims"]
        assert mock_mouse._pos_buffer == mock_mouse_data["pos_buffer"]
        assert mock_mouse._delay == mock_mouse_data["delay"]
        assert not mock_mouse._mouse_locked
        assert mock_mouse._running is False

    def test_toggle_mouse_lock(self, caplog: pytest.LogCaptureFixture, mock_mouse: Mouse) -> None:
        """Test toggling the mouse lock state."""
        initial_state = mock_mouse._mouse_locked
        mock_mouse.toggle_mouse_lock()
        assert mock_mouse._mouse_locked != initial_state
        assert "Mouse lock toggled. Current state: Locked" in caplog.text

        caplog.clear()
        mock_mouse.toggle_mouse_lock()
        assert mock_mouse._mouse_locked == initial_state
        assert "Mouse lock toggled. Current state: Unlocked" in caplog.text

    def test_exit_when_running(self, caplog: pytest.LogCaptureFixture, mock_mouse: Mouse) -> None:
        """Test the exit method when the mouse is running."""
        mock_mouse._running = True
        mock_mouse.exit()

        assert "Mouse control thread stopping..." in caplog.text
        assert not mock_mouse._mouse_locked
        assert not mock_mouse._running

    def test_exit_when_not_running(self, caplog: pytest.LogCaptureFixture, mock_mouse: Mouse) -> None:
        """Test the exit method when the mouse is not running."""
        mock_mouse._running = False
        mock_mouse.exit()

        assert "Mouse control thread stopping..." not in caplog.text
        assert not mock_mouse._mouse_locked
        assert not mock_mouse._running

    def test_on_press_toggle_lock(
        self, caplog: pytest.LogCaptureFixture, mock_mouse: Mouse, mock_keyboard_listener: MagicMock
    ) -> None:
        """Test handling key press events to toggle mouse lock."""
        mock_mouse._mouse_locked = False
        mock_mouse.on_press(mock_mouse._lock_toggle_btn, mock_keyboard_listener)

        assert mock_mouse._mouse_locked
        assert "Mouse lock toggled. Current state: Locked" in caplog.text

        caplog.clear()
        mock_mouse.on_press(mock_mouse._lock_toggle_btn, mock_keyboard_listener)

        assert not mock_mouse._mouse_locked
        assert "Mouse lock toggled. Current state: Unlocked" in caplog.text

    def test_on_press_exit(
        self, caplog: pytest.LogCaptureFixture, mock_mouse: Mouse, mock_keyboard_listener: MagicMock
    ) -> None:
        """Test handling key press events to exit the program."""
        mock_mouse._running = True
        mock_mouse.on_press(mock_mouse._exit_btn, mock_keyboard_listener)

        assert not mock_mouse._running
        assert "Mouse control thread stopping..." in caplog.text
        assert not mock_mouse._mouse_locked
        mock_keyboard_listener.stop.assert_called_once()

    def test_run_mouse_locked(self, mock_mouse: Mouse, mock_mouse_data: dict, mock_time_sleep: MagicMock) -> None:
        """Test the run method when the mouse is locked."""
        mock_time_sleep.side_effect = [KeyboardInterrupt]
        mock_mouse._mouse_locked = True
        mock_mouse._mouse.position = (0, 0)
        with pytest.raises(KeyboardInterrupt):
            mock_mouse.run()

        assert mock_mouse._mouse.position == (mock_mouse_data["pos_buffer"], mock_mouse_data["pos_buffer"])

    def test_run_mouse_not_locked(self, mock_mouse: Mouse, mock_time_sleep: MagicMock) -> None:
        """Test the run method when the mouse is not locked."""
        mock_time_sleep.side_effect = [KeyboardInterrupt]
        mock_mouse._mouse_locked = False
        mock_mouse._mouse.position = (0, 0)
        with pytest.raises(KeyboardInterrupt):
            mock_mouse.run()

        assert mock_mouse._mouse.position == (0, 0)
