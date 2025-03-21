from sqlalchemy.orm import Session
from crm.models.events import Event
from crm.models.roles import RoleEnum
from crm.helpers.authorize_helper import get_current_user
from crm.helpers.format_helper import FormatHelper
from crm.helpers.filter_helper import FilterHelper
import click


def create_event(db: Session, name: str, location: str, attendees: str, notes: str, contract_id: str, start_date: str, end_date: str, support_id: str):
    """Create a new event."""    
    event = Event(
        name=name,
        location=location,
        attendees=attendees,
        notes=notes,
        contract_id=contract_id,
        start_date=FormatHelper.format_date(start_date),
        end_date=FormatHelper.format_date(end_date),
        support_id=support_id
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event(db: Session, event_id: int):
    """Retrieve a event by ID."""
    return db.query(Event).filter(Event.id == event_id).first()

def get_all_events(db: Session, filter_field, filter_value):
    """Retrieve all events."""
    current_collaborator, error = get_current_user()
    is_of_authorized_roles = RoleEnum(current_collaborator.role_id) == RoleEnum.MANAGEMENT or RoleEnum(current_collaborator.role_id) == RoleEnum.SUPPORT
    if not is_of_authorized_roles and (filter_field != None or filter_value != None):
        click.echo(f"🚨 Only Managers have the right to use the filter option for events, proceeding without them...")
        
    if not error and is_of_authorized_roles:
        filter_helper = FilterHelper(db, Event)
        return filter_helper.apply_filter(filter_field, filter_value)
    return db.query(Event).all()

def update_event(db: Session, event_id: int, **kwargs):
    """Update a event's details."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None

    for key, value in kwargs.items():
        if hasattr(event, key) and value is not None:
            if key == "start_date" or key == "end_date":
                print("hein???")
                setattr(event, key, FormatHelper.format_date(value))
            else:
                setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int):
    """Delete a event by ID."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return False

    db.delete(event)
    db.commit()
    return True
