from project.project_module.models import project,project_wapper
from project.users.models import Users
from flask_restful import Resource
from project import db
from flask import request,jsonify,json
from project.utils.statics_data import date_in_result
from project.utils.conversions import todate_time
from project.task.models import task_of_project

class project_crud(Resource):
    def post(self):
        val = {}
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
            print('SERVER==>{} {}'.format(str(val),'sucess'))
        except Exception as e:
            status = False
            val = {
                'error': str(e),
                'status': status
            }
            print('Error:"{}" ,"status":{}'.format(str(e),status))
        return jsonify(val)
    def patch(self):
        try:
            print('IN SERVER :{}'.format(str(json.loads(request.data))))
            object_ = json.loads(request.data)
            print('==>REQUEST PROJECT:{}'.format(str(object_)))
            var = object_['user']
            project_ = object_['project']
            try:
                if (project_['project_starting_date']==None) or (project_['project_starting_date']=='None'):
                    project_.pop('project_starting_date')
                if (project_['project_releasing']==None) or (project_['project_releasing']=='None'):
                    project_.pop('project_releasing')
            except KeyError:
                pass
            print('==>CHECK LAST:{}'.format(str(project_)))
            project.query.get(var['pid']).update(project_)
            print("updateing..")
            db.session.commit()
            return {
                'status': True
            }
        except Exception as e:
            return {
                    'status': True,
                    'error' : str(e)
                }


class get_project_all(Resource):
    def get(self, id):
        data = list()
        # object_ = json.loads(request.data)
        us = Users.query.get(id)
        for row in project.query.filter(project.share.contains(us)):
            d = row.__dict__
            d.pop('_sa_instance_state')
            print(d)
            for x in date_in_result:
                d[x]=str(d[x])
            data.append(d)
        print({'all_projects': data})
        return {'all_projects': data}

class get_project(Resource):
    def post(self):
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        data = list()
        us = Users.query.get(dataDict['uid'])
        for row in project.query.filter(db.and_(project.share.contains(us),project.pid==dataDict['pid'])):
            d = row.__dict__
            d.pop('_sa_instance_state')
            for x in date_in_result:
                d[x]=str(d[x])
            data.append(d)
        print('\nSingle Project:')
        print({'all_projects': data})
        return {'all_projects': data}

class delete_project(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            pro = project.query.get(dataDict['pid'])
            if pro.pid:
                try:
                    status = project.query.get(dataDict['pid'])
                    status.share.clear()
                except Exception as e:
                    print(f'Error {e} ')
                status = project.query.filter(
                    db.and_(project.uid == dataDict['uid'], project.pid == dataDict['pid'])).delete()
                status = task_of_project.query.filter(task_of_project.pid == dataDict['pid']).delete()
                db.session.commit()
                status = True
            else:
                status = False
        except Exception as e:
            print(str(e))
        print({'status': status})
        return {'status': status}

class share_project(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            us = Users.query.filter(Users.email == dataDict['mail_id']).first()
            pro = project.query.get(dataDict['pid'])
            pro.share.append(us)
            db.session.commit()
            status=True
            print({'status': status})
            return {'status': status}
        except Exception as e:
            print({'status': status,'error':str(e)})
            return {'status': status,'error':str(e)}

class all_project_users(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            us = Users.query.get(dataDict['uid'])
            us = project.query.filter(db.and_(project.share.contains(us),project.pid==dataDict['pid'])).first()
            users=list()
            for x in us.share:
                d = x.__dict__
                d.pop('_sa_instance_state')
                d.pop('password_text')
                users.append(d)
            status = True
            data ={'status': status,
                    'users':json.loads(json.dumps(users))}
            print('\n\nusers {}:{}'.format(dataDict['uid'],data))
            return data
        except Exception as e:
            print({'status': status,'error':str(e)})
            return {'status': status,'error':str(e)}


