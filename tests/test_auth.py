"""Unit tests for authentication functionality."""
import pytest
from app.auth import create_access_token, verify_password, get_password_hash


def test_password_hashing():
    """Test password hashing works."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert len(hashed) > 0


def test_password_verification():
    """Test password verification."""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    # Correct password should verify
    assert verify_password(password, hashed) is True
    
    # Wrong password should not verify
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token():
    """Test JWT token creation."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    
    assert token is not None
    assert len(token) > 0
    assert isinstance(token, str)
