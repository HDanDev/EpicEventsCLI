from sqlalchemy import Column, Integer, Boolean, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from crm.models.base import Base
from datetime import datetime, timezone


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    commercial_id = Column(Integer, ForeignKey("collaborators.id"), nullable=False)
    costing = Column(Float, nullable=False)
    remaining_due_payment = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_signed = Column(Boolean, default=False)

    client = relationship("Client")
    commercial = relationship("Collaborator")

    def __repr__(self):
        return f"<Contract {self.id} for Client {self.client_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "costing": self.costing,
            "remaining_due_payment": self.remaining_due_payment,
            "creation_date": self.creation_date.isoformat() if self.creation_date else None,
            "signed": self.signed,
            "client_id": self.client_id,
            "commercial_id": self.commercial_id,
            "events": [event.to_dict() for event in self.events] if self.events else [],
        }
        
    def minimal_to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "commercial_id": self.commercial_id
        }