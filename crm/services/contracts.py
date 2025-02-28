from sqlalchemy.orm import Session
from crm.models.contracts import Contract
from crm.models.roles import RoleEnum
from crm.helpers.authorize_helper import get_current_user


def create_contract(db: Session, costing: float, remaining_due_payment: float, is_signed: bool, client_id: int, commercial_id: int):
    """Create a new contract."""

    contract = Contract(
        costing=costing,
        remaining_due_payment=remaining_due_payment,
        is_signed=is_signed,
        client_id=client_id,
        commercial_id=commercial_id
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract

def get_contract(db: Session, contract_id: int):
    """Retrieve a contract by ID."""
    return db.query(Contract).filter(Contract.id == contract_id).first()

def get_all_contracts(db: Session):
    """Retrieve all contracts."""
    current_collaborator, error = get_current_user(db)
    if not error and RoleEnum(current_collaborator.id) == RoleEnum.SALES:
        print("add filtering for Sales")
    return db.query(Contract).all()

def update_contract(db: Session, contract_id: int, **kwargs):
    """Update a contract's details."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return None

    for key, value in kwargs.items():
        if hasattr(contract, key) and value is not None:
            setattr(contract, key, value)

    db.commit()
    db.refresh(contract)
    return contract

def delete_contract(db: Session, contract_id: int):
    """Delete a contract by ID."""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        return False

    db.delete(contract)
    db.commit()
    return True
