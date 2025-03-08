import pytest
from sqlalchemy.orm import Session
from crm.models.contracts import Contract
from crm.models.clients import Client
from crm.services.contracts import create_contract, get_contract, get_all_contracts, update_contract, delete_contract
from tests.test_context_db import test_db, test_manager_email
from unittest.mock import patch


@pytest.fixture
def sample_contract(test_db: Session):
    """Fixture to create a sample contract for testing."""
    test_client = test_db.query(Client).first()
    assert test_client, "❌ No test client found. Ensure test_db fixture is correctly set up."

    contract = create_contract(
        db=test_db,
        costing=1000.00,
        remaining_due_payment=500.00,
        is_signed=True,
        client_id=test_client.id,
        commercial_id=test_client.commercial_id
    )
    test_db.commit()
    return contract


def test_create_contract(test_db):
    """Test contract creation."""
    test_client = test_db.query(Client).first()
    assert test_client, "❌ No test client found."

    contract = create_contract(
        db=test_db,
        costing=2000.00,
        remaining_due_payment=1500.00,
        is_signed=False,
        client_id=test_client.id,
        commercial_id=test_client.commercial_id
    )

    assert contract.id is not None, "❌ Contract ID should not be None"
    assert contract.costing == 2000.00
    assert contract.remaining_due_payment == 1500.00
    assert contract.is_signed is False


def test_get_contract(test_db, sample_contract):
    """Test retrieving a contract by ID."""
    retrieved_contract = get_contract(db=test_db, contract_id=sample_contract.id)

    assert retrieved_contract is not None, "❌ Contract should be found"
    assert retrieved_contract.id == sample_contract.id
    assert retrieved_contract.costing == 1000.00


def test_get_all_contracts(test_db):
    """Test retrieving all contracts."""
    mock_collaborator = type("Collaborator", (object,), {"id": 3, "role_id": 3})
    with (
        patch("crm.services.contracts.get_current_user", return_value=(mock_collaborator, None)),
    ):
        contracts = get_all_contracts(db=test_db, filter_field=None, filter_value=None)

    assert isinstance(contracts, list), "❌ Should return a list"
    assert len(contracts) > 0, "❌ At least one contract should be present"


def test_update_contract(test_db, sample_contract):
    """Test updating a contract's details."""
    updated_contract = update_contract(
        db=test_db,
        contract_id=sample_contract.id,
        remaining_due_payment=0.00,
        is_signed=True
    )

    assert updated_contract is not None, "❌ Contract should exist"
    assert updated_contract.remaining_due_payment == 0.00
    assert updated_contract.is_signed is True


def test_delete_contract(test_db, sample_contract):
    """Test deleting a contract."""
    result = delete_contract(db=test_db, contract_id=sample_contract.id)

    assert result is True, "❌ Contract should be deleted"
    assert get_contract(db=test_db, contract_id=sample_contract.id) is None, "❌ Contract should not exist after deletion"
