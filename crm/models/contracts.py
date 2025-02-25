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
    
    @property
    def infos(self):
        """Returns a string representation of the contract."""
        return (
            f"""
            ID: {self.id}
            Costing: {self.costing}
            Remaining due payment: {self.remaining_due_payment}
            Creation date: {self.creation_date.isoformat() if self.creation_date else None}
            Is signed: {self.is_signed}
            Related client ID: {self.client_id}
            Related commercial ID: {self.commercial_id}
            """
            )
        
    @property
    def minimal_infos(self):
        """Returns a succint string representation of the contract."""
        return (
            f"""
            ID: {self.id}
            Related client ID: {self.client_id}
            Related commercial ID: {self.commercial_id}
            """
            )

    def __repr__(self):
        return f"<Contract {self.id} for Client {self.client_id}>"