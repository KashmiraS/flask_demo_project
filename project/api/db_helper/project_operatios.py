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
    def patch(self):
        object_ = json.loads(request.data)
        print('==>REQUEST PROJECT:{}'.format(json.dumps(object_)))
        var = json.loads(object_['user'])
        pro = project.query.get(var['pid'])
        project_ = json.loads(object_['project'])
        pro.project_name = project_['project_name']
        pro.project_description = project_['project_description']
        if not (project_['project_starting_date']==None):
            pro.project_starting_date = project_['project_starting_date']
        if not (project_['project_releasing']==None):
            pro.project_releasing = project_['project_releasing']
        pro.customer_name = project_['customer_name']
        pro.customer_contact = project_['customer_contact']
        pro.customer_mail = project_['customer_mail']
        pro.customer_company_name = project_['customer_company_name']
        pro.customer_site = project_['customer_site']
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

class delete_project(Resource):
    def post(self):
        status = False
        data = request.data
        dataDict = json.loads(data)
        print(dataDict)
        try:
            status = project.query.filter(db.and_(project.uid == dataDict['uid'],project.pid==dataDict['pid'])).delete()
            db.session.commit()
        except Exception:
            pass


        print({'status': status})
        return {'status': status}