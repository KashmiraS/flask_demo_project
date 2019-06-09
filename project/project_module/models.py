from project import db
from sqlalchemy.orm import backref
from datetime import datetime
from project.users.models import Users
from project.utils.conversions import to_date,todate_time
from project.utils.statics_data import date_in_result


share_project = db.Table('share_project', db.metadata,
                         db.Column('uid', db.Integer, db.ForeignKey(Users.uid)),
                         db.Column('pid', db.Integer, db.ForeignKey('project.pid')),
                         db.Column('share_date', db.DateTime, default=datetime.utcnow)
                         )
class project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    project_description = db.Column(db.Text)
    project_starting_date = db.Column(db.Date, default=datetime.utcnow)
    project_releasing = db.Column(db.Date, default=datetime.utcnow)
    # just for demo I used customer in this
    customer_name = db.Column(db.Text)
    customer_contact = db.Column(db.Text)
    customer_mail = db.Column(db.Text)
    customer_company_name = db.Column(db.Text)
    customer_site = db.Column(db.Text)
    uid = db.Column(db.Integer, db.ForeignKey(Users.uid))
    share = db.relationship("Users", secondary=share_project,backref="Users",lazy='dynamic')


    def __init__(self, project_):
        self.project_name = project_['project_name']
        self.project_description = project_['project_description']
        self.project_starting_date = todate_time(project_['project_starting_date']).date()
        self.project_releasing = todate_time( project_['project_releasing']).date()
        self.customer_name = project_['customer_name']
        self.customer_contact = project_['customer_contact']
        self.customer_mail = project_['customer_mail']
        self.customer_company_name = project_['customer_company_name']
        self.customer_site = project_['customer_site']
        self.uid = project_['uid']
        self.share.append(Users.query.get(project_['uid']))

    def __repr__(self):
        return {
            'project_name': self.project_name,
            'project_description': self.project_description,
            'project_starting_date': self.project_starting_date,
            'project_releasing': self.project_releasing,
            'customer_name': self.customer_name,
            'customer_contact': self.customer_contact,
            'customer_mail': self.customer_mail,
            'customer_company_name': self.customer_company_name,
            'customer_site': self.customer_site,
            'share': self.share
        }
    def update(self,project_):
        print(type(project_))
        self.project_name = project_['project_name']
        self.project_description = project_['project_description']
        if 'project_starting_date' in project_:
            self.project_starting_date = todate_time(project_['project_starting_date']).date()
        if 'project_releasing' in project_:
            self.project_releasing = todate_time(project_['project_releasing']).date()
        self.customer_name = project_['customer_name']
        self.customer_contact = project_['customer_contact']
        self.customer_mail = project_['customer_mail']
        self.customer_company_name = project_['customer_company_name']
        self.customer_site = project_['customer_site']

    def object_to_object(self, object1,object2):
        for obj1, obj2 in object1.keys():
            object1[obj1] = object2[obj2]
        return object1


class project_wapper():
    def __init__(self,project_):
        self.project_name = project_['project_name']
        self.project_description = project_['project_description']
        if not project_['project_starting_date'] ==None:
            self.project_starting_date = project_['project_starting_date']#datetime.strptime(str(project_['project_starting_date']), '%a, %d %b %Y %X %Z').date()
        if not project_['project_releasing'] == None:
            self.project_releasing =project_['project_releasing']# datetime.strptime(str(project_['project_releasing']), '%a, %d %b %Y %X %Z').date()
        self.customer_name = project_['customer_name']
        self.customer_contact = project_['customer_contact']
        self.customer_mail = project_['customer_mail']
        self.customer_company_name = project_['customer_company_name']
        self.customer_site = project_['customer_site']
        self.uid = project_['uid']

    def __repr__(self):
        return {
            "project_name": self.project_name,
            "project_description": self.project_description,
            "project_starting_date": self.project_starting_date,
            "project_releasing": self.project_releasing,
            "customer_name": self.customer_name,
            "customer_contact": self.customer_contact,
            "customer_mail": self.customer_mail,
            "customer_company_name": self.customer_company_name,
            "customer_site": self.customer_site
        }

