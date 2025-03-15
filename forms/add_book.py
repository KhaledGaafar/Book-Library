from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, DateField, DateTimeField, FloatField, SelectField, SubmitField,EmailField,FileField,URLField
from wtforms.validators import DataRequired, Email, Length


class BookForm(FlaskForm):
    name = StringField('BookName', validators=[DataRequired()])
    publish_date= DateField('Publish Date', format='%Y-%m-%d', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    appropriate = SelectField('Appropriate For', choices=[
        ('under 8', 'Under 8'),
        ('8-15', '8-15'),
        ('adults', 'Adults')
    ], validators=[DataRequired()])
    user_id = SelectField('Author', coerce=int, validators=[DataRequired()])
    #image= URLField('Book Image')
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Book')