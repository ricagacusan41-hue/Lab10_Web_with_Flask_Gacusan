# Flask App Demo

This is a simple Flask web application with user registration, login, profile editing, and student management.

## Features

- User registration and login using `Flask-Login`
- Password hashing with `werkzeug.security`
- SQLite database via `Flask-SQLAlchemy`
- Profile page with photo upload and profile details
- Admin-only student management pages
- Jinja2 templates and static assets for UI

## Getting Started

### Prerequisites

- Python 3.8+ installed
- A virtual environment (`venv`) is recommended

### Install dependencies

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

### Default admin user

The app creates a default admin user automatically on first run.

- Email: `admin@example.com`
- Password: `adminpass`

You can override these values with environment variables before running the app:

```bash
set ADMIN_EMAIL=your-admin@example.com
set ADMIN_PASSWORD=yourpassword
python app.py
```

## Uploading to GitHub

1. Create a new repository on GitHub.
2. In your local project root (`c:\Users\Azriel\flask_app`):

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/your-repo-name.git
git branch -M main
git push -u origin main
```

3. Make sure `.gitignore` includes `venv/`, `instance/`, `__pycache__/`, `*.pyc`, and `.env`.

## Notes

- Keep sensitive data like `SECRET_KEY` and database credentials out of source control.
- Use `instance/` or environment variables for production configuration.
