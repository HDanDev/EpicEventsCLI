from crm.database import Base, engine, SessionLocal
from crm.models.roles import Role
from crm.models.collaborators import Collaborator
from sqlalchemy import text, inspect  # ✅ Fix for SQLAlchemy 2.0+
import os
import bcrypt

print("🔹 Step 1: Checking database connection...")

# 1️⃣ Create tables
try:
    print("📌 Creating tables in the database...")
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
    print("✅ Tables created successfully!")

    # Check if tables exist
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    print(f"🔍 Existing tables in database: {existing_tables}")

    if "roles" not in existing_tables or "collaborators" not in existing_tables:
        print("❌ ERROR: Required tables were NOT created!")
        exit(1)
except Exception as e:
    print(f"❌ ERROR creating tables: {e}")
    exit(1)

# 2️⃣ Create a session
session = SessionLocal()

# 3️⃣ Check database connection
try:
    session.execute(text("SELECT 1"))  # ✅ Corrected for SQLAlchemy 2.0+
    print("✅ Database connection is working!")
except Exception as e:
    print(f"❌ ERROR: Cannot connect to database! {e}")
    exit(1)

# 4️⃣ Insert Roles first
print("📌 Checking roles in the database...")
roles = [
    Role(id=1, name="Sales"),
    Role(id=2, name="Support"),
    Role(id=3, name="Management")
]

for role in roles:
    exists = session.query(Role).filter_by(id=role.id).first()
    if exists:
        print(f"✅ Role '{role.name}' already exists.")
    else:
        print(f"➕ Adding role '{role.name}'...")
        session.add(role)

# 5️⃣ Insert Main Manager **after roles exist**
print("📌 Checking users in the database...")

# Get environment variables
main_manager_email = os.getenv('MAIN_MANAGER_EMAIL')
main_manager_password = bcrypt.hashpw(os.getenv('MAIN_MANAGER_PASSWORD').encode(), bcrypt.gensalt()).decode()

if not main_manager_email or not main_manager_password:
    print("⚠️ WARNING: Environment variables for MAIN_MANAGER are missing!")

users = [
    Collaborator(first_name="Main", last_name="Manager",
                 email=main_manager_email,
                 password_hash=main_manager_password,
                 role_id=3)
]

for user in users:
    exists = session.query(Collaborator).filter_by(email=user.email).first()
    if exists:
        print(f"✅ User '{user.email}' already exists.")
    else:
        print(f"➕ Adding user '{user.email}'...")
        session.add(user)

# 6️⃣ Commit and close session
try:
    session.commit()
    print("✅ Database initialized with default data!")
except Exception as e:
    print(f"❌ ERROR committing to database: {e}")
finally:
    session.close()
