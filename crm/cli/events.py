import click
from crm.database import DB
from crm.services.events import create_event, get_event, get_all_events, update_event, delete_event
from crm.helpers.validator_helper import ValidatorHelper
from crm.helpers.authorize_helper import role_restricted, authentication_required, self_user_restricted, get_current_user
from crm.enums.model_type_enum import ModelTypeEnum
from crm.models.roles import RoleEnum
from crm.enums.relationships_enum import RelationshipEnum


@click.group()
def events():
    """Manage Events"""
    pass

@click.command()
@click.option('--name', prompt="Name", help="Name of the event")
@click.option('--location', prompt="Location", help="Location of the event")
@click.option('--attendees', prompt="Number of attendees", help="Number of attendees of the event", type=int)
@click.option('--notes', prompt="Additional notes", help="Notes of the event")
@click.option('--contract-id', prompt="Contract ID", help="Contract ID of the event related contract", type=int)
@click.option('--start-date', prompt="Start date (⚠️Should follow this strict format: \"DD/MM/YYYY-HHhMM\")", help="Start date of the event")
@click.option('--end-date', prompt="End date (⚠️Should follow this strict format: \"DD/MM/YYYY-HHhMM\")", help="End date of the event")
@click.option('--support-id', prompt="Support ID", help="Collaborator ID of the event related support collaborator", type=int)
@role_restricted([RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CONTRACT)
def add(name, location, attendees, notes, contract_id, start_date, end_date, support_id):
    """Add a new event."""
    data = {
        "name": name,
        "location": location,
        "attendees": attendees,
        "notes": notes,
        "contract_id": contract_id,
        "start_date": start_date,
        "end_date": end_date,
        "support_id": support_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.EVENT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    try:
        event = create_event(DB, name, location, attendees, notes, contract_id, start_date, end_date, support_id)
        click.echo(f"✅ Event {event.name} created!")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")
    finally:
        DB.close()

@click.command()
@click.argument('event_id', type=int)
@role_restricted([RoleEnum.SUPPORT])
def view(event_id):
    """Get a event by ID."""
    event = get_event(DB, event_id)
    DB.close()
    if event:
        click.echo(f"👤 {event.infos}")
    else:
        click.echo("❌ Event not found!")

@click.command()
@click.option('--filter-field', type=str, help="Field to filter by (available choices are: id, name, location, attendees, notes, contract_id, start_date, end_date, support_id).")
@click.option('--filter-value', type=str, help="Value to filter by.")
@authentication_required()
def list(filter_field, filter_value):
    """List all events."""
    try:
        events = get_all_events(DB, filter_field, filter_value)
    except ValueError as e:
        click.echo(f"🚨 {str(e)}")
        raise SystemExit(1)
    DB.close()

    if not events:
        click.echo("🚨 No events found!")
    else:
        for c in events:
            click.echo(f"👤 {c.minimal_infos}")

@click.command()
@click.argument('event_id', type=int)
@click.option('--name', prompt="Name", help="Name of the event")
@click.option('--location', prompt="Location", help="Location of the event")
@click.option('--attendees', prompt="Number of attendees", help="Number of attendees of the event", type=int)
@click.option('--notes', prompt="Additional notes", help="Notes of the event")
@click.option('--contract-id', prompt="Contract ID", help="Contract ID of the event related contract", type=int)
@click.option('--start-date', prompt="Start date (⚠️Should follow this strict format: \"DD/MM/YYYY-HHhMM\")", help="Start date of the event")
@click.option('--end-date', prompt="End date (⚠️Should follow this strict format: \"DD/MM/YYYY-HHhMM\")", help="End date of the event")
@click.option('--support-id', prompt="Support ID", help="Collaborator ID of the event related support collaborator", type=int)
@role_restricted([RoleEnum.MANAGEMENT, RoleEnum.SUPPORT], True)
def edit(event_id, name, location, attendees, notes, contract_id, start_date, end_date, support_id):
    """Edit a event."""
    data = {
        "name": name,
        "location": location,
        "attendees": attendees,
        "notes": notes,
        "contract_id": contract_id,
        "start_date": start_date,
        "end_date": end_date,
        "support_id": support_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.EVENT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    event = update_event(DB, event_id, **data)
    DB.close()
    if event:
        click.echo(f"✅ Event {event_id} updated successfully!")
    else:
        click.echo("❌ Event not found!")


@click.command()
@click.argument('event_id', type=int)
@role_restricted([RoleEnum.SALES], True)
def delete(event_id):
    """Remove a event."""
    success = delete_event(DB, event_id)
    DB.close()
    if success:
        click.echo(f"✅ Event {event_id} deleted successfully!")
    else:
        click.echo("❌ Event not found!")

events.add_command(add)
events.add_command(view)
events.add_command(list)
events.add_command(edit)
events.add_command(delete)
