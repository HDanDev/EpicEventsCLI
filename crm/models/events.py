from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
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
    
    @property
    def infos(self):
        """Returns a string representation of the event."""
        return (
            f"""
            ID: {self.id}
            Name: {self.name}
            Start date: {self.start_date.isoformat() if self.start_date else None}
            End date: {self.end_date.isoformat() if self.end_date else None}
            Location: {self.location}
            Number of attendees: {self.attendees}
            Additional notes: {self.notes}
            Related contract ID: {self.contract_id}
            Related support ID: {self.support_id}
            """
            )
        
    @property
    def minimal_infos(self):
        """Returns a succint string representation of the event."""
        return (
            f"""
            ID: {self.id}
            Name: {self.name}
            End date: {self.end_date.isoformat() if self.end_date else None}
            Related support ID: {self.support_id}
            """
            )

    def __repr__(self):
        return f"<Event {self.name} (Contract ID: {self.contract_id})>"
