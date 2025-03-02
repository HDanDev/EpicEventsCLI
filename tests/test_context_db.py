import pytest
from sqlalchemy import create_engine, inspect
from click.testing import CliRunner
from sqlalchemy.orm import sessionmaker
from crm.models import Base
from crm.models.roles import Role
from crm.models.collaborators import Collaborator
from crm.models.clients import Client
from crm.models.contracts import Contract
from crm.models.events import Event
import bcrypt
from datetime import datetime

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

test_manager_email = "testmanager@email.com"
test_support_email = "testsupport@email.com"
test_commercial_email = "testcommercial@email.com"
test_client_email = "testclient@email.com"
password = "S3curedP@ssword"
hashed_password = bcrypt.hashpw("S3curedP@ssword".encode(), bcrypt.gensalt()).decode()

@pytest.fixture
def test_db():
    """Create a new test database for each test with default roles and users"""
    print("\n📌 Setting up test database...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"🔍 Existing tables: {existing_tables}")

    roles = [
        Role(id=1, name="Sales"),
        Role(id=2, name="Support"),
        Role(id=3, name="Management"),
    ]
    db.add_all(roles)
    try_commit(db, "Roles")
    
    role_check = (
        db.query(Role).filter_by(id=1).first() and
        db.query(Role).filter_by(id=2).first() and 
        db.query(Role).filter_by(id=3).first()
        )
    
    if not role_check:
        print("❌ ERROR: Roles do not exist before inserting user!")
        
    collaborators = [
        Collaborator(
            first_name="Test",
            last_name="Manager",
            email=test_manager_email,
            password_hash=hashed_password,
            role_id=3
        ),
        Collaborator(
            first_name="Test",
            last_name="Support",
            email=test_support_email,
            password_hash=hashed_password,
            role_id=2
        ),
        Collaborator(
            first_name="Test",
            last_name="Commercial",
            email=test_commercial_email,
            password_hash=hashed_password,
            role_id=1
        )
    ]
    
    db.add_all(collaborators)
    try_commit(db, "Collaborators")
    
    test_client = Client(
        first_name="Test",
        last_name="Client",
        email=test_client_email,
        phone="06600606",
        company_name="Test Company",
        commercial_id=collaborators[2].id
        )

    db.add(test_client)
    try_commit(db, "Client")
    
    test_contract = Contract(
        client_id=test_client.id,
        commercial_id=collaborators[2].id,
        costing=500.00,
        remaining_due_payment=500.00,
        creation_date=datetime.strptime("01/01/1900", "%d/%m/%Y"),
        is_signed=True
        )
    
    db.add(test_contract)
    try_commit(db, "Contract")
    
    test_event = Event(
        name="Test event",
        start_date=datetime.strptime("01/01/1900", "%d/%m/%Y"),
        end_date=datetime.strptime("02/01/1900", "%d/%m/%Y"),
        location="Paris",
        attendees=500,
        notes="A test event",
        contract_id=test_contract.id,
        support_id=collaborators[1].id
        )
    
    db.add(test_event)
    try_commit(db, "Event")

    all_users = db.query(Collaborator).all()
    print("✅ Existing users in DB:")
    for user in all_users:
        print(f"   - {user.first_name} {user.last_name}, Role ID: {user.role_id}")

    all_events = db.query(Event).all()
    print("✅ Existing events in DB:")
    for event in all_events:
        print(f"   - {event.name} {event.contract}, Role ID: {event.support}")

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
    print("\n✅ Test database cleaned up!")
    
def try_commit(db, model):
    try:
        db.commit()
        print(f"✅ {model} inserted successfully!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        db.rollback()

@pytest.fixture
def cli_runner():
    """Returns a Click CLI runner instance"""
    return CliRunner()
