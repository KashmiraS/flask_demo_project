from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_restful import Api

host_address = 'http://127.0.0.1:5000/api'


class User(UserMixin):
    pass


app = Flask(__name__)
api_obj = Api(app)
app.config['SECRET_KEY'] = 'Here is the key'

################
## SQLALCHEMY ##
################

dirpath = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dirpath, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Migrate(app, db)

#################
# LOGIN MANAGER #
#################
login_manager = LoginManager()
login_manager.init_app(app)
users_record = {'foo@bar.tld': {'password': 'secret'}}

from project.users.models import Users


@login_manager.user_loader
def user_loader(email):
    if not bool(Users.query.filter_by(email=email).first()):
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if not bool(Users.query.filter_by(email=email).first()):
        return
    user = User()
    user.id = email
    try:
        user.is_authenticated = bool(Users.query.filter_by(email=email).first())
    except AttributeError:
        pass
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('users.login'))


#############################
#### BLUEPRINT REGISTRY #####
#############################
from project.users.views import user_print
from project.project_module.views import project_print

# from project.api.db_helper.login_check import login

# app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(user_print, url_prefix='/users')
app.register_blueprint(project_print, url_prefix='/project')


###########
## INDEX ##
###########
@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


###################
#### REST CALLS ###
###################
from project.api.db_helper.login_check import login_helper
from project.api.db_helper.login_check import user_check
from project.api.db_helper.login_check import register
from project.api.db_helper.project_operatios import get_project_all,project_crud,get_project

api_obj.add_resource(login_helper, '/api/login/<string:email_>/<string:password>')
api_obj.add_resource(user_check, '/api/user_check/<string:email_>')
api_obj.add_resource(register, '/api/register/<string:username>/<string:email>/<string:password>')
#api_obj.add_resource(project_crud, '/api/project/<string:project_name>/<string:project_description>/<string:project_starting_date>/<string:project_releasing>/<string:customer_name>/<string:customer_contact>/<string:customer_mail>/<string:customer_company_name>/<string:customer_site>')
api_obj.add_resource(get_project_all, '/api/project/all/<int:id>')
api_obj.add_resource(project_crud, '/api/project')
api_obj.add_resource(get_project, '/api/project/view')

