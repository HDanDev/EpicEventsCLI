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
    
    def __repr__(self):
        return f"<Client {self.full_name} from {self.company_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "company_name": self.company_name,
            "first_contact_date": self.first_contact_date.isoformat() if self.first_contact_date else None,
            "last_contact_date": self.last_contact_date.isoformat() if self.last_contact_date else None,
            "contracts": [contract.to_dict() for contract in self.contracts] if self.contracts else [],
            "commercial_id": self.commercial_id,
        }
        
    def minimal_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "commercial_id": self.commercial_id
        }