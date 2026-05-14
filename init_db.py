import os
from app import app
from models import db

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

with app.app_context():
    db.create_all()
    print("Database initialized and ready.")
