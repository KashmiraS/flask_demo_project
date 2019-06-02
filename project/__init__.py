from flask import Flask,render_template,url_for,redirect
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

class User(UserMixin):
    pass

app = Flask(__name__)

app.config['SECRET_KEY'] = 'Here is the key'
login_manager = LoginManager()
login_manager.init_app(app)

users_record = {'foo@bar.tld': {'password': 'secret'}}

@login_manager.user_loader
def user_loader(email):
    if email not in users_record:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    users = {'foo@bar.tld': {'password': 'secret'}}
    email = request.form.get('email')
    if email not in users:
        return
    user = User()
    user.id = email
    try:
        user.is_authenticated = request.form['password'] == users[email]['password']
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
app.register_blueprint(user_print, url_prefix='/users')


###########
## INDEX ##
###########
@app.route('/')
def index():
    return render_template('index.html')

