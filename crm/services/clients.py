from sqlalchemy.orm import Session
from crm.models.clients import Client
from crm.models.roles import RoleEnum
from crm.helpers.authorize_helper import get_current_user


def create_client(db: Session, first_name: str, last_name: str, email: str, phone: str, company_name: str):
    """Create a new client."""

    client = Client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company_name=company_name
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_client(db: Session, client_id: int):
    """Retrieve a client by ID."""
    return db.query(Client).filter(Client.id == client_id).first()

def get_all_clients(db: Session):
    """Retrieve all clients."""
    current_collaborator, error = get_current_user(db)
    if not error and RoleEnum(current_collaborator.id) == RoleEnum.MANAGEMENT:
        print("add filtering for Management")
    return db.query(Client).all()

def update_client(db: Session, client_id: int, **kwargs):
    """Update a client's details."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None

    for key, value in kwargs.items():
        if hasattr(client, key) and value is not None:
            setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

def delete_client(db: Session, client_id: int):
    """Delete a client by ID."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return False

    db.delete(client)
    db.commit()
    return True
