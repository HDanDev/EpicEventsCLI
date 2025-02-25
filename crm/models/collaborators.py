from sqlalchemy import Column, Integer, String, ForeignKey
from bcrypt import checkpw
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
        """Returns the full name of the collaborator."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def infos(self):
        """Returns a string representation of the collaborator."""
        return (
            f"""
            ID: {self.id}
            First name: {self.first_name}
            Last name: {self.last_name}
            Email: {self.email}
            Role ID: {self.role_id}
            """
            )
        
    @property
    def minimal_infos(self):
        """Returns a succint string representation of the collaborator."""
        return self.infos

    def __repr__(self):
        return f"<Collaborator {self.full_name} (Role ID: {self.role_id})>"    

    def check_password(self, password):
        """Verifies the provided password against the stored hash."""
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

