from datetime import datetime
from flask_login import UserMixin


from database import db



class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    image = db.Column(db.String(20), nullable=True,default='images/photo.jpg')



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    publish_date= db.Column(db.DateTime, nullable=False)
    created_at= db.Column(db.DateTime, default=datetime.now())
    price= db.Column(db.Float)
    appropriate = db.Column(db.Integer)
    #image= db.Column(db.String(200), nullable=True)
    image = db.Column(db.String(20), nullable=True, default='images/1.jpg')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    user= db.relationship('User',backref='books')


