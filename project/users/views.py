from flask import url_for,render_template,Blueprint,request,redirect
from project import login_manager,User,users_record
import flask_login
user_print = Blueprint('users',__name__,template_folder='templates/users')

@user_print.route('/')
@flask_login.login_required
def index():
    return render_template('users.html',users_ =flask_login.current_user.id)

@user_print.route('/signup')
def registration():
    flask_login.logout_user()
    return render_template('registration.html')

@user_print.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            if email =='' and password == '':
                return render_template('login.html', Error_='NO_INPUT')
            else:
                print('here input')
                if request.form['password'] == users_record[email]['password']:
                    user = User()
                    user.id = email
                    flask_login.login_user(user)
                    return redirect(url_for('users.index'))
                else:
                    return render_template('login.html',Error_='KEY_ERROR')
        except KeyError:
            return render_template('login.html',Error_='ERROR_ON_USER_KEY')
        except Exception as e:
            return render_template('login.html',Error_='ok'+str(e))