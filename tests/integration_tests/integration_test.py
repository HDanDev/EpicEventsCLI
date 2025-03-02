import pytest
from unittest.mock import patch
from crm.cli.main import cli
from crm.models import Collaborator, Client, Contract, Event
from datetime import datetime
from tests.test_context_db import test_db, cli_runner, test_manager_email, password
import keyring
from config import KEYRING_SERVICE

def test_full_integration_flow(cli_runner, test_db):
    """Full test covering login, creating entities, and deleting them."""
    # 🔹 Apply DB fixture patches
    with (
        patch("crm.cli.auth.DB", test_db),
        patch("crm.cli.clients.DB", test_db),
        patch("crm.cli.collaborators.DB", test_db),
        patch("crm.cli.contracts.DB", test_db),
        patch("crm.cli.events.DB", test_db),
        patch("crm.helpers.authorize_helper.DB", test_db),
    ):
        ## Step 1: Login as manager
        result = cli_runner.invoke(cli, ["auth", "login"], input=f"{test_manager_email}\n{password}\n")
        assert "✅ Login successful!" in result.output

        ## Step 2: Create sales and support collaborators
        result = cli_runner.invoke(cli, ["collaborators", "add"], input=f"John\nDoe\njohn.doe@email.com\n{password}\n{password}\n1\n")
        assert "✅ Collaborator John Doe created!" in result.output
        sales_collaborator_id = test_db.query(Collaborator).filter_by(email="john.doe@email.com").first().id

        result = cli_runner.invoke(cli, ["collaborators", "add"], input=f"Jane\nSmith\njane.smith@email.com\n{password}\n{password}\n2\n")
        assert "✅ Collaborator Jane Smith created!" in result.output
        support_collaborator_id = test_db.query(Collaborator).filter_by(email="jane.smith@email.com").first().id

        ## Step 3: Get all collaborators
        result = cli_runner.invoke(cli, ["collaborators", "list"])
        assert "Email: john.doe@email.com" in result.output
        assert "Email: jane.smith@email.com" in result.output

        ## Step 4: Edit collaborator
        result = cli_runner.invoke(cli, [
            "collaborators", "edit", str(sales_collaborator_id),
            "--first-name", "John",
            "--last-name", "D.",
            "--email", "john.d@email.com",
            "--role-id", "1"
            ])
        assert f"✅ Collaborator {sales_collaborator_id}" in result.output

        ## Step 5: Login as new sales
        result = cli_runner.invoke(cli, ["auth", "login"], input=f"john.d@email.com\n{password}\n")
        assert "✅ Login successful!" in result.output

        ## Step 6: Create a client
        result = cli_runner.invoke(cli, ["clients", "add"], input="Alice\nJohnson\nalice@email.com\n123456789\nAliceCorp\n")
        assert "✅ Client" in result.output
        client_id = test_db.query(Client).filter_by(email="alice@email.com").first().id

        ## Step 7: Get all clients
        result = cli_runner.invoke(cli, ["clients", "list"])
        assert "Email: alice@email.com" in result.output

        ## Step 8: Login as manager & create contract
        cli_runner.invoke(cli, ["auth", "login"], input=f"{test_manager_email}\n{password}\n")
        result = cli_runner.invoke(cli, ["contracts", "add"], input="1000.0\n500.0\nFalse\n{}\n{}\n".format(client_id, sales_collaborator_id))
        assert "✅ Contract" in result.output
        contract_id = test_db.query(Contract).filter_by(client_id=client_id).first().id

        ## Step 9: Login as sales & get contract
        cli_runner.invoke(cli, ["auth", "login"], input=f"john.d@email.com\n{password}\n")
        result = cli_runner.invoke(cli, ["contracts", "list"])
        assert str(contract_id) in result.output

        ## Step 10: Edit contract
        result = cli_runner.invoke(cli, ["contracts", "edit", str(contract_id)], input="1500.0\n300.0\nTrue\n{}\n{}\n".format(client_id, sales_collaborator_id))
        assert "✅ Contract" in result.output

        ## Step 11: Get all contracts
        result = cli_runner.invoke(cli, ["contracts", "list"])
        assert "Costing: 1500.0" in result.output

        ## Step 12: Create event for contract
        result = cli_runner.invoke(cli, ["events", "add"], input="Test event\n20 Saint-Louis, 1000 Paris, France\n50\nA test event comment\n{}\n01/03/2025-12h00\n02/03/2025-18h00\n0\n".format(contract_id))
        assert "✅ Event" in result.output
        event_id = test_db.query(Event).filter_by(contract_id=contract_id).first().id

        ## Step 13: Login as manager & assign support to event
        cli_runner.invoke(cli, ["auth", "login"], input=f"{test_manager_email}\n{password}\n")
        result = cli_runner.invoke(cli, ["events", "edit", str(event_id)], input="Test event\n20 Saint-Louis, 1000 Paris, France\n50\nA test event comment\n{}\n01/03/2025-12h00\n02/03/2025-18h00\n{}\n".format(contract_id, support_collaborator_id))
        assert "✅ Event" in result.output

        ## Step 14: Login as support & view event
        cli_runner.invoke(cli, ["auth", "login"], input=f"jane.smith@email.com\n{password}\n")
        result = cli_runner.invoke(cli, ["events", "list"])
        assert str(event_id) in result.output

        ## Step 15: Edit event details
        result = cli_runner.invoke(cli, ["events", "edit", str(event_id)], input="Updated Event\n86 Walburge, 250 Bruxelles, Belgium\n100\nUpdated event comment\n{}\n10/10/2026-16h00\n15/11/2027-20h15\n{}\n".format(contract_id, support_collaborator_id))
        assert "✅ Event" in result.output

        ## Step 16: Login as sales & delete event
        cli_runner.invoke(cli, ["auth", "login"], input=f"john.d@email.com\n{password}\n")
        result = cli_runner.invoke(cli, ["events", "delete", str(event_id)])
        assert "✅ Event" in result.output

        ## Step 17: Delete contract & client
        result = cli_runner.invoke(cli, ["contracts", "delete", str(contract_id)])
        assert "✅ Contract" in result.output

        result = cli_runner.invoke(cli, ["clients", "delete", str(client_id)])
        assert "✅ Client" in result.output

        ## Step 18 Login as manager & delete collaborator
        cli_runner.invoke(cli, ["auth", "login"], input=f"{test_manager_email}\n{password}\n")
        result = cli_runner.invoke(cli, ["collaborators", "delete", str(support_collaborator_id)])
        assert "✅ Collaborator" in result.output

        test_db.close()
