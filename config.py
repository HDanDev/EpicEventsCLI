import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("APP_SECRET_KEY", "supersecretkey")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm.db")
KEYRING_SERVICE = os.getenv("KEYRING_SERVICE", "keyringservice")
