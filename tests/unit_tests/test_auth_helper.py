import pytest
import jwt
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone
from crm.helpers.authorize_helper import (
    get_current_user,
    get_authenticated_collaborator,
    encode_auth_token,
    decode_auth_token
)
from crm.models.collaborators import Collaborator
from crm.models.blacklist_tokens import BlacklistToken
from config import SECRET_KEY

@pytest.fixture
def mock_context():
    """Mock the database session (SQLAlchemy)."""
    return MagicMock()

@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing."""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(days=1),
        "iat": datetime.now(timezone.utc),
        "sub": "123"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def expired_token():
    """Generate an expired JWT token."""
    payload = {
        "exp": datetime.now(timezone.utc) - timedelta(days=1),
        "iat": datetime.now(timezone.utc),
        "sub": "123"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def invalid_token():
    """Generate an invalid JWT token."""
    return "invalid.token.string"

@patch("crm.helpers.authorize_helper.keyring.get_password")
def test_get_current_user_valid(mock_keyring, mock_context):
    """Test retrieving a valid logged-in user."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        mock_keyring.return_value = "valid_token"

        with patch("crm.helpers.authorize_helper.get_authenticated_collaborator") as mock_auth:
            mock_auth.return_value = (MagicMock(id=1), None)
            user, error = get_current_user()

        assert user is not None
        assert error is None

@patch("crm.helpers.authorize_helper.keyring.get_password")
def test_get_current_user_no_token(mock_keyring, mock_context):
    """Test when no authentication token is stored."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        mock_keyring.return_value = None

        user, error = get_current_user()
        
        assert user is None
        assert error == "❌ No stored authentication token. Please log in first."

@patch("crm.helpers.authorize_helper.decode_auth_token")
def test_get_authenticated_collaborator_invalid(mock_decode, mock_context, invalid_token):
    """Test when token is invalid."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        mock_decode.return_value = "Invalid token. Please log in again."

        user, error = get_authenticated_collaborator(invalid_token)

        assert user is None
        assert error == "❌ Token is invalid or expired."
        mock_context.get.assert_not_called()

def test_encode_auth_token():
    """Test token encoding."""
    token = encode_auth_token(123)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    assert decoded["sub"] == "123"

def test_decode_auth_token_valid(mock_context, valid_token):
    """Test decoding a valid JWT token."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        mock_context.query().filter_by().first.return_value = None

        user_id = decode_auth_token(valid_token)
        
        assert user_id == "123"

def test_decode_auth_token_blacklisted(mock_context, valid_token):
    """Test decoding a blacklisted token."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        mock_context.query().filter_by().first.return_value = BlacklistToken(token=valid_token)

        user_id = decode_auth_token(valid_token)
        
        assert user_id == "Token has been revoked. Please log in again."

def test_decode_auth_token_expired(mock_context, expired_token):
    """Test decoding an expired token."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        user_id = decode_auth_token(expired_token)
        
        assert user_id == "Token has expired. Please log in again."

def test_decode_auth_token_invalid(mock_context, invalid_token):
    """Test decoding an invalid token."""
    with (
        patch("crm.helpers.authorize_helper.DB", mock_context),
    ):
        user_id = decode_auth_token(invalid_token)
        
        assert user_id == "Invalid token. Please log in again."
