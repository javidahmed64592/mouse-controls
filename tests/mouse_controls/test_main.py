"""Unit tests for the mouse_controls.main module."""

from collections.abc import Generator
from unittest.mock import patch

import pytest

from mouse_controls.main import Config, main
from mouse_controls.models.mouse import Mouse
from mouse_controls.models.mouse_listener import MouseListener


@pytest.fixture
def mock_config_data() -> dict:
    """Mock configuration data for testing."""
    return {"pos_lims": ((0, 1920), (0, 1080)), "pos_buffer": 10, "delay": 0.001}


@pytest.fixture
def mock_config(mock_config_data: dict) -> Generator[Config, None, None]:
    """Mock Config instance for testing."""
    with patch("mouse_controls.main.Config.from_json_file") as mock_from_json:
        config = Config(**mock_config_data)
        mock_from_json.return_value = config
        yield config


@pytest.fixture
def mock_mouse_instance(mock_mouse: Mouse) -> Generator[Mouse, None, None]:
    """Mock Mouse instance for testing."""
    with patch("mouse_controls.main.Mouse") as mock_mouse_class:
        mock_mouse_class.return_value = mock_mouse
        yield mock_mouse


@pytest.fixture
def mock_mouse_listener_instance(mock_mouse_listener: MouseListener) -> Generator[MouseListener, None, None]:
    """Mock MouseListener instance for testing."""
    with patch("mouse_controls.main.MouseListener") as mock_listener_class, patch.object(mock_mouse_listener, "start"):
        mock_listener_class.return_value = mock_mouse_listener
        yield mock_mouse_listener


def test_main(mock_config: Config, mock_mouse_instance: Mouse, mock_mouse_listener_instance: MouseListener) -> None:
    """Test the main function of the mouse control application."""
    main()
    mock_mouse_listener_instance.start.assert_called_once()  # type: ignore[attr-defined]
