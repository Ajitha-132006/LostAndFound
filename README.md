# Lost and Found Portal (Django)

This project is a web-based Lost and Found Portal built with Django.

## Features

- User registration, login, and logout
- Post lost/found items with optional image upload
- Browse and filter items by status/category
- Search by title, description, and location
- Mark an item as resolved
- Admin panel support for moderation

## Project Structure

```text
lost_and_found/
├── manage.py
├── requirements.txt
├── db.sqlite3                 # Created after first migrate
├── media/                     # Uploaded images
├── static/
│   └── css/style.css
├── templates/
│   ├── base.html
│   ├── registration/
│   │   ├── login.html
│   │   └── register.html
│   └── portal/
│       ├── landing.html
│       ├── dashboard.html
│       ├── item_detail.html
│       ├── item_form.html
│       ├── item_list.html
│       └── my_items.html
├── lost_and_found_portal/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── portal/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── migrations/
        └── __init__.py
```

## Setup

1. Create and activate virtual environment:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Run migrations:
```powershell
python manage.py makemigrations
python manage.py migrate
```

4. Create admin user:
```powershell
python manage.py createsuperuser
ajitha,wpllab
```

5. Start server:
```powershell
python manage.py runserver
```

Open:
- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

sarvani
sarvani@gmail
JZAuQWKf!5_8782