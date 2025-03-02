from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from crm.models import Base

from crm.models.roles import Role
from crm.models.collaborators import Collaborator
from crm.models.clients import Client
from crm.models.contracts import Contract
from crm.models.events import Event

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DB = SessionLocal()
