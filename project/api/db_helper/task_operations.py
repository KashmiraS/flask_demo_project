from project.project_module.models import project
from project.task.models import task_of_project
from flask_restful import Resource
from project import db
from flask import request, json
from project.utils.statics_data import dates


# create task to associated project
class create_task(Resource):
    # Create task
    def post(self):
        try:
            object_ = json.loads(request.data)
            print('CREATE TASK SERVER REQUEST-->{}'.format(object_))
            task_ = task_of_project(object_)
            db.session.add(task_)
            db.session.commit()
            return {'status': True, 'task_id': task_.tid}
        except Exception as e:
            return {'status': False, 'error': str(e)}


# get tasks by project id
class get_task(Resource):
    def post(self):
        try:
            object_ = json.loads(request.data)
            print(' GET ALL TASK SERVER-->{}'.format(object_))
            data = list()
            for row in task_of_project.query.filter(task_of_project.pid == object_['pid']):
                d = row.__dict__
                d.pop('_sa_instance_state')  # removing because of empty response
                for x in dates:
                    d[x] = str(d[x])
                data.append(d)
            pro = project.query.get(int(object_['pid']))
            print("SERVER RESPONSE :{}".format(str(data)))
            return {'status': True, 'tasks': data, 'project_name': str(pro.project_name)}
        except Exception as e:
            return {'status': False, 'error': str(e)}

# deleting task form project
class delete_task(Resource):
    def post(self):
        status = False
        try:
            object_ = json.loads(request.data)
            print('TASK DELETE SERVER REQUEST -->{}'.format(object_))
            obj = task_of_project.query.get(object_['tid'])
            status = (obj.tid == object_['tid'])
            task_of_project.query.filter(task_of_project.tid == object_['tid']).delete()
            db.session.commit()
        except Exception as e:
            pass
        return {'status': status}

#  mark on task to complete or working
class markings(Resource):
    # will work for complete mark of task
    # indications WORKING - 0 COMPLETE - 1
    def post(self):
        try:
            object_ = json.loads(request.data)
            print('MARK COMPLETE TASK SERVER REQUEST-->{}'.format(object_))
            task = task_of_project.query.get(object_['tid'])
            task.state = 1
            db.session.commit()
            return {'status': True}
        except Exception as e:
            return {'status': False, 'error': str(e)}

    # mark working
    def patch(self):
        try:
            object_ = json.loads(request.data)
            print('MARK WORKING TASK SERVER REQUEST-->{}'.format(object_))
            task = task_of_project.query.get(object_['tid'])
            task.state = 0
            db.session.commit()
            return {'status': True}
        except Exception as e:
            return {'status': False, 'error': str(e)}
