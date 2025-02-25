from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from crm.models.base import Base

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)
    
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    support_id = Column(Integer, ForeignKey('collaborators.id'))

    contract = relationship("Contract")
    support = relationship("Collaborator")

    def __repr__(self):
        return f"<Event {self.name} (Contract ID: {self.contract_id})>"

    def set_start_date(self, date):
        self.start_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        
    def set_end_date(self, date):
        self.end_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "location": self.location,
            "attendees": self.attendees,
            "notes": self.notes,
            "contract_id": self.contract_id,
            "support_id": self.support_id,
        }
        
    def minimal_to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "contract_id": self.contract_id,
            "support_id": self.support_id
        }
