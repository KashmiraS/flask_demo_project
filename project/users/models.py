from project import db  # GET DATABASE OBJECT
# Take Reference of
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html
from datetime import datetime


class Users(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    email = db.Column(db.Text)
    password_text = db.Column(db.Text)
    reg_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password_text):
        self.username = username
        self.email = email
        self.password_text = password_text

    def __repr__(self):
        return {
            'username': self.username,
            'email': self.email,
        }
