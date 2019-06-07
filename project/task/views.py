from flask import Blueprint, render_template
from flask_login import login_required
task_view = Blueprint('task', __name__,template_folder='templates/task')


@task_view.route('/')
@login_required
def index():
    return render_template('task_home.html')
