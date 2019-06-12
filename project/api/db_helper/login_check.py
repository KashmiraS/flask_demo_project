from project.users.models import Users
from flask_restful import Resource
from project import db
from flask import json

class login_helper(Resource):
    def get(self, email_, password):
        print("LOGIN REQUEST :{} ".format(email_))
        try:
            re = Users.query.filter(Users.email == email_, Users.password_text == password).first().__dict__
            print(re['uid'])
            res = {'status': bool(re),
                   'user_id':re['uid'],
                     'username': re['username']
                   }
            print(str(res))
            return res
        except Exception as e:
            return {
                'status':False,
                'error':str(e)
            }

    def post(self, name):
        print("POST ====>" + name)
        return {'status': name}

    def delete(self):
        print("DELETE ====>")
        return {'status': 'delete called'}


class user_check(Resource):
    def get(self, email_):
        return {'status': bool(Users.query.filter_by(email=email_).first())}


class register(Resource):
    def post(self, username, email, password):
        status =True
        try:
            print("REGISTER POST ====>{} {}".format(username, email))
            user_obj = Users(username, email, password)
            db.session.add(user_obj)
            db.session.commit()
        except Exception:
            status = False
        return { 'user':email, 'status': status ,'name' : username }
