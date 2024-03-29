from flask import request, redirect, render_template, Blueprint, json, url_for, session, flash
from flask_login import login_required
from project.project_module.forms import AddProject, ShareProjectForm
from project.project_module.models import project_wapper
from project.utils.statics_data import date_in_result, not_in_result
from project.utils.conversions import to_date_time, to_date, with_utf
from project.request_module.apicalls import project_api

project_print = Blueprint('project', __name__, template_folder='templates/project_module')

api = project_api()


@project_print.route('/')
@login_required
def index():
    uid_send = dict()
    uid_send["uid"] = session['uid']
    print(json.dumps(uid_send))
    data = api.get_all(session['uid'])
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
    form = AddProject()
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
        print('==>>REQUEST : {}'.format(str(project_obj.__dict__)))
        data = api.create(json.dumps(project_obj.__dict__))
        print('{} response '.format(data))
        if data['status']:
            return redirect(url_for('project.index'))
    return render_template('new_project.html', form=form)


@project_print.route('/edit/<int:pid>', methods=['GET', 'POST'])
@login_required
def edit(pid):
    form = AddProject()
    req = {'pid': pid, 'uid': session['uid']}
    res = api.view(req)
    print('RESPONSE : {}'.format(str(res)))
    data = res['all_projects'][0]
    if len(res['all_projects']) == 0:
        return render_template('project_view.html', data='NO')
    if len(data) == 0:
        return redirect(url_for('project.index'))
    else:
        print(type(data))
        if request.method == 'GET':
            for key, val in data.items():
                if key in ['project_name', 'project_description', 'customer_contact', 'customer_company_name',
                           'customer_site', 'customer_mail', 'customer_name']:
                    form[key].data = val
                if key in ['project_starting_date', 'project_releasing']:
                    form[key].value = with_utf(to_date(val))
                    print('KEY >{} {}'.format(type(to_date_time(val)), val))

    if request.method == 'POST':
        project_ = dict()
        for key, val in data.items():
            if not key in not_in_result:
                project_[key] = form[key].data
        project_['uid'] = session['uid']
        project_obj = project_wapper(project_)
        print('==>>REQUEST : {}'.format(str(project_obj.__dict__)))
        up_req = {
            'user': req,
            'project': project_obj.__dict__
        }
        print('\n\n------<>{}'.format(up_req))
        data = api.save_edited(json.dumps(up_req))
        print('{} response '.format(data))
        if data['status']:
            return redirect(url_for('project.index'))
    return render_template('edit_project.html', form=form)


@project_print.route('/view')
@login_required
def project_view():
    req = {'pid': request.args.get('pid'), 'uid': session['uid']}
    res = api.view(req)
    users = api.get_project_users(req)
    print('RESPONSE : {}'.format(str(res)))
    if len(res['all_projects']) == 0:
        return render_template('project_view.html', data='NO')
    for x in date_in_result:
        res['all_projects'][0][x] = to_date_time(res['all_projects'][0][x])
    return render_template('project_view.html', data=res['all_projects'][0], users=users['users'])


@project_print.route('/delete')
@login_required
def delete():
    req = {'pid': request.args.get('pid'), 'uid': session['uid']}
    res = api.delete(req)
    print('RESPONSE : {}'.format(str(res)))
    if res['status']:
        return redirect(url_for('project.index'))
    return redirect(url_for('project.project_view'))


@project_print.route('/share/<int:project_id>', methods=['GET', 'POST'])
@login_required
def share(project_id):
    form = ShareProjectForm()
    if request.method == 'POST':
        req = {'pid': project_id, 'uid': session['uid'], 'mail_id': str(form.mail_id.data)}
        res = api.share(req)
        print(str(res))
        if res['status']:
            flash('Project Shared Successfully!')
        else:
            flash('Project Not Shared!')
    return render_template('share_project.html', form=form)
