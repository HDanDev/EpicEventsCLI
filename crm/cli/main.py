import click
from crm.cli.collaborators import collaborators
from crm.cli.auth import auth

@click.group()
def cli():
    """Epic Events CLI"""
    pass

cli.add_command(collaborators)
cli.add_command(auth)

if __name__ == "__main__":
    cli()
