from sqlalchemy import Column, Integer, String, DateTime, func
from crm.models.base import Base


class BlacklistToken(Base):
    __tablename__ = 'blacklist_tokens'

    id = Column(Integer, primary_key=True)
    token = Column(String(500), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"<BlacklistToken {self.token}>"
