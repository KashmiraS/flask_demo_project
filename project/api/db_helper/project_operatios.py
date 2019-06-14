from project.mailer_module.mailer_class import send_mail
from project.project_module.models import project
from project.users.models import Users
from flask_restful import Resource
from project import db
from flask import request, jsonify, json
from project.utils.statics_data import date_in_result
from project.task.models import task_of_project


# ADD and Update the project details will taken care by this class
class project_crud(Resource):
    # To add new project
    '''
    Including request parameters in JSON
    project_name = STRING
    project_description = STRING
    project_starting_date = DATE (YYYY-MM-DD)
    project_releasing = DATE (YYYY-MM-DD)
    customer_name = STRING
    customer_contact = STRING
    customer_mail = STRING
    customer_company_name = STRING
    customer_site = STRING
    uid = INTEGER USER who creating thi project ForeignKey(Users.uid))
    share = LIST  relationship('Users')
    '''

    def post(self):
        status = True
        try:

            object_ = json.loads(request.data)
            print('==>REQUEST PROJECT:{}'.format(json.dumps(object_)))
            project_obj = project(object_)
            db.session.add(project_obj)
            db.session.commit()
            val = {
                'project_id': str(project_obj.pid),
                'status': status
            }
            print('SERVER==>{} {}'.format(str(val), 'success'))
        except Exception as e:
            status = False
            val = {
                'error': str(e),
                'status': status
            }
            print('Error:"{}" ,"status":{}'.format(str(e), status))
        return jsonify(val)

    # To add Update project
    '''
    Including request parameters in JSON
    pid = INTEGER 
    project_name = STRING
    project_description = STRING
    project_starting_date = DATE (YYYY-MM-DD)
    project_releasing = DATE (YYYY-MM-DD)
    customer_name = STRING
    customer_contact = STRING
    customer_mail = STRING
    customer_company_name = STRING
    customer_site = STRING
    uid = INTEGER USER who creating thi project ForeignKey(Users.uid)) 
    share = LIST  relationship('Users')
    '''

    def patch(self):
        try:
            print('IN SERVER :{}'.format(str(json.loads(request.data))))
            object_ = json.loads(request.data)
            print('==>REQUEST PROJECT:{}'.format(str(object_)))
            var = object_['user']
            project_ = object_['project']
            try:
                if (project_['project_starting_date'] is None) or (project_['project_starting_date'] is 'None'):
                    project_.pop('project_starting_date')
                if (project_['project_releasing'] is None) or (project_['project_releasing'] is 'None'):
                    project_.pop('project_releasing')
            except KeyError:
                pass
            print('==>CHECK LAST:{}'.format(str(project_)))
            project.query.get(var['pid']).update(project_)
            print("updating..")
            db.session.commit()
            return {
                'status': True
            }
        except Exception as e:
            return {
                'status': True,
                'error': str(e)
            }


# GET All projects by the user id
class get_project_all(Resource):
    def get(self, id):
        data = list()
        us = Users.query.get(id)
        for row in project.query.filter(project.share.contains(us)):
            d = row.__dict__
            d.pop('_sa_instance_state')
            print(d)
            for x in date_in_result:
                d[x] = str(d[x])  # CONVERTING all dates in String format
            data.append(d)
        print({'all_projects': data})
        return {'all_projects': data}


# GET Single project by project id and to verify is user is authorized or not we need user id also
class get_project(Resource):
    def post(self):
        data = request.data
        data_dict = json.loads(data)
        print(data_dict)
        data = list()
        us = Users.query.get(data_dict['uid'])
        for row in project.query.filter(db.and_(project.share.contains(us), project.pid == data_dict['pid'])):
            d = row.__dict__
            d.pop('_sa_instance_state')
            for x in date_in_result:
                d[x] = str(d[x])
            data.append(d)
        print('\nSingle Project:')
        print({'all_projects': data})
        return {'all_projects': data}


# This class will help to delete the project if user and project id
class delete_project(Resource):
    def post(self):
        status = False
        data = request.data
        data_dict = json.loads(data)
        print(data_dict)
        try:
            pro = project.query.get(data_dict['pid'])  # get project is exist or not
            if pro.pid:
                try:
                    status = project.query.get(data_dict['pid'])
                    status.share.clear()
                except Exception as e:
                    print(f'Error {e} ')
                status = project.query.filter(
                    db.and_(project.uid == data_dict['uid'], project.pid == data_dict['pid'])).delete()
                status = task_of_project.query.filter(task_of_project.pid == data_dict['pid']).delete()
                db.session.commit()
                status = True
            else:
                status = False
        except Exception as e:
            print(str(e))
        print({'status': status})
        return {'status': status}


# This class is responsible for share project with other users
class share_project(Resource):
    def post(self):
        status = False
        data = request.data
        data_dict = json.loads(data)
        print(data_dict)
        try:
            us = Users.query.filter(Users.email == data_dict['mail_id']).first()
            pro = project.query.get(data_dict['pid'])
            pro.share.append(us)
            db.session.commit()
            status = True
            send_mail(f'Shared project:{pro.project_name}', 'USER', data_dict['mail_id'],
                      f'{us.username} has shared a project with you.')  # subject,user_name,mail_id,body
            print({'status': status})
            return {'status': status}
        except Exception as e:
            print({'status': status, 'error': str(e)})
            return {'status': status, 'error': str(e)}


# to get all associated users of project
class all_project_users(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            us = Users.query.get(dataDict['uid'])  # get user
            us = project.query.filter(db.and_(project.share.contains(us), project.pid == dataDict['pid'])).first()
            users = list()
            for x in us.share:
                d = x.__dict__
                d.pop('_sa_instance_state')
                d.pop('password_text')
                users.append(d)  # create users list
            status = True
            data = {'status': status,
                    'users': json.loads(json.dumps(users))}
            print('\n\nusers {}:{}'.format(dataDict['uid'], data))
            return data
        except Exception as e:
            print({'status': status, 'error': str(e)})
            return {'status': status, 'error': str(e)}
