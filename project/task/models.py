from project import db
from project.users.models import Users
from project.project_module.models import project
from project.utils.conversions import to_date


class task_of_project(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    details = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    state = db.Column(db.Integer)
    uid = db.Column('uid', db.Integer, db.ForeignKey(Users.uid))
    pid = db.Column('pid', db.Integer, db.ForeignKey(project.pid, ondelete='CASCADE'))
    # Creating relationship with project
    projects = db.relationship("project", backref="task_of_project")

    def __init__(self, task_):
        self.title = task_['title']
        self.details = task_['details']
        if task_ in ['start_date']:
            self.start_date = to_date(task_['start_date']).date()
        if task_ in ['end_date']:
            self.end_date = to_date(task_['end_date']).date()
        self.uid = task_['uid']
        self.pid = task_['pid']
        self.state = 0
