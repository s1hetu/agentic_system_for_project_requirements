# scope-agency

## Project Setup

### Clone repo
```bash
    git clone https://github.com/s1hetu/agentic_system_for_project_requirements.git
```

### Create virtualenv
```bash
  python venv .venv
```

### Activate virtualenv
```bash
  source .venv/bin/activate
```

### Environmental Variables
- Create a .env file with variables defined in example.env and values.

### Install Requirements
```bash
  pip install -r requirements.txt
```

### Create and Run Migrations
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```

### Run Server
```bash
  python manage.py runserver
```