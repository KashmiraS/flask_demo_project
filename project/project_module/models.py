from project import db
from datetime import datetime
from project.users.models import Users


class project(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.Text)
    project_description = db.Column(db.Text)
    project_starting_date = db.Column(db.Text, default=datetime.utcnow)
    project_releasing = db.Column(db.Text, default=datetime.utcnow)
    # just for demo I used customer in this
    customer_name = db.Column(db.Text)
    customer_contact = db.Column(db.Text)
    customer_mail = db.Column(db.Text)
    customer_company_name = db.Column(db.Text)
    customer_site = db.Column(db.Text)
    uid = db.Column(db.Integer, db.ForeignKey(Users.uid))

    def __init__(self, project_):
        self.project_name = project_['project_name']
        self.project_description = project_['project_description']
        self.project_starting_date = project_['project_starting_date']
        self.project_releasing = project_['project_releasing']
        self.customer_name = project_['customer_name']
        self.customer_contact = project_['customer_contact']
        self.customer_mail = project_['customer_mail']
        self.customer_company_name = project_['customer_company_name']
        self.customer_site = project_['customer_site']
        self.uid = project_['uid']

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
            'customer_site': self.customer_site
        }

    def object_to_object(self, object1,object2):
        for obj1, obj2 in object1.keys():
            object1[obj1] = object2[obj2]
        return object1


class project_wapper():
    def __init__(self,project_):
        self.project_name = project_['project_name']
        self.project_description = project_['project_description']
        self.project_starting_date = project_['project_starting_date']
        self.project_releasing = project_['project_releasing']
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

