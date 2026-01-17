# Flask Notes App

A simple web-based Notes application built with **Python Flask** and **MySQL**, allowing users to:
- Register and login securely
- Add, edit, and delete notes
- View their personal dashboard
- Enjoy password strength and email validation

## Features

- User authentication (register/login/logout)
- Password hashing & strength validation
- Email format validation
- CRUD operations for notes (Create, Read, Update, Delete)
- Flash messages for feedback
- Responsive dashboard with dynamic note display

## Tech Stack

- Python 3.10+
- Flask
- MySQL (via mysql-connector-python)
- HTML / CSS / JS (frontend)
- Jinja2 templates
- Werkzeug (password hashing)

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flask-notes-app.git
cd flask-notes-app

2.Create a virtual environment:
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

Install dependencies:

pip install -r requirements.txt


Set up MySQL database:

Create a database named users

Update db.py with your MySQL credentials

Run the app:

python app.py


Open in browse
