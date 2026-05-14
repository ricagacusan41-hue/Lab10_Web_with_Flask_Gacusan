from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin_email = 'admin@example.com'
    admin_password = 'adminpass'
    admin_display = 'Admin'

    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print('Admin already exists:', existing.email)
    else:
        admin = User(
            email=admin_email,
            password=generate_password_hash(admin_password),
            role='admin',
            display_name=admin_display
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin created:', admin_email)
