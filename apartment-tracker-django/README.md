# 🏠 Apartment Tracker — Django

A production-grade Django web app for roommates to collaboratively track, rate, and compare apartment listings — backed by a PostgreSQL database. Converted from a Streamlit prototype to a full Django application with user authentication.

## Live App
🔗 [https://frxncescxx.pythonanywhere.com](https://frxncescxx.pythonanywhere.com)

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

### reflection
My main goal for this project was to flush out my project from a previous assignment. I created an app that allows users to add apartment/housing listings from online platforms and store them on the app. There each user is able to create an account where they can then rate and comment on each housing listing and compare different one’s side to side. The app saves entries from different users, roommates, so that everyone is able to see one another’s thoughts and opinions on specific listings.  The reason I chose this idea is because since graduation is coming up, I am looking to find housing in the greater Seattle area for my roommate and I. Instead of having to pull up multiple listings in different windows this app allows us to see everything clearly in through a simple UI.
When working on this assignment I was able to implement everything that I wanted in it and made a deployable app through pythonanywhere and Django. The only drawback is that the account create occurs in terminal and not on the website itself. If I had more time, I would definitely fix that because it makes things a bit harder for people to use. Especially if they do not know how to use GitHub. Despite that, this project went pretty well for me and the only issues I had was making my project live on pythonanywhere.
I wish we learned more how to code on our own in this class and had more time for these projects because, I do enjoy the help from AI, but it is not as fulfilling as knowing I coded this project on my own. So, something I would do differently if given the skill and time would be to work on this project with minimal AI usage, but right now I just do not have the skill to do so.
