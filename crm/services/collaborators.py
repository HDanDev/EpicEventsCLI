from sqlalchemy.orm import Session
from crm.models.collaborators import Collaborator
from crm.models.roles import Role
from crm.helpers.format_helper import FormatHelper


def create_collaborator(db: Session, first_name: str, last_name: str, email: str, password: str, role_id: int):
    """Create a new collaborator."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise ValueError(f"Role ID {role_id} does not exist!")

    collaborator = Collaborator(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=FormatHelper.hash_password(password),
        role_id=role_id
    )
    db.add(collaborator)
    db.commit()
    db.refresh(collaborator)
    return collaborator

def get_collaborator(db: Session, collaborator_id: int):
    """Retrieve a collaborator by ID."""
    return db.query(Collaborator).filter(Collaborator.id == collaborator_id).first()

def get_all_collaborators(db: Session):
    """Retrieve all collaborators."""
    return db.query(Collaborator).all()

def update_collaborator(db: Session, collaborator_id: int, **kwargs):
    """Update a collaborator's details."""
    collaborator = db.query(Collaborator).filter(Collaborator.id == collaborator_id).first()
    if not collaborator:
        return None

    for key, value in kwargs.items():
        if hasattr(collaborator, key) and value is not None:
            setattr(collaborator, key, value)

    db.commit()
    db.refresh(collaborator)
    return collaborator

def update_password(db: Session, collaborator_id: int, password: str):
    """Update a collaborator's password."""
    collaborator = db.query(Collaborator).filter(Collaborator.id == collaborator_id).first()
    if not collaborator:
        return None

    if password is not None:
        setattr(collaborator, "password_hash", FormatHelper.hash_password(password))

    db.commit()
    db.refresh(collaborator)
    return collaborator

def delete_collaborator(db: Session, collaborator_id: int):
    """Delete a collaborator by ID."""
    collaborator = db.query(Collaborator).filter(Collaborator.id == collaborator_id).first()
    if not collaborator:
        return False

    db.delete(collaborator)
    db.commit()
    return True
