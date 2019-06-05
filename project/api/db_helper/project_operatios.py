from project.project_module.models import project
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


class get_project(Resource):
    def get(self, pid):
        print("Project REQUEST :{} ".format(pid))
        res = project.query.get(pid)
        print(str(res))
        return res
