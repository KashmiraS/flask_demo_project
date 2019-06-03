from flask import request, redirect, render_template, Blueprint
from flask_login import login_required
from project.project_module.forms import add_project

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
        project_name = form.project_name.data
        project_description = form.project_name.data
        project_starting_date = form.project_name.data
        project_releasing = form.project_name.data

        customer_name = form.project_name.data
        customer_contact = form.project_name.data
        customer_mail = form.project_name.data
        customer_company_name =form.project_name.data
        customer_site = form.project_name.data

    return render_template('new_project.html', form=form)
