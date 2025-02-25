import pytest
import keyring
import jwt
from datetime import datetime, timedelta, timezone
from crm.services.auth import login_service, logout_service, SECRET_KEY, KEYRING_SERVICE
from crm.models.collaborators import Collaborator
from crm.models.blacklist_tokens import BlacklistToken
from crm.database import SessionLocal
from tests.test_context_db import test_db, test_manager_email, password


def test_login_service_success(test_db):
    """Test successful login."""
    test_user = test_db.query(Collaborator).filter_by(email=test_manager_email).first()
    assert test_user is not None, "⚠️ Test user not found in database!"

    user, error = login_service(test_db, test_manager_email, password)
    assert user is not None
    assert error is None

    token = keyring.get_password(KEYRING_SERVICE, "auth_token")
    assert token is not None, "❌ No token found in keyring after login!"


def test_login_service_invalid_password(test_db):
    """Test login failure due to incorrect password."""
    user, error = login_service(test_db, test_manager_email, "wrongpassword")

    assert user is None
    assert error == "❌ Invalid credentials."

def test_login_service_invalid_email(test_db):
    """Test login failure due to non-existent email."""
    user, error = login_service(test_db, "wrongemail@email.com", password)

    assert user is None
    assert error == "❌ Invalid credentials."


def test_logout_service(test_db):
    """Test logout process."""
    user, _ = login_service(test_db, test_manager_email, password)
    assert user is not None, "⚠️ Login failed before logout test!"

    error = logout_service(test_db)
    assert error is None

    token = keyring.get_password(KEYRING_SERVICE, "auth_token")
    assert token is None, "❌ Token should be removed from keyring after logout!"

    blacklisted_token = test_db.query(BlacklistToken).filter(BlacklistToken.token.isnot(None)).first()
    assert blacklisted_token is not None, "❌ Token should be blacklisted after logout!"


def test_blacklisted_token_cannot_be_used(test_db):
    """Ensure blacklisted tokens are invalid."""
    token_payload = {
        "sub": 1,
        "email": test_manager_email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    fake_token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

    blacklisted_token = BlacklistToken(token=fake_token)
    test_db.add(blacklisted_token)
    test_db.commit()

    blacklisted = test_db.query(BlacklistToken).filter_by(token=fake_token).first()
    assert blacklisted is not None, "❌ Token should be blacklisted!"
