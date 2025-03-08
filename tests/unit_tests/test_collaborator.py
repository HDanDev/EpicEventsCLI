import pytest
from unittest.mock import patch
from crm.models.roles import Role
from crm.models.collaborators import Collaborator
from tests.test_context_db import test_db, test_manager_email
from crm.services.collaborators import create_collaborator, get_collaborator, get_all_collaborators, update_collaborator, delete_collaborator
import bcrypt

def test_create_collaborator(test_db):
    password_hash = bcrypt.hashpw("testpassword".encode(), bcrypt.gensalt()).decode()
    collab = create_collaborator(test_db, "John", "Doe", "johndoe@email.com", password_hash, 1)
    assert collab.id is not None
    assert collab.first_name == "John"

def test_get_all_collaborator(test_db):
    mock_collaborator = type("Collaborator", (object,), {"id": 3, "role_id": 3})
    with (
        patch("crm.services.collaborators.get_current_user", return_value=(mock_collaborator, None)),
    ):
        collabs = get_all_collaborators(test_db, filter_field=None, filter_value=None)
        assert collabs is not None
        assert len(collabs) == 3

def test_get_collaborator(test_db):
    collab = get_collaborator(test_db, 1)
    assert collab is not None
    assert collab.email == test_manager_email

def test_update_collaborator(test_db):
    updated = update_collaborator(test_db, 1, first_name="Jane")
    assert updated is not None
    assert updated.first_name == "Jane"

def test_delete_collaborator(test_db):
    assert delete_collaborator(test_db, 1) is True
    assert get_collaborator(test_db, 1) is None