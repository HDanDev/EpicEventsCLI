from sqlalchemy.orm import Session
from crm.models.clients import Client
from crm.models.roles import RoleEnum
from crm.helpers.authorize_helper import get_current_user
from crm.helpers.filter_helper import FilterHelper
import click


def create_client(db: Session, first_name: str, last_name: str, email: str, phone: str, company_name: str):
    """Create a new client."""
    current_collaborator, error = get_current_user()
    client = Client(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company_name=company_name, 
        commercial_id=current_collaborator.id
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_client(db: Session, client_id: int):
    """Retrieve a client by ID."""
    return db.query(Client).filter(Client.id == client_id).first()

def get_all_clients(db: Session, filter_field, filter_value):
    """Retrieve all clients."""
    current_collaborator, error = get_current_user()
    if RoleEnum(current_collaborator.role_id) != RoleEnum.MANAGEMENT and (filter_field != None or filter_value != None):
        click.echo(f"🚨 Only Managers have the right to use the filter option for clients, proceeding without them...")
        
    if not error and RoleEnum(current_collaborator.role_id) == RoleEnum.MANAGEMENT:
        filter_helper = FilterHelper(db, Client)
        return filter_helper.apply_filter(filter_field, filter_value)
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
