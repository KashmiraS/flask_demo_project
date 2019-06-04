from project.users.models import Users
from project import db
from sqlalchemy.orm import load_only
import json
# For Users.query.options(load_only("uid", "email")): only columns
def get_all():
    d = list()
    for x in Users.query.options(load_only("uid", "email")):
        val = x.__dict__
        val.pop('_sa_instance_state')
        #val.pop('reg_date')
        d.append(val)
    return "{ 'users':"+str(d)+"}"