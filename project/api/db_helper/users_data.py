from project.users.models import Users
from project import db
import json
def get_all():
    d = list()
    for x in Users.query.all():
        val = x.__dict__
        val.pop('_sa_instance_state')
        val.pop('reg_date')
        d.append(val)
    return "{ 'users':"+str(d)+"}"
