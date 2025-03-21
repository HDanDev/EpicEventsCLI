import click
from crm.database import DB
from crm.services.collaborators import create_collaborator, get_collaborator, get_all_collaborators, update_collaborator, update_password, delete_collaborator
from crm.helpers.validator_helper import ValidatorHelper
from crm.helpers.authorize_helper import role_restricted, authentication_required, self_user_restricted, get_current_user
from crm.enums.model_type_enum import ModelTypeEnum
from crm.models.roles import RoleEnum


@click.group()
def collaborators():
    """Manage Collaborators"""
    pass

@click.command()
@click.option('--first-name', prompt="First Name", help="First name of the collaborator")
@click.option('--last-name', prompt="Last Name", help="Last name of the collaborator")
@click.option('--email', prompt="Email", help="Email of the collaborator")
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="Password for the collaborator")
@click.option('--role-id', type=int, prompt="Role ID", help="Role ID of the collaborator")
@role_restricted([RoleEnum.MANAGEMENT])
def add(first_name, last_name, email, password, role_id):
    """Add a new collaborator."""
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "role_id": role_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.COLLABORATOR, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    try:
        collaborator = create_collaborator(DB, first_name, last_name, email, password, role_id)
        click.echo(f"✅ Collaborator {collaborator.full_name} created!")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")
    finally:
        DB.close()

@click.command()
@click.argument('collaborator_id', type=int)
@authentication_required()
def view(collaborator_id):
    """Get a collaborator by ID."""
    collaborator = get_collaborator(DB, collaborator_id)
    DB.close()
    if collaborator:
        click.echo(f"👤 {collaborator.infos}")
    else:
        click.echo("❌ Collaborator not found!")

@click.command()
@click.option('--filter-field', type=str, help="Field to filter by (available choices are: id, id, first_name, last_name, email, role_id).")
@click.option('--filter-value', type=str, help="Value to filter by.")
@authentication_required()
def list(filter_field, filter_value):
    """List all collaborators."""
    try:
        collaborators = get_all_collaborators(DB, filter_field, filter_value)
    except ValueError as e:
        click.echo(f"🚨 {str(e)}")
        raise SystemExit(1)
    DB.close()

    if not collaborators:
        click.echo("🚨 No collaborators found!")
    else:
        for c in collaborators:
            click.echo(f"👤 {c.minimal_infos}")

@click.command()
@click.argument('collaborator_id', type=int)
@click.option('--first-name', help="New first name")
@click.option('--last-name', help="New last name")
@click.option('--email', help="New email")
@click.option('--role-id', type=int, help="New role ID")
@role_restricted([RoleEnum.MANAGEMENT], True)
def edit(collaborator_id, first_name, last_name, email, role_id):
    """Edit a collaborator."""
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "role_id": role_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.COLLABORATOR, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return

    updates = {"first_name": first_name, "last_name": last_name, "email": email, "role_id": role_id}
    
    collaborator = update_collaborator(DB, collaborator_id, **updates)
    DB.close()
    if collaborator:
        click.echo(f"✅ Collaborator {collaborator_id} updated successfully!")
    else:
        click.echo("❌ Collaborator not found!")
        
@click.command()
@click.option('--password', help="New password")
@self_user_restricted()
def edit_password(password):
    """Update password."""
    data = {
        "password": password
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.COLLABORATOR, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    current_collaborator = get_current_user(DB)
    collaborator = update_password(DB, current_collaborator.id, password)
    DB.close()
    if collaborator:
        click.echo(f"✅ Password updated successfully!")
    else:
        click.echo("❌ Collaborator not found!")
        

@click.command()
@click.argument('collaborator_id', type=int)
@role_restricted([RoleEnum.MANAGEMENT], True)
def delete(collaborator_id):
    """Remove a collaborator."""
    success = delete_collaborator(DB, collaborator_id)
    DB.close()
    if success:
        click.echo(f"✅ Collaborator {collaborator_id} deleted successfully!")
    else:
        click.echo("❌ Collaborator not found!")

collaborators.add_command(add)
collaborators.add_command(view)
collaborators.add_command(list)
collaborators.add_command(edit)
collaborators.add_command(edit_password)
collaborators.add_command(delete)
