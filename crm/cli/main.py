import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import click
from crm.cli.collaborators import collaborators
from crm.cli.clients import clients
from crm.cli.contracts import contracts
from crm.cli.events import events
from crm.cli.auth import auth
from config import sentry_sdk


@click.group()
def cli():
    """Epic Events CLI"""
    pass

cli.add_command(auth)
cli.add_command(collaborators)
cli.add_command(clients)
cli.add_command(contracts)
cli.add_command(events)

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise
