from flask import request, redirect, render_template, Blueprint, jsonify, json, Response, url_for, session
import requests
from flask_login import login_required
from project.project_module.forms import add_project
from project.project_module.models import project_wapper

project_print = Blueprint('project', __name__, template_folder='templates/project_module')


@project_print.route('/')
@login_required
def index():
    uid_send = dict()
    uid_send["uid"] = session['uid']
    print(json.dumps(uid_send))
    data = json.loads(requests.get('http://127.0.0.1:5000/api/project/all/{}'.format(session['uid'])).text)
    var = list()
    try:
        var = data['all_projects']
        print(var)
    except Exception:
        pass
    return render_template('project_module.html', var=var)


@project_print.route('/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = add_project()
    if request.method == 'POST':
        project_ = dict()
        project_['project_name'] = form.project_name.data
        project_['project_description'] = form.project_description.data
        project_['project_starting_date'] = form.project_starting_date.data
        project_['project_releasing'] = form.project_releasing.data

        project_['customer_name'] = form.customer_name.data
        project_['customer_contact'] = form.customer_contact.data
        project_['customer_mail'] = form.customer_mail.data
        project_['customer_company_name'] = form.customer_company_name.data
        project_['customer_site'] = form.customer_site.data
        project_['uid'] = session['uid']
        project_obj = project_wapper(project_)
        # res = Response(json.dumps(data), status=200, mimetype='application/json')
        print('==>>REQUEST : {}'.format(str(project_obj.__dict__)))
        data = json.loads(requests.post('http://127.0.0.1:5000/api/project', json.dumps(project_obj.__dict__)).text)
        print('{} response '.format(data))
        if (data['status']):
            return redirect(url_for('project.index'))
    return render_template('new_project.html', form=form)


@project_print.route('/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    form = add_project()
    req = {'pid': pid, 'uid': session['uid']}
    res = json.loads(requests.post('http://127.0.0.1:5000/api/project/view', json.dumps(req)).text)
    print('RESPONSE : {}'.format(str(res)))
    if len(res['all_projects']) == 0:
        return render_template('project_view.html', data='NO')
    data = res['all_projects'][0]
    if len(data) == 0:
        return redirect(url_for('project.index'))
    else:
        if request.method == 'GET':
            form.project_name.data = data['project_name']
            form.project_description.data = data['project_description']
            form.project_starting_date.date = data['project_starting_date']
            form.project_releasing.date = data['project_releasing']
            form.customer_name.data = data['customer_name']
            form.customer_contact.data = data['customer_contact']
            form.customer_mail.data = data['customer_mail']
            form.customer_company_name.data = data['customer_company_name']
            form.customer_site.data = data['customer_site']
    if request.method == 'POST':
        project_ = dict()
        project_['project_name'] = form.project_name.data
        project_['project_description'] = form.project_description.data
        project_['project_starting_date'] = form.project_starting_date.data
        project_['project_releasing'] = form.project_releasing.data

        project_['customer_name'] = form.customer_name.data
        project_['customer_contact'] = form.customer_contact.data
        project_['customer_mail'] = form.customer_mail.data
        project_['customer_company_name'] = form.customer_company_name.data
        project_['customer_site'] = form.customer_site.data
        project_['uid'] = session['uid']
        project_obj = project_wapper(project_)
        # res = Response(json.dumps(data), status=200, mimetype='application/json')
        print('==>>REQUEST : {}'.format(str(project_obj.__dict__)))
        up_req = {
            'user': json.dumps(req),
            'project': json.dumps(project_obj.__dict__)
        }
        data = json.loads(requests.patch('http://127.0.0.1:5000/api/project', json.dumps(up_req)).text)
        print('{} response '.format(data))
        if (data['status']):
            return redirect(url_for('project.index'))
    return render_template('edit_project.html', form=form)


@project_print.route('/view')
@login_required
def project_view():
    req = {'pid': request.args.get('pid'), 'uid': session['uid']}
    res = json.loads(requests.post('http://127.0.0.1:5000/api/project/view', json.dumps(req)).text)
    print('RESPONSE : {}'.format(str(res)))
    if len(res['all_projects']) == 0:
        return render_template('project_view.html', data='NO')
    return render_template('project_view.html', data=res['all_projects'][0])


@project_print.route('/delete')
@login_required
def delete():
    req = {'pid': request.args.get('pid'), 'uid': session['uid']}
    res = json.loads(requests.post('http://127.0.0.1:5000/api/project/delete', json.dumps(req)).text)
    print('RESPONSE : {}'.format(str(res)))
    if res['status']:
        return redirect(url_for('project.index'))
    return redirect(url_for('project.project_view'))