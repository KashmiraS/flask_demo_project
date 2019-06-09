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

class get_project_all(Resource):
    def get(self, id):
        data = list()
        # object_ = json.loads(request.data)
        for row in project.query.filter(project.uid == id):
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
        for row in project.query.filter(db.and_(project.uid == dataDict['uid'],project.pid==dataDict['pid'])):
            d = row.__dict__
            d.pop('_sa_instance_state')
            for x in date_in_result:
                d[x]=str(d[x])
            data.append(d)
        print({'all_projects': data})
        return {'all_projects': data}

class delete_project(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            status = project.query.filter(db.and_(project.uid == dataDict['uid'],project.pid==dataDict['pid'])).delete()
            status = task_of_project.query.filter(task_of_project.pid==dataDict['pid']).delete()
            db.session.commit()
        except Exception:
            pass


        print({'status': status})
        return {'status': status}