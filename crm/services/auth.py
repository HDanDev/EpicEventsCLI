import keyring
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from crm.models.collaborators import Collaborator
from crm.models.blacklist_tokens import BlacklistToken
from config import KEYRING_SERVICE, SECRET_KEY
from crm.helpers.authorize_helper import encode_auth_token, decode_auth_token

def login_service(db: Session, email: str, password: str):
    """Logs in the user, stores token in keyring, and returns the user"""
    collaborator = db.query(Collaborator).filter_by(email=email).first()

    if collaborator and collaborator.check_password(password):
        auth_token = encode_auth_token(collaborator.id)
        if auth_token:
            keyring.set_password(KEYRING_SERVICE, "auth_token", auth_token)
            return collaborator, None
        else:
            return None, "❌ Failed to generate authentication token."
    else:
        return None, "❌ Invalid credentials."

def logout_service(db: Session):
    """Logs out the user by blacklisting the token and removing it from keyring"""
    token = keyring.get_password(KEYRING_SERVICE, "auth_token")

    if not token:
        return "⚠️ No active session found."

    decoded_token = decode_auth_token(token)

    if isinstance(decoded_token, str) and not decoded_token.isdigit():
        return f"❌ {decoded_token}"

    try:
        existing_blacklist = db.query(BlacklistToken).filter_by(token=token).first()
        if existing_blacklist:
            keyring.delete_password(KEYRING_SERVICE, "auth_token")
            return "⚠️ Already logged out."

        blacklisted_token = BlacklistToken(token=token)
        db.add(blacklisted_token)
        db.commit()

        keyring.delete_password(KEYRING_SERVICE, "auth_token")
        return None
    except Exception as e:
        db.rollback()
        return f"❌ Error logging out: {str(e)}"
