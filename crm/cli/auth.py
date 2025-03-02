import click
from crm.services.auth import login_service, logout_service
from crm.database import DB

@click.group()
def auth():
    """Manage authentication"""
    pass

@click.command()
@click.option("--email", prompt=True, help="Your email")
@click.option("--password", prompt=True, confirmation_prompt=False, help="Your password")
def login(email, password):
    """Log in to the CRM system"""
    user, error = login_service(DB, email, password)
    if error:
        click.echo(error)
        return
    click.echo(f"✅ Login successful! Logged in as {user.full_name}!")

@click.command()
def logout():
    """Log out of the CRM system"""
    error = logout_service(DB)
    
    if error:
        click.echo(error)
        return
    click.echo("✅ Successfully logged out!")

auth.add_command(login)
auth.add_command(logout)
