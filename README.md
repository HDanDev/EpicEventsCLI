# EpicEvents
12th OC project "Develop a securized bakend architecture using Python and Sql"

## Installation Guide

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.9 or later
- pip (Python package manager)
- virtualenv (optional but recommended)
- PostgreSQL (or your preferred database)

### Setting Up the Project

#### 1. Clone the Repository
```sh
git clone https://github.com/HDanDev/EpicEvents.git
cd EpicEvents
```

#### 2. Create and Activate Virtual Environment

```sh
python -m venv venv
```
On Windows:
```sh
venv\Scripts\activate
```
On macOS/Linux:
```sh
source venv/bin/activate
```

#### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file at the root of the project and add the necessary configurations:
```ini
DATABASE_URL=
HASH_SECRET_KEY=
MAIN_MANAGER_EMAIL=
MAIN_MANAGER_PASSWORD=
APP_SECRET_KEY=
SENTRY_URL=
KEYRING_SERVICE=
```

#### 5. Initialize Database
```sh
python init-db.py
```

#### 6. Run Commands
Authentication Commands:
```sh
python crm/cli/main.py auth login
```
```sh
python crm/cli/main.py auth logout
```

The default main manager user credentials are those specified in the .env file (cf. **MAIN_MANAGER_EMAIL** and **MAIN_MANAGER_PASSWORD**)

Collaborators Commands:
```sh
python crm/cli/main.py collaborators add
```
```sh
python crm/cli/main.py collaborators view
```
```sh
python crm/cli/main.py collaborators list
```
```sh
python crm/cli/main.py collaborators edit
```
```sh
python crm/cli/main.py collaborators edit_password
```
```sh
python crm/cli/main.py collaborators delete
```

Clients Commands:
```sh
python crm/cli/main.py clients add
```
```sh
python crm/cli/main.py clients view
```
```sh
python crm/cli/main.py clients list
```
```sh
python crm/cli/main.py clients edit
```
```sh
python crm/cli/main.py clients delete
```

Contracts Commands:
```sh
python crm/cli/main.py contracts add
```
```sh
python crm/cli/main.py contracts view
```
```sh
python crm/cli/main.py contracts list
```
```sh
python crm/cli/main.py contracts edit
```
```sh
python crm/cli/main.py contracts delete
```

Events Commands:
```sh
python crm/cli/main.py events add
```
```sh
python crm/cli/main.py events view
```
```sh
python crm/cli/main.py events list
```
```sh
python crm/cli/main.py events edit
```
```sh
python crm/cli/main.py events delete
```

Alternatively you can get all the command using your integrated terminal:
```sh
python crm/cli/main.py --help
```
Then ask for a specific command using:
```sh
python crm/cli/main.py [Specific command e.g. "auth"] --help
```

#### 7. Run Tests with Pytest
```sh
pytest -s
```
If for some reason you're facing issues with the command above try the following:
```sh
$env:PYTHONPATH = (Get-Location).Path
>> pytest -s
```

## Features
- User Authentication and Role-Based Access Control
- Manage Collaborators, Clients, Contracts, and Events
- Secure Data Handling with SQLAlchemy
- Logging and Error Tracking with Sentry



