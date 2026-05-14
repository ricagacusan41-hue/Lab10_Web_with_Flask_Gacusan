from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[InputRequired(), Length(max=50)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Log In")


class ProfileForm(FlaskForm):
    display_name = StringField("Display Name", validators=[InputRequired()])
    section = StringField("Section")
    sex = SelectField("Sex", choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    image = FileField("Profile Picture")
    submit = SubmitField("Save Changes")
