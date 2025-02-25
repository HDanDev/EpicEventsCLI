# import bcrypt
# from sqlalchemy.orm import Session
# from crm.models import Collaborator
# from crm.database import SessionLocal

# def create_user(first_name, last_name, email, password, role):
#     session = SessionLocal()
#     hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
#     user = Collaborator(first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password, role_id=role)
#     session.add(user)
#     session.commit()
#     session.close()
#     print(f"User {user.full_name} created.")

from sqlalchemy.orm import Session
from crm.models.collaborators import Collaborator
from crm.models.roles import Role
from crm.database import SessionLocal

def create_collaborator(db: Session, first_name: str, last_name: str, email: str, password_hash: str, role_id: int):
    """Create a new collaborator."""
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise ValueError(f"Role ID {role_id} does not exist!")

    collaborator = Collaborator(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
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

def update_password(db: Session, collaborator_id: int, hashed_password: str):
    """Update a collaborator's password."""
    collaborator = db.query(Collaborator).filter(Collaborator.id == collaborator_id).first()
    if not collaborator:
        return None

    if hashed_password is not None:
        setattr(collaborator, "password_hash", hashed_password)

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
