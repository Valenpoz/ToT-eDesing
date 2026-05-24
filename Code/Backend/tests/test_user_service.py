import pytest
from unittest.mock import patch
from services import user_service

def test_hash_password():
    hashed = user_service.hash_password("mi_clave123")
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA-256 produce 64 caracteres hexadecimales

@patch("services.user_service.user")
def test_register_user_success(mock_user):
    mock_user.create_user.return_value = True

    result = user_service.register_user("Juan", "juan@mail.com", "clave", 1)

    assert result["success"] is True
    assert "registrado" in result["message"]
    mock_user.create_user.assert_called_once()

@patch("services.user_service.user")
def test_register_user_failure(mock_user):
    mock_user.create_user.return_value = False

    result = user_service.register_user("Juan", "juan@mail.com", "clave", 1)

    assert result["success"] is False
    assert "Error" in result["message"]

@patch("services.user_service.user")
def test_login_user_success(mock_user):
    mock_user.login_user.return_value = {"id": 1, "nombre": "Juan"}

    result = user_service.login_user("juan@mail.com", "clave")

    assert result["success"] is True
    assert result["user"]["nombre"] == "Juan"
    mock_user.login_user.assert_called_once()

@patch("services.user_service.user")
def test_login_user_failure(mock_user):
    mock_user.login_user.return_value = None

    result = user_service.login_user("juan@mail.com", "clave")

    assert result["success"] is False
    assert "no encontrado" in result["message"]
