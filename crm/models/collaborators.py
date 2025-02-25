from sqlalchemy import Column, Integer, String, ForeignKey
from bcrypt import hashpw, gensalt, checkpw
from crm.models.base import Base

class Collaborator(Base):
    __tablename__ = "collaborators"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False) 
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"<Collaborator {self.full_name} (Role ID: {self.role_id})>"    

    def set_password(self, password):
        """Hashes and stores the password securely."""
        self.password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verifies the provided password against the stored hash."""
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Returns a dictionary representation of the collaborator."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role_id": self.role_id,
        }
        
    def minimal_to_dict(self):
        """Returns a minimal dictionary representation of the collaborator."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role_id": self.role_id,
        }
