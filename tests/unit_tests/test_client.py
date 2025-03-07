import pytest
from sqlalchemy.orm import Session
from crm.models.clients import Client
from crm.models.roles import RoleEnum
from unittest.mock import patch
from crm.helpers.authorize_helper import get_current_user
from crm.services.clients import create_client, get_client, get_all_clients, update_client, delete_client
from tests.test_context_db import test_db


@pytest.fixture
def sample_client(test_db: Session):
    """Fixture to create a sample client for testing."""
    mock_collaborator = type("Collaborator", (object,), {"id": 3})

    with patch("crm.services.clients.get_current_user", return_value=(mock_collaborator, None)):
        client = create_client(
            db=test_db,
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
            company_name="Doe Inc"
        )
        test_db.commit()
        return client


def test_create_client(test_db):
    """Test client creation."""
    mock_collaborator = type("Collaborator", (object,), {"id": 3})

    with patch("crm.services.clients.get_current_user", return_value=(mock_collaborator, None)):
        client = create_client(
            db=test_db,
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            phone="987654321",
            company_name="Smith Ltd"
        )

        assert client.id is not None, "❌ Client ID should not be None"
        assert client.first_name == "Alice"
        assert client.last_name == "Smith"
        assert client.email == "alice.smith@example.com"
        assert client.commercial_id == 3


def test_get_client(test_db, sample_client):
    """Test retrieving a client by ID."""
    retrieved_client = get_client(db=test_db, client_id=sample_client.id)

    assert retrieved_client is not None, "❌ Client should be found"
    assert retrieved_client.id == sample_client.id
    assert retrieved_client.email == "john.doe@example.com"


def test_get_all_clients(test_db):
    """Test retrieving all clients."""
    clients = get_all_clients(db=test_db)

    assert isinstance(clients, list), "❌ Should return a list"
    assert len(clients) > 0, "❌ Should retrieve at least one client"


def test_update_client(test_db, sample_client):
    """Test updating a client's details."""
    updated_client = update_client(
        db=test_db,
        client_id=sample_client.id,
        phone="111222333",
        company_name="Updated Doe Inc"
    )

    assert updated_client is not None, "❌ Client should exist"
    assert updated_client.phone == "111222333"
    assert updated_client.company_name == "Updated Doe Inc"


def test_delete_client(test_db, sample_client):
    """Test deleting a client."""
    result = delete_client(db=test_db, client_id=sample_client.id)

    assert result is True, "❌ Client should be deleted"
    assert get_client(db=test_db, client_id=sample_client.id) is None, "❌ Client should not exist after deletion"
