"""Unit tests for the example.main module."""

from mouse_controls.main import example_function


def test_example_function() -> None:
    """Test the example_function."""
    result = example_function()
    assert result == "This is an example function."
