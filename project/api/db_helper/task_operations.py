from project.project_module.models import project,project_wapper
from project.users.models import Users
from project.task.models import task_of_project
from flask_restful import Resource
from project import db
from flask import request,jsonify,json
from project.utils.statics_data import date_in_result ,dates
from project.utils.conversions import todate_time

class create_task(Resource):
    def post(self):
        try:
            object_ = json.loads(request.data)
            print('TASK SERVER-->{}'.format(object_))
            task_ = task_of_project(object_)
            db.session.add(task_)
            db.session.commit()
            return {'status': True,'task_id':task_.tid}
        except Exception as e:
            return {'status': False, 'error':str(e)}

class get_task(Resource):
    def post(self):
        try:
            object_ = json.loads(request.data)
            print('TASK SERVER-->{}'.format(object_))
            #data =task_of_project.query.all()#filter(task_of_project.pid == object_['pid']).get_all()
            data = list()
            for row in task_of_project.query.filter(task_of_project.pid == object_['pid']):
                d = row.__dict__
                d.pop('_sa_instance_state')
                for x in dates:
                    d[x] = str(d[x])
                data.append(d)
            pro = project.query.get(int(object_['pid']))
            print("SERVER DATA :{}".format(str(data)))
            return {'status': True,'tasks':data,'project_name': str(pro.project_name)}
        except Exception as e:
            return {'status': False, 'error':str(e)}
class delete_task(Resource):
    def post(self):
        status =False
        try:
            object_ = json.loads(request.data)
            print('TASK SERVER-->{}'.format(object_))
            obj = task_of_project.query.get(object_['tid'])
            status = (obj.tid==object_['tid'])
            task_of_project.query.filter(task_of_project.tid==object_['tid']).delete()
            db.session.commit()
        except Exception as e:
           pass
        return {'status': status}
class markings(Resource):
    def post(self):
        try:
            object_ = json.loads(request.data)
            print('TASK SERVER-->{}'.format(object_))
            task = task_of_project.query.get(object_['tid'])
            task.state =1
            db.session.commit()
            return {'status': True }
        except Exception as e:
            return {'status': False, 'error':str(e)}

    def patch(self):
        try:
            object_ = json.loads(request.data)
            print('TASK SERVER-->{}'.format(object_))
            task = task_of_project.query.get(object_['tid'])
            task.state = 0
            db.session.commit()
            return {'status': True }
        except Exception as e:
            return {'status': False, 'error':str(e)}
