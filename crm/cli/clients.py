import click
from crm.database import DB
from crm.services.clients import create_client, get_client, get_all_clients, update_client, delete_client
from crm.helpers.validator_helper import ValidatorHelper
from crm.helpers.authorize_helper import role_restricted, authentication_required, self_user_restricted, get_current_user
from crm.enums.model_type_enum import ModelTypeEnum
from crm.models.roles import RoleEnum
from crm.enums.relationships_enum import RelationshipEnum


@click.group()
def clients():
    """Manage Clients"""
    pass

@click.command()
@click.option('--first-name', prompt="First Name", help="First name of the client")
@click.option('--last-name', prompt="Last Name", help="Last name of the client")
@click.option('--email', prompt="Email", help="Email of the client")
@click.option('--phone', prompt="Phone", help="Phone number of the client")
@click.option('--company-name', prompt="Company Name", help="Company name of the client")
@role_restricted([RoleEnum.SALES])
def add(first_name, last_name, email, phone, company_name):
    """Add a new client."""
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "company_name": company_name
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.CLIENT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    try:
        client = create_client(DB, first_name, last_name, email, phone, company_name)
        click.echo(f"✅ Client {client.full_name} created!")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")
    finally:
        DB.close()

@click.command()
@click.argument('client_id', type=int)
@role_restricted([RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CLIENT)
def view(client_id):
    """Get a client by ID."""
    client = get_client(DB, client_id)
    DB.close()
    if client:
        click.echo(f"👤 {client.infos}")
    else:
        click.echo("❌ Client not found!")

@click.command()
@authentication_required()
def list():
    """List all clients."""
    clients = get_all_clients(DB)
    DB.close()
    if not clients:
        click.echo("🚨 No clients found!")
    else:
        for c in clients:
            click.echo(f"👤 {c.minimal_infos}")

@click.command()
@click.argument('client_id', type=int)
@click.option('--first-name', prompt="First Name", help="New client's first name")
@click.option('--last-name', prompt="Last Name", help="New client's last name")
@click.option('--email', prompt="Email", help="New client's email")
@click.option('--phone', prompt="Phone", help="New client's phone number")
@click.option('--company-name', prompt="Company Name", help="New client's company name")
@role_restricted([RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CLIENT)
def edit(client_id, first_name, last_name, email, phone, company_name):
    """Edit a client."""
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "company_name": company_name
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.CLIENT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    client = update_client(DB, client_id, **data)
    DB.close()
    if client:
        click.echo(f"✅ Client {client_id} updated successfully!")
    else:
        click.echo("❌ Client not found!")


@click.command()
@click.argument('client_id', type=int)
@role_restricted([RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CLIENT)
def delete(client_id):
    """Remove a client."""
    success = delete_client(DB, client_id)
    DB.close()
    if success:
        click.echo(f"✅ Client {client_id} deleted successfully!")
    else:
        click.echo("❌ Client not found!")

clients.add_command(add)
clients.add_command(view)
clients.add_command(list)
clients.add_command(edit)
clients.add_command(delete)
