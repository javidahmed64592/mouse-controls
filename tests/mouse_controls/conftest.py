"""Fixtures for testing mouse_controls."""

import logging
import os
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pynput.keyboard import Key, Listener

from mouse_controls.mock_pynput import setup_pynput_mock
from mouse_controls.models.mouse import Mouse
from mouse_controls.models.mouse_listener import MouseListener

POS_LIMS = ((0, 1920), (0, 1080))
POS_BUFFER = 10
DELTA_TIME = 0.001
LOCK_TOGGLE_BUTTON = Key.ctrl_r
EXIT_BUTTON = Key.end


# General fixtures
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with pynput mocking for headless environments."""
    if os.environ.get("CI") or os.environ.get("DISPLAY") is None:
        setup_pynput_mock()


@pytest.fixture(autouse=True)
def configure_caplog(caplog: pytest.LogCaptureFixture) -> None:
    """Configure caplog for all tests."""
    caplog.set_level(logging.INFO)


@pytest.fixture
def mock_time_sleep() -> Generator[MagicMock, None, None]:
    """Mock time.sleep to avoid delays in tests."""
    with patch("time.sleep") as mock_sleep:
        yield mock_sleep


# Mouse fixtures
@pytest.fixture
def mock_mouse_data() -> dict:
    """Mock data for Mouse instance."""
    return {
        "pos_lims": POS_LIMS,
        "pos_buffer": POS_BUFFER,
        "delay": DELTA_TIME,
        "lock_toggle_btn": LOCK_TOGGLE_BUTTON,
        "exit_btn": EXIT_BUTTON,
    }


@pytest.fixture
def mock_mouse(mock_mouse_data: dict) -> Generator[Mouse, None, None]:
    """Mock Mouse instance for testing."""
    with patch("mouse_controls.models.mouse.Controller") as mock_controller:
        mock_mouse = Mouse(
            pos_lims=mock_mouse_data["pos_lims"],
            pos_buffer=mock_mouse_data["pos_buffer"],
            delay=mock_mouse_data["delay"],
            lock_toggle_btn=mock_mouse_data["lock_toggle_btn"],
            exit_btn=mock_mouse_data["exit_btn"],
        )
        mock_mouse._mouse = mock_controller.return_value
        with patch.object(mock_mouse, "start"):
            yield mock_mouse


@pytest.fixture
def mock_keyboard_listener() -> Generator[MagicMock, None, None]:
    """Mock keyboard listener for testing."""
    with patch("mouse_controls.models.mouse_listener.Listener") as mock_listener_class:
        mock_listener_instance = MagicMock(spec=Listener)
        mock_listener_instance.join = MagicMock()
        mock_listener_instance.stop = MagicMock()
        mock_listener_instance.__enter__ = MagicMock(return_value=mock_listener_instance)
        mock_listener_instance.__exit__ = MagicMock(return_value=None)

        mock_listener_class.return_value = mock_listener_instance
        yield mock_listener_instance


@pytest.fixture
def mock_mouse_listener(mock_mouse: Mouse, mock_keyboard_listener: MagicMock) -> MouseListener:
    """Mock MouseListener instance for testing."""
    with patch("mouse_controls.models.mouse_listener.Listener", return_value=mock_keyboard_listener):
        mock_keyboard_listener.join.side_effect = KeyboardInterrupt
        return MouseListener(mock_mouse)
