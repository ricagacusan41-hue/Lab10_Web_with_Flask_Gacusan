from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

from forms import RegisterForm, LoginForm, ProfileForm
from models import db, User, Student

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Ensure the database has an admin user when the app starts.
def ensure_admin_user():
    admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'adminpass')
    existing_admin = User.query.filter_by(role='admin').first()
    if existing_admin:
        return

    existing_user = User.query.filter_by(email=admin_email).first()
    if existing_user:
        existing_user.role = 'admin'
        existing_user.display_name = existing_user.display_name or 'Admin'
        db.session.commit()
        print(f"Updated existing user to admin: {admin_email}")
        return

    admin = User(
        email=admin_email,
        password=generate_password_hash(admin_password),
        role='admin',
        display_name='Admin'
    )
    db.session.add(admin)
    db.session.commit()
    print(f"Created default admin: {admin_email}")

# ✅ Fixed: use db.session.get instead of deprecated Query.get
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

_database_initialized = False

@app.before_request
def initialize_database():
    global _database_initialized
    if _database_initialized:
        return
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    db.create_all()
    ensure_admin_user()
    _database_initialized = True

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(
            email=form.email.data,
            password=hashed_password,
            display_name=form.full_name.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('profile'))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('home'))

@app.route('/students')
@login_required
def students():
    student_list = Student.query.order_by(Student.full_name).all()
    # Attach user profile info to each student
    for student in student_list:
        user = User.query.filter_by(email=student.email).first()
        if user:
            student.user_image = user.image_filename
            student.user_section = getattr(user, "section", None)
            student.user_sex = user.sex
    return render_template('students.html', students=student_list)

@app.route('/add-student', methods=['POST'])
@login_required
def add_student():
    if current_user.role != 'admin':
        flash("Permission denied.")
        return redirect(url_for('students'))
    name = request.form.get('name')
    email = request.form.get('email')
    if not name or not email:
        flash("Name and email required.")
        return redirect(url_for('students'))
    student = Student(full_name=name, email=email)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/delete-student/<int:id>')
@login_required
def delete_student(id):
    if current_user.role != 'admin':
        flash("Permission denied.")
        return redirect(url_for('students'))
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/remove_photo', methods=['POST'])
@login_required
def remove_photo():
    current_user.image_filename = None   # clear the photo field
    db.session.commit()
    flash("Photo removed.")
    return redirect(url_for('profile'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if request.method == 'GET':
        form.display_name.data = current_user.display_name
        form.college.data = current_user.college
        form.sex.data = current_user.sex
    if form.validate_on_submit():
        if form.display_name.data:
            current_user.display_name = form.display_name.data
        if form.college.data:
            current_user.college = form.college.data
        if form.sex.data:
            current_user.sex = form.sex.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            upload_dir = os.path.join(app.static_folder, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            upload_path = os.path.join(upload_dir, filename)
            form.image.data.save(upload_path)
            current_user.image_filename = filename
        db.session.commit()
        flash("Profile updated.")
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

if __name__ == '__main__':
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    with app.app_context():
        db.create_all()
        ensure_admin_user()
    app.run(debug=True)
