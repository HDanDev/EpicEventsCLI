from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from crm.models.base import Base
from datetime import datetime, timezone


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False) 
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=False)
    first_contact_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_contact_date = Column(DateTime)
    
    commercial_id = Column(Integer, ForeignKey('collaborators.id'))

    commercial = relationship("Collaborator")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def infos(self):
        """Returns a string representation of the client."""
        return (
            f"""
            ID: {self.id}
            First name: {self.first_name}
            Last name: {self.last_name}
            Email: {self.email}
            Phone number: {self.phone}
            Company name: {self.company_name}
            First contact date: {self.first_contact_date.isoformat() if self.first_contact_date else None}
            Last contact date: {self.last_contact_date.isoformat() if self.last_contact_date else None}
            Related collaborator ID: {self.commercial_id}
            """
            )
        
    @property
    def minimal_infos(self):
        """Returns a succint string representation of the client."""
        return (
            f"""
            ID: {self.id}
            First name: {self.first_name}
            Last name: {self.last_name}
            Email: {self.email}
            Related collaborator ID: {self.commercial_id}
            """
            )
    
    def __repr__(self):
        return f"<Client {self.full_name} from {self.company_name}>"