from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DateField, DateTimeField, FloatField, SelectField, SubmitField,EmailField,FileField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email, Length

class Login(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Login')