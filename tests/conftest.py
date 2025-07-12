"""Pytest plugin for handling pynput mocking in headless environments."""

import os

import pytest

from mouse_controls.mock_pynput import setup_pynput_mock


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with pynput mocking for headless environments."""
    if os.environ.get("CI") or os.environ.get("DISPLAY") is None:
        setup_pynput_mock()
