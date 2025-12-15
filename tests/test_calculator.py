"""Unit tests for basic functionality."""
import pytest


def test_basic_addition():
    """Test basic Python addition."""
    result = 2 + 3
    assert result == 5


def test_basic_subtraction():
    """Test basic Python subtraction."""
    result = 5 - 3
    assert result == 2


def test_basic_multiplication():
    """Test basic Python multiplication."""
    result = 4 * 3
    assert result == 12


def test_basic_division():
    """Test basic Python division."""
    result = 10 / 2
    assert result == 5


def test_string_operations():
    """Test string operations."""
    text = "Hello World"
    assert text.lower() == "hello world"
    assert text.upper() == "HELLO WORLD"
    assert len(text) == 11
