from flask import request, redirect, render_template, Blueprint, jsonify, json, Response
import requests
from flask_login import login_required
from project.project_module.forms import add_project
from project.project_module.models import project_wapper

project_print = Blueprint('project', __name__, template_folder='templates/project_module')


@project_print.route('/')
@login_required
def index():
    return render_template('project_module.html')


@project_print.route('/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = add_project()
    if request.method == 'POST':
        project_name = form.project_name.data
        project_description = form.project_description.data
        project_starting_date = form.project_starting_date.data
        project_releasing = form.project_releasing.data

        customer_name = form.customer_name.data
        customer_contact = form.customer_contact.data
        customer_mail = form.customer_mail.data
        customer_company_name = form.customer_company_name.data
        customer_site = form.customer_site.data
        project_obj = project_wapper(project_name, project_description, project_starting_date, project_releasing,
                              customer_name, customer_contact, customer_mail, customer_company_name, customer_site)
        # res = Response(json.dumps(data), status=200, mimetype='application/json')
        print('==>>REQUEST : {}'.format(str(project_obj.__dict__)))
        print('{} response '.format(str(json.loads(requests.post('http://127.0.0.1:5000/api/project', json.dumps(project_obj.__dict__)).text))))

    return render_template('new_project.html', form=form)
