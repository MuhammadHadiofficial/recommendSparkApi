
from . import db
from flask_login import UserMixin
class User(UserMixin,db.Model):
    userId = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    Email = db.Column(db.String(255), unique=True)
    Password = db.Column(db.String(255))
    userName = db.Column(db.String(255))
    Region = db.Column(db.String(255))
    def get_id(self):
           return (self.userId)
