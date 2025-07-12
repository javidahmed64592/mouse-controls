"""Fixtures for testing mouse_controls."""

import logging
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from pynput.keyboard import Key, Listener

from mouse_controls.models.mouse import Mouse

POS_LIMS = ((0, 1920), (0, 1080))
POS_BUFFER = 10
DELTA_TIME = 0.001
LOCK_TOGGLE_BUTTON = Key.ctrl_r
EXIT_BUTTON = Key.end


# General fixtures
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
def mock_mouse(mock_mouse_data: dict) -> Mouse:
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
        return mock_mouse


@pytest.fixture
def mock_keyboard_listener() -> Generator[Listener, None, None]:
    """Mock keyboard listener for testing."""
    with patch("pynput.keyboard.Listener", return_value=MagicMock(spec=Listener)) as mock_listener:
        yield mock_listener.return_value
