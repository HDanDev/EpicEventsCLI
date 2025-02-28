from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from crm.models.base import Base


class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    collaborators = relationship('Collaborator', backref='role')

    def __repr__(self):
        return f"<Role {self.name}>"


class RoleEnum(PyEnum):
    SALES = 1
    SUPPORT = 2
    MANAGEMENT = 3
