import click
from crm.services.auth import login_service, logout_service
from crm.database import SessionLocal

@click.group()
def auth():
    """Manage authentication"""
    pass

@click.command()
@click.option("--email", prompt=True, help="Your email")
@click.option("--password", prompt=True, confirmation_prompt=False, help="Your password")
def login(email, password):
    """Log in to the CRM system"""
    db = SessionLocal()
    user, error = login_service(db, email, password)
    if error:
        click.echo(error)
        return
    click.echo(f"✅ Logged in as {user.full_name}!")

@click.command()
def logout():
    """Log out of the CRM system"""
    db = SessionLocal()
    error = logout_service(db)
    
    if error:
        click.echo(error)
        return
    click.echo("✅ Successfully logged out!")

auth.add_command(login)
auth.add_command(logout)
