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
```bash
cp .env.example .env
```
Edit `.env` with your database credentials.

### 5. Run migrations
```bash
python manage.py migrate --fake-initial
```

### 6. Create a login account
```bash
python manage.py createsuperuser
```

### 7. Run the app
```bash
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000)

## Tables

### `apartments`
Stores each listing with rent, beds/baths, amenity flags, and an optional image URL.

### `roommates`
Stores the people participating in the apartment search, identified by name and unique email.

### `ratings` (junction table)
Links apartments and roommates many-to-many. One rating per roommate per apartment. Stores a 1–5 score and optional comment.
