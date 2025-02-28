from crm.database import engine

print(f"🔍 Database URL in use: {engine.url}")

from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        print(f"✅ Connected to database: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ ERROR: Could not connect to database! {e}")
