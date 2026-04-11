# Clinify - Clinic Management System
CPSC 471 - Group 27

---

## Setup

1. Get the `.env` file in the root folder
2. Create virtual environment and activate it
```bash 
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up the database (PostgreSQL must be installed)
```bash
psql -U postgres -f database/schema.sql
psql -U postgres -f database/seed.sql
```
5. Run
```bash
python manage.py runserver
```

---

## Project Files

| File/Folder | What it does |
|---|---|
| `config/settings.py` | Project config, database connection |
| `config/urls.py` | Entry point for all routes |
| `core/urls.py` | All 14 page routes |
| `core/views.py` | All logic for patient, doctor, admin |
| `core/models.py` | Raw SQL connection helper |
| `core/forms.py` | Login and register forms |
| `core/templates/core/` | All HTML pages |
| `static/css/style.css` | Styling |
| `static/js/script.js` | Frontend JS |
| `database/schema.sql` | PostgreSQL tables and stored procedures |
| `database/seed.sql` | Sample data for testing |