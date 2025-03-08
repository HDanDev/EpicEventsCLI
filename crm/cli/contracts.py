import click
from crm.database import DB
from crm.services.contracts import create_contract, get_contract, get_all_contracts, update_contract, delete_contract
from crm.helpers.validator_helper import ValidatorHelper
from crm.helpers.authorize_helper import role_restricted, authentication_required, self_user_restricted, get_current_user
from crm.enums.model_type_enum import ModelTypeEnum
from crm.models.roles import RoleEnum
from crm.enums.relationships_enum import RelationshipEnum


@click.group()
def contracts():
    """Manage Contracts"""
    pass

@click.command()
@click.option('--costing', prompt="Costing", help="Costing of the contract", type=float)
@click.option('--remaining-due-payment', prompt="Remaining due payment", help="Remaining due payment of the contract", type=float)
@click.option('--is-signed', prompt="Is signed?", help="Weither the contract is signed or not", type=bool)
@click.option('--client-id', prompt="Client ID", help="Client ID of the contract related client", type=int)
@click.option('--commercial-id', prompt="Commercial ID", help="Collaborator ID of the contract related collaborator", type=int)
@role_restricted([RoleEnum.MANAGEMENT])
def add(costing, remaining_due_payment, is_signed, client_id, commercial_id):
    """Add a new contract."""
    data = {
        "costing": costing,
        "remaining_due_payment": remaining_due_payment,
        "is_signed": is_signed,
        "client_id": client_id,
        "commercial_id": commercial_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.CONTRACT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    try:
        contract = create_contract(DB, costing, remaining_due_payment, is_signed, client_id, commercial_id)
        click.echo(f"✅ Contract {contract.id} created!")
    except ValueError as e:
        click.echo(f"❌ Error: {e}")
    finally:
        DB.close()

@click.command()
@click.argument('contract_id', type=int)
@role_restricted([RoleEnum.MANAGEMENT, RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CLIENT)
def view(contract_id):
    """Get a contract by ID."""
    contract = get_contract(DB, contract_id)
    DB.close()
    if contract:
        click.echo(f"👤 {contract.infos}")
    else:
        click.echo("❌ Contract not found!")

@click.command()
@click.option('--filter-field', type=str, help="Field to filter by (available choices are: id, costing, remaining_due_payment, creation_date, is_signed, client_id, commercial_id).")
@click.option('--filter-value', type=str, help="Value to filter by.")
@authentication_required()
def list(filter_field, filter_value):
    """List all contracts."""
    try:
        contracts = get_all_contracts(DB, filter_field, filter_value)
    except ValueError as e:
        click.echo(f"🚨 {str(e)}")
        raise SystemExit(1)
    DB.close()

    if not contracts:
        click.echo("🚨 No contracts found!")
    else:
        for c in contracts:
            # click.echo(f"👤 {c.minimal_infos}")
            click.echo(f"👤 {c.infos}")

@click.command()
@click.argument('contract_id', type=int)
@click.option('--costing', prompt="Costing", help="Costing of the contract", type=float)
@click.option('--remaining-due-payment', prompt="Remaining due payment", help="Remaining due payment of the contract", type=float)
@click.option('--is-signed', prompt="Is signed?", help="Weither the contract is signed or not", type=bool)
@click.option('--client-id', prompt="Client ID", help="Client ID of the contract related client", type=int)
@click.option('--commercial-id', prompt="Commercial ID", help="Collaborator ID of the contract related collaborator", type=int)
@role_restricted([RoleEnum.MANAGEMENT, RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CLIENT)
def edit(contract_id, costing, remaining_due_payment, is_signed, client_id, commercial_id):
    """Edit a contract."""
    data = {
        "costing": costing,
        "remaining_due_payment": remaining_due_payment,
        "is_signed": is_signed,
        "client_id": client_id,
        "commercial_id": commercial_id
    }

    validator = ValidatorHelper(DB, ModelTypeEnum.CONTRACT, data)
    validator.validate_data()

    if not validator.is_valid():
        click.echo("❌ Validation failed:")
        for error in validator.error_messages:
            click.echo(f"   - {error}")
        DB.close()
        return
    
    contract = update_contract(DB, contract_id, **data)
    DB.close()
    if contract:
        click.echo(f"✅ Contract {contract_id} updated successfully!")
    else:
        click.echo("❌ Contract not found!")


@click.command()
@click.argument('contract_id', type=int)
@role_restricted([RoleEnum.MANAGEMENT, RoleEnum.SALES], relationType=RelationshipEnum.COLLABORATOR_CONTRACT)
def delete(contract_id):
    """Remove a contract."""
    success = delete_contract(DB, contract_id)
    DB.close()
    if success:
        click.echo(f"✅ Contract {contract_id} deleted successfully!")
    else:
        click.echo("❌ Contract not found!")

contracts.add_command(add)
contracts.add_command(view)
contracts.add_command(list)
contracts.add_command(edit)
contracts.add_command(delete)
