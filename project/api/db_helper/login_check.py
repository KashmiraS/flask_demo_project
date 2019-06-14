from project.mailer_module.mailer_class import send_mail
from project.users.models import Users
from flask_restful import Resource
from project import db, host_address
from flask import json, request


class login_helper(Resource):
    '''
    Login helper will help to work with all User operations like:
    1. Register
    2. Login
    3. Login Check
    4. Get user'''

    def get(self, email_, password):
        # Login status check
        print("LOGIN REQUEST SERVER:{} ".format(email_))
        try:
            # GET user by username and password
            re = Users.query.filter(Users.email == email_, Users.password_text == password).first().__dict__
            print(re['uid'])
            res = {'status': bool(re),
                   'user_id': re['uid'],
                   'username': re['username']
                   }
            print('LOGIN RESPONSE SERVER :{}'.format(str(res)))
            return res  # sending response with user details including status
        except Exception as e:
            return {
                'status': False,
                'error': str(e)
            }


# user check is created for get user by mail id is user is exist or not
class user_check(Resource):
    # This function will use for get user mail is exist of not
    def get(self, email_):
        return {'status': bool(Users.query.filter_by(email=email_).first())}


class get_user(Resource):
    # Get user by mail id and send response with user details of associated user details
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


# This class is responsible for password changes
class password_class(Resource):
    # This function will help to send link of forget password and also sending mail to associated user
    def post(self):
        status = False
        user = dict()
        try:
            data = request.data
            dataDict = json.loads(data)
            print('CHANGE PASSWORD REQUEST: {}'.format(dataDict))

            # GET USER
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()

            # MAIL
            link = f'{host_address[:-4]}/users/new_password/{us.email}'
            body = f'Forget password link <a href="{link}">Click here</a>'
            send_mail('FORGET PASSWORD', us.username, us.email, body)  # SEND MAIL
            status = True
        except Exception as e:
            print(str(e))
        return {'status': status, 'user': str(user)}

    def patch(self):
        # for update new password
        status = False
        user = dict()
        try:
            data = request.data
            print("CHANGE PASSWORD NEW PASSWORD REQUEST: {}".format(data))
            dataDict = json.loads(data)
            print(type(dataDict))
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()
            us.password_text = str(dataDict['new_password'])  # assign new password
            user['uid'] = us.uid
            user['mail_id'] = us.email
            user['username'] = us.username
            db.session.commit()
            status = True
        except Exception as e:
            pass
        return {'status': status, 'user': str(user)}

# Register user with user table
class register(Resource):
    # add new user with user name, email and password
    def post(self, username, email, password):
        status = True
        try:
            print("REGISTER USER SERVER REQUEST====>{} {}".format(username, email))
            user_obj = Users(username, email, password)
            db.session.add(user_obj)
            db.session.commit()
        except Exception:
            status = False
        return {'user': email, 'status': status, 'name': username}
