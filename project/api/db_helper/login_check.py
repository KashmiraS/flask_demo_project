import base64

from project.mailer_module.mailer_class import send_mail
from project.users.models import Users
from flask_restful import Resource
from project import db,host_address
from flask import json, request


class login_helper(Resource):
    def get(self, email_, password):
        print("LOGIN REQUEST :{} ".format(email_))
        try:
            re = Users.query.filter(Users.email == email_, Users.password_text == password).first().__dict__
            print(re['uid'])
            res = {'status': bool(re),
                   'user_id': re['uid'],
                   'username': re['username']
                   }
            print(str(res))
            return res
        except Exception as e:
            return {
                'status': False,
                'error': str(e)
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
class get_user(Resource):
    def post(self):
        status = False
        user = dict()
        try:
            data = request.data
            print(data)
            dataDict = json.loads(data)
            print(dataDict)
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()
            user['username'] = us.username
            user['email'] = us.email
            user['uid'] = us.uid
            status = True
        except Exception as e:
            print(str(e))
        return {'status': status, 'user': user}


class password_class(Resource):
    def post(self):
        status = False
        user = dict()
        try:
            data = request.data
            print(data)
            dataDict = json.loads(data)
            print(dataDict)
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()
            link = f'{host_address[:-4]}/users/new_password/{us.email}'
            body=f'Forget password link <a href="{link}">Click here</a>'
            send_mail('FORGET PASSWORD',us.username,us.email,body)
            status = True
        except Exception as e:
            print(str(e))
        return {'status': status, 'user': str(user)}

    def patch(self):
        status = False
        user = dict()
        try:
            data = request.data
            print("CHANGE PASSWORD {}".format(data))
            dataDict = json.loads(data)
            print(type(dataDict))
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()
            us.password_text = str(dataDict['new_password'])
            user['uid'] =us.uid
            user['mail_id']  = us.email
            user['username'] =us.username
            db.session.commit()
            status = True
        except Exception as e:
            pass
        return {'status': status, 'user': str(user)}


class register(Resource):
    def post(self, username, email, password):
        status = True
        try:
            print("REGISTER POST ====>{} {}".format(username, email))
            user_obj = Users(username, email, password)
            db.session.add(user_obj)
            db.session.commit()
        except Exception:
            status = False
        return {'user': email, 'status': status, 'name': username}
