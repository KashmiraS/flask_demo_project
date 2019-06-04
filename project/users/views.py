from flask import url_for, render_template, Blueprint, request, redirect
from project import User, db ,host_address
import requests
import json
import flask_login
from project.users.froms import user_registration, user_login
from project.users.models import Users

user_print = Blueprint('users', __name__, template_folder='templates/users')


@user_print.route('/')
@flask_login.login_required
def index():
    return render_template('users.html', users_=flask_login.current_user.id)


@user_print.route('/signup', methods=['GET', 'POST'])
def registration():
    form = user_registration()
    flask_login.logout_user()
    Error_ = ""
    if request.method == 'POST':
        re_enter_pass = form.re_enter_pass.data
        password = form.password.data
        if (password == re_enter_pass):
            try:
                username = form.username.data
                email = form.email.data
                present = (json.loads((requests.get('{}/user_check/{}'.format(host_address,email))).text))['status']
                if not present:
                    res=(json.loads((requests.post('{}/register/{}/{}/{}'.format(host_address,username, email, password))).text))['status']
                    if res:
                        return redirect(url_for('users.login'))
                Error_ = 'EXIST'
            except Exception as e:
                print(str(e))
                Error_ = 'VALUES_ERROR'
                return render_template('registration.html', form=form, Error_=Error_)
        else:
            Error_ = 'PASSWORD_NOT_MATCH'
            return render_template('registration.html', form=form, Error_=Error_)
    return render_template('registration.html', form=form, Error_=Error_)


@user_print.route('/signin', methods=['GET', 'POST'])
def login():
    form = user_login()
    Error_ = ""
    if request.method == 'POST':
        try:
            email_ = form.email.data
            password = form.password.data
            if len(email_) == 0 and len(password) == 0:
                return render_template('login.html', form=form, Error_='NO_INPUT')
            else:
                print('here input' + email_)
                present = (json.loads((requests.get('{}/login/{}/{}'.format(host_address,email_, password))).text))['status']
                if present:
                    user = User()
                    user.id = email_
                    print(flask_login.current_user.is_authenticated)
                    flask_login.login_user(user)
                    return redirect(url_for('users.index'))
                Error_ = 'KEY_ERROR'
        except KeyError:
            Error_ = 'ERROR_ON_USER_KEY'
        except Exception as e:
            Error_ = 'ok'+str(e)
    print(Error_)
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('users.index'))
    else:
        return render_template('login.html', form=form, Error_=Error_)


@user_print.route('/logout')
def logout():
    print('in logout')
    flask_login.logout_user()
    return redirect(url_for('users.login'))
