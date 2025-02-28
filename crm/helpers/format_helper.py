from datetime import datetime
from bcrypt import hashpw, gensalt


class FormatHelper:
    def format_date(date: str) -> datetime:
        """Convert 'DD/MM/YYYY-HHhMM' to a Python datetime object."""
        return datetime.strptime(date, "%d/%m/%Y-%Hh%M")
    
    def hash_password(password: str) -> str:
        """Hashes the password securely."""
        return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')