import pytest
from sqlalchemy.orm import Session
from crm.models.clients import Client
from unittest.mock import patch
from crm.services.clients import create_client, get_client, get_all_clients
from tests.test_context_db import test_db, cli_runner
from crm.cli.main import cli


@pytest.fixture
def patch_batch(test_db):
    mock_collaborator = type("Collaborator", (object,), {"id": 3, "role_id": 3})
    with (
        patch("crm.cli.clients.DB", test_db),
        patch("crm.helpers.authorize_helper.DB", test_db),
        patch("crm.services.clients.get_current_user", return_value=(mock_collaborator, None)),
        patch("crm.helpers.authorize_helper.get_current_user", return_value=(mock_collaborator, None)),
    ):
        yield


@pytest.fixture
def sample_client(test_db: Session, patch_batch):
    """Fixture to create a sample client for testing."""
    client = create_client(
        db=test_db,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="123456789",
        company_name="Doe Inc"
    )
    client = create_client(
        db=test_db,
        first_name="Marc",
        last_name="Miley",
        email="Marce@example.com",
        phone="843456789",
        company_name="Marc Inc"
    )
    client = create_client(
        db=test_db,
        first_name="Dany",
        last_name="Xorg",
        email="danydoe@example.com",
        phone="563456789",
        company_name="Xorg Inc"
    )
    client = create_client(
        db=test_db,
        first_name="Ben",
        last_name="Affleck",
        email="Bene@example.com",
        phone="763456789",
        company_name="Ben Inc"
    )
    test_db.commit()
    return client


def test_filter_by_email(cli_runner, sample_client, test_db, patch_batch):
    """Test filtering clients by email via CLI."""
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-field", "email", "--filter-value", "john.doe@example.com"])
    # print(result.output)
    assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
    assert "Email: john.doe@example.com" in result.output
    assert "John" in result.output


def test_filter_by_name(cli_runner, sample_client, test_db, patch_batch):
    """Test filtering clients by first_name via CLI."""
    
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-field", "first_name", "--filter-value", "John"])

    assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
    assert "John" in result.output
    assert "Doe" in result.output


def test_filter_invalid_field(cli_runner, test_db, patch_batch):
    """Test invalid field argument."""
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-field", "invalid_field", "--filter-value", "John"])

    assert result.exit_code != 0
    assert "Invalid field" in result.output


def test_filter_invalid_value(cli_runner, sample_client, test_db, patch_batch):
    """Test invalid value format for filtering."""
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-field", "email", "--filter-value", "invalid@email.com"])

    assert result.exit_code == 0
    assert "No clients found" in result.output


def test_filter_by_multiple_fields(cli_runner, sample_client, test_db, patch_batch):
    """Test filtering by multiple fields (e.g., first_name and email)."""
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-field", "first_name", "--filter-value", "John"])

    assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
    assert "John" in result.output
    assert "Doe" in result.output


def test_filter_value_only(cli_runner, sample_client, test_db, patch_batch):
    """Test filtering when only the filter_value is provided."""
    result = cli_runner.invoke(cli, ["clients", "list", "--filter-value", "Doe"])

    assert result.exit_code == 0, f"Command failed with exit code {result.exit_code}"
    assert "First name: John" in result.output
