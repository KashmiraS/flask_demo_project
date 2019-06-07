from project import db
from project.users.models import Users
from project.project_module.models import project
import datetime

share_project = db.Table('share_project', db.metadata,
    db.Column('uid', db.Integer, db.ForeignKey(Users.uid)),
    db.Column('pid', db.Integer, db.ForeignKey(project.pid)),
	db.Column('share_date', db.DateTime, default=datetime.utcnow)
)