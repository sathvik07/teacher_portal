# Django Teacher Portal

A simple teacher portal to manage students, built with Django, HTML, and JavaScript.

## Features

- Secure login for teachers
- Add new students
- Merge marks for same student + subject
- Inline edit & delete student records
- Teacher-specific student filtering

## Tech Stack

- Python 3.x
- Django 4.x
- HTML/CSS/JS (vanilla)

##️ How to Run

Clone the repo: 
```bash
git clone https://github.com/yourusername/teacher-portal.git
cd teacher-portal
```

Set up a virtual environment (optional but recommended):
```bash
python -m venv env
source env/bin/activate # On Windows: env\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

Run the development server:
```bash
python manage.py runserver
```

Open your browser and go to Visit: `http://127.0.0.1:8000/`
