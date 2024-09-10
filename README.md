# Social network parsing

### Setup environment
```
cd {{project_name}}

pyenv local 3.11

if we have pyproject.toml:

poetry shell
poetry install

or 

python3 -m venv .venv
source .venv/bin/activate - for macOs/Linux
\.venv\Scripts\activate.bat - for Windows

pip install -r requirements.txt

cat .env.example > .env
```

### Start app
```

uvicorn main:app --reload 

```

### Start create db and make migrations

1. Creating a database and user in PostgreSQL

psql -U postgres

-- User Creation
CREATE USER testuser WITH PASSWORD 'testpass';

-- Database creation
CREATE DATABASE testdb;

-- Assigning database rights to a user
GRANT ALL PRIVILEGES ON DATABASE testdb TO testuser;


2. Additionally, you can customize access rights to schemes and tables:

-- Assigning permissions to all schemes and tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO testuser;

3. Connect to the database using the created URL (All data with .env):

from sqlalchemy.engine import URL

db_url = URL.create(
    drivername="postgresql+asyncpg",
    username="testuser",
    password="testpass",
    host="localhost",
    port=5432,
    database="testdb"
)

4. Make migrations