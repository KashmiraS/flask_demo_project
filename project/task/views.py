from project.task.forms import create_task_form
import requests
from project import host_address
from flask import Blueprint, render_template,request,session,redirect,url_for
import json
from flask_login import login_required

task_view = Blueprint('task', __name__, template_folder='templates/task')


@task_view.route('/<int:project_id>')
@login_required
def index(project_id):
    req = {'pid':project_id,'uid':session['uid']}
    resp = json.loads(requests.post(f'{host_address}/task/all', json.dumps(req)).text)
    print('>>{}'.format(str(resp)))
    count = dict()
    count['complete'] =0
    count['remaining']=0
    count['all']=0
    if(resp['status']):
        data = resp['tasks']
        for x in data:
            if(x['state']==1):
                count['complete'] +=1
            elif (x['state']==0):
                count['remaining'] += 1
            count['all'] +=1

    return render_template('task_home.html',project_id=project_id,count=count,project_name=resp['project_name'])


@task_view.route('/view/<int:list_id>/<int:project_id>')
@login_required
def view(list_id, project_id):
    req = {'pid':project_id,'uid':session['uid']}
    tasks = list()
    print('\nREQUEST VIEW TASK-->{}'.format(str(req)))
    resp = json.loads(requests.post(f'{host_address}/task/all', json.dumps(req)).text)
    print('\nRESPONSE VIEW TASK-->{}'.format(str(resp)))
    if resp['status']:
        tasks = resp['tasks']
    return render_template('list_of_task.html', list_id=list_id, project_id=project_id,tasks=tasks)


@task_view.route('/create/<int:project_id>',methods=['GET','POST'])
@login_required
def create_task(project_id):
    form = create_task_form()
    if request.method =='POST':
        req =dict()
        req['title'] = form.title.data
        req['details'] = form.details.data
        req['start_date'] = str(form.start_date.data)
        req['end_date'] = str(form.end_date.data)
        req['uid'] = session['uid']
        req['pid'] = project_id
        print('\nREQUEST CREATE TASK-->{}'.format(str(req)))
        resp = json.loads(requests.post(f'{host_address}/task/create',json.dumps(req)).text)
        print('\nRESPONSE CREATE TASK-->{}'.format(str(resp)))
        if resp['status']:
            return redirect(url_for('task.index',project_id=project_id))

    return render_template('create_task.html', project_id=project_id,form=form)

@login_required
@task_view.route('/delete/<int:project_id>/<int:list_id>/<int:tid>')
def delete_task(project_id,list_id,tid):
    req = dict()
    req['uid'] = session['uid']
    req['pid'] = project_id
    req['tid'] = tid
    requests.post(f'{host_address}/task/delete', json.dumps(req))
    return redirect(url_for('task.view',list_id=list_id,project_id=project_id))

@login_required
@task_view.route('/complete/<int:project_id>/<int:list_id>/<int:tid>')
def mark_complete(project_id,list_id,tid):
    req = dict()
    req['uid'] = session['uid']
    req['pid'] = project_id
    req['tid'] = tid
    requests.post(f'{host_address}/task/marking', json.dumps(req))
    return redirect(url_for('task.view',list_id=list_id,project_id=project_id))


@login_required
@task_view.route('/working/<int:project_id>/<int:list_id>/<int:tid>')
def mark_un_complete(project_id,list_id,tid):
    req = dict()
    req['uid'] = session['uid']
    req['pid'] = project_id
    req['tid'] = tid
    requests.patch(f'{host_address}/task/marking', json.dumps(req))
    return redirect(url_for('task.view',list_id=list_id,project_id=project_id))