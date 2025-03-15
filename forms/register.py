from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DateField, DateTimeField, FloatField, SelectField, SubmitField,EmailField,FileField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, Length, ValidationError

from models import User


class UserForm(FlaskForm):
    first_name = StringField('FirstName', validators=[DataRequired()])
    last_name = StringField('LastName', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add User')


