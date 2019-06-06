from project.project_module.models import project,project_wapper
from project.users.models import Users
from flask_restful import Resource
from project import db
from flask import request,jsonify,json


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


class get_project_all(Resource):
    def get(self, id):
        data = list()
        # object_ = json.loads(request.data)
        for row in project.query.filter(project.uid == id):
            d = row.__dict__
            d.pop('_sa_instance_state')
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
            data.append(d)
        print({'all_projects': data})
        return {'all_projects': data}
