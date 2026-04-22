# 🏠 Apartment Tracker — Django

A production-grade Django web app for roommates to collaboratively track, rate, and compare apartment listings — backed by a PostgreSQL database. Converted from a Streamlit prototype to a full Django application with user authentication.

## Live App
🔗 [https://your-username.pythonanywhere.com](https://your-username.pythonanywhere.com)

## ERD
![ERD](erd.png)

## What it does
- **Dashboard** — Summary metrics and filterable apartment card grid
- **Apartments** — Full CRUD with search, image display, amenity tracking
- **Roommates** — Manage who is in the search group
- **Rate** — Each roommate rates each apartment 1–5 stars with a comment
- **Compare** — Side-by-side comparison of any two apartments
- **Login** — Django's built-in authentication protects all pages

## Tech Stack
- Python / Django 4.2
- PostgreSQL (hosted on Retool)
- Bootstrap 5
- Deployed on PythonAnywhere

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/apartment-tracker-django.git
cd apartment-tracker-django
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy `.env.example` to `.env` and fill in your database credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
DJANGO_SECRET_KEY=any-long-random-string
DEBUG=True
DB_NAME=retool
DB_USER=retool
DB_PASSWORD=your-password
DB_HOST=your-host.retooldb.com
DB_PORT=5432
```

### 5. Run migrations (maps Django models to existing tables)
```bash
python manage.py migrate --fake-initial
```

### 6. Create a superuser (for login)
```bash
python manage.py createsuperuser
```

### 7. Run the app
```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) and log in with the superuser you created.

---

## Deploying to PythonAnywhere

1. Create a free account at [pythonanywhere.com](https://pythonanywhere.com)
2. Open a **Bash console** and run:
```bash
git clone https://github.com/YOUR_USERNAME/apartment-tracker-django.git
cd apartment-tracker-django
pip install -r requirements.txt
```
3. Create a `.env` file with your production credentials
4. Go to **Web** tab → **Add a new web app** → **Manual configuration** → **Python 3.10**
5. Set the virtualenv path and WSGI file path
6. In the WSGI file, point to your project's `wsgi.py`
7. Set `DEBUG=False` and add your PythonAnywhere domain to `ALLOWED_HOSTS` in settings
8. Reload the app

---

## Tables

### `apartments`
Stores each listing with rent, beds/baths, amenity flags, and an optional image URL.

### `roommates`
Stores the people participating in the apartment search, identified by name and unique email.

### `ratings` (junction table)
Links apartments and roommates many-to-many. One rating per roommate per apartment, enforced by a unique constraint. Stores a 1–5 score and optional comment.
