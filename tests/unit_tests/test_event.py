import pytest
from sqlalchemy.orm import Session
from crm.models.events import Event
from crm.models.contracts import Contract
from crm.helpers.format_helper import FormatHelper
from crm.services.events import create_event, get_event, get_all_events, update_event, delete_event
from tests.test_context_db import test_db, test_manager_email
from unittest.mock import patch


@pytest.fixture
def sample_event(test_db: Session):
    """Fixture to create a sample event for testing."""
    test_contract = test_db.query(Contract).first()
    assert test_contract, "❌ No test contract found. Ensure test_db fixture is correctly set up."

    event = create_event(
        db=test_db,
        name="Sample Event",
        location="Town alley 10, 4000 Liege, Be",
        attendees=100,
        notes="This is a test event.",
        contract_id=test_contract.id,
        start_date="06/06/2030-18h30",
        end_date="07/06/2030-20h30",
        support_id=test_contract.commercial_id
    )
    test_db.commit()
    return event


def test_create_event(test_db):
    """Test event creation."""
    test_contract = test_db.query(Contract).first()
    assert test_contract, "❌ No test contract found."

    event = create_event(
        db=test_db,
        name="Test event",
        location="Bourg str 32, 200 Paris, Fr",
        attendees=250,
        notes="A test event for test purpose",
        contract_id=test_contract.id,
        start_date="06/06/2030-18h30",
        end_date="07/06/2030-20h30",
        support_id=test_contract.commercial_id
    )

    assert event.id is not None, "❌ Event ID should not be None"
    assert event.name == "Test event"
    assert event.location == "Bourg str 32, 200 Paris, Fr"
    assert event.attendees == 250
    assert event.notes == "A test event for test purpose"
    assert event.start_date == FormatHelper.format_date("06/06/2030-18h30")
    assert event.end_date == FormatHelper.format_date("07/06/2030-20h30")


def test_get_event(test_db, sample_event):
    """Test retrieving an event by ID."""
    retrieved_event = get_event(db=test_db, event_id=sample_event.id)

    assert retrieved_event is not None, "❌ Event should be found"
    assert retrieved_event.id == sample_event.id
    assert retrieved_event.name == "Sample Event"


def test_get_all_events(test_db):
    """Test retrieving all events."""
    mock_collaborator = type("Collaborator", (object,), {"id": 3, "role_id": 3})
    with (
        patch("crm.services.events.get_current_user", return_value=(mock_collaborator, None)),
    ):
        events = get_all_events(db=test_db, filter_field=None, filter_value=None)

        assert isinstance(events, list), "❌ Should return a list"
        assert len(events) > 0, "❌ At least one event should be present"


def test_update_event(test_db, sample_event):
    """Test updating an event's details."""
    updated_event = update_event(
        db=test_db,
        event_id=sample_event.id,
        location="Bruxelles",
        attendees=200
    )

    assert updated_event is not None, "❌ Event should exist"
    assert updated_event.location == "Bruxelles"
    assert updated_event.attendees == 200


def test_delete_event(test_db, sample_event):
    """Test deleting an event."""
    result = delete_event(db=test_db, event_id=sample_event.id)

    assert result is True, "❌ Event should be deleted"
    assert get_event(db=test_db, event_id=sample_event.id) is None, "❌ Event should not exist after deletion"
