import jwt
import click
from datetime import datetime, timedelta, timezone
from functools import wraps
from crm.models.collaborators import Collaborator
from crm.models.clients import Client
from crm.models.contracts import Contract
from crm.models.roles import RoleEnum
from crm.enums.relationships_enum import RelationshipEnum
from crm.models.blacklist_tokens import BlacklistToken
import keyring
from config import SECRET_KEY, KEYRING_SERVICE
from crm.database import SessionLocal

db = SessionLocal()

def get_current_user():
    """Retrieve the currently logged-in user using stored token."""
    token = keyring.get_password(KEYRING_SERVICE, "auth_token")
    if not token:
        return None, "❌ No stored authentication token. Please log in first."

    user, error = get_authenticated_collaborator(token)
    if error:
        return None, error

    return user, None

def authentication_required(f):
    """Decorator to require authentication for CLI commands."""
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user, error = get_current_user()
        if error:
            click.echo(error)
            return
        return f(*args, **kwargs)
    return decorated

def get_authenticated_collaborator(token):
    """Retrieve an authenticated user based on token."""
    if not token:
        return None, "❌ Token is missing or invalid."

    try:
        collaborator_id = decode_auth_token(token)
        current_collaborator = db.get(Collaborator, collaborator_id)

        if not current_collaborator:
            return None, "❌ Unauthorized token for this action."

        return current_collaborator, None

    except Exception as e:
        return None, "❌ Token is invalid or expired."

def self_user_restricted(f):
    """Decorator to restrict actions to the logged-in user."""
    @wraps(f)
    @authentication_required
    def decorated(id, *args, **kwargs):
        current_collaborator, error = get_current_user()
        if error or current_collaborator.id != id:
            click.echo("❌ Permission denied.")
            return
        return f(id, *args, **kwargs)
    return decorated

def role_restricted(roles, is_self_edition_exception=False, relationType=RelationshipEnum.NONE):
    """Decorator to restrict actions based on user roles."""
    def decorator(func):
        @wraps(func)
        @authentication_required
        def wrapper(*args, **kwargs):
            target_user_id = kwargs.get("id")
            
            current_collaborator, error = get_current_user()

            if is_self_edition_exception and current_collaborator.id == target_user_id:
                return func(*args, **kwargs)

            role = RoleEnum(current_collaborator.role_id)
            if role not in roles or error:
                click.echo("❌ Permission denied.")
                return

            if relationType:
                result = relationship_check_switch(current_collaborator, relationType, *args, **kwargs)
                if result:
                    click.echo(result)
                    return

            return func(*args, **kwargs)
        return wrapper
    return decorator

def encode_auth_token(user_id):
    """Generate an authentication token for a user."""
    try:
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": str(user_id)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    except Exception as e:
        return str(e)


def decode_auth_token(auth_token):
    """Decodes a JWT token and checks if it is blacklisted."""
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=["HS256"])
        
        blacklisted = db.query(BlacklistToken).filter_by(token=auth_token).first()
        if blacklisted:
            return "Token has been revoked. Please log in again."

        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Token has expired. Please log in again."
    except jwt.InvalidTokenError as e:
        return "Invalid token. Please log in again."


def relationship_check_switch(current_collaborator, relationship_enum=RelationshipEnum.NONE, *args, **kwargs):
    """Check user relationships for permission-based access."""
    if relationship_enum == RelationshipEnum.NONE or not current_collaborator:
        return None
    elif RoleEnum(current_collaborator.role_id) == RoleEnum.SALES and relationship_enum == RelationshipEnum.COLLABORATOR_CLIENT:
        return collaborator_client_relationship_check(current_collaborator, *args, **kwargs)
    elif RoleEnum(current_collaborator.role_id) == RoleEnum.SALES and relationship_enum == RelationshipEnum.COLLABORATOR_CONTRACT:
        return collaborator_contract_relationship_check(current_collaborator, *args, **kwargs)

def collaborator_client_relationship_check(current_collaborator, *args, **kwargs):
    """Ensure a collaborator can only interact with assigned clients."""
    client_id = kwargs.get("id")

    client = db.query(Client).filter(
        Client.id == client_id,
        Client.commercial_id == current_collaborator.id
        ).first()
    
    if client is None:
        return "❌ Permission denied: You can only interact with assigned clients."
    return None

def collaborator_contract_relationship_check(current_collaborator, *args, **kwargs):
    """Ensure a collaborator can only create events for signed contracts."""
    contract_id = kwargs.get("contract_id")

    if not contract_id:
        return "❌ The contract_id field is mandatory."

    contract = db.get(Contract, contract_id)

    if not contract:
        return "❌ Contract not found."

    if not contract.signed:
        return "❌ Permission denied: Only signed contracts allow event creation."

    client = db.query(Client).filter(
        Client.id == contract.client_id,
        Client.commercial_id == current_collaborator.id
        ).first()

    if client is None:
        return "❌ Permission denied: You can only create events for assigned clients."

    return None
