import base64

from flask import url_for, render_template, Blueprint, request, redirect, session, flash
from project import User, db ,host_address
import requests
import json
import flask_login
from project.users.froms import user_registration, user_login, forget_password_form, new_password
from project.users.models import Users
from project.request_module.apicalls import user_api

user_print = Blueprint('users', __name__, template_folder='templates/users')
api = user_api()


@user_print.route('/')
@flask_login.login_required
def index():
    return render_template('users.html', users_=flask_login.current_user.id)


@user_print.route('/signup', methods=['GET', 'POST'])
def registration():
    form = user_registration(request.form)
    flask_login.logout_user()
    Error_ = ""
    if request.method == 'POST':
        re_enter_pass = form.re_enter_pass.data
        password = form.password.data
        if (password == re_enter_pass):
            try:
                username = form.username.data
                email = form.email.data
                present = api.check_mail(email) #(json.loads((requests.get('{}/user_check/{}'.format(host_address,email))).text))['status']
                if not present:
                    res=api.register(username, email, password) #(json.loads((requests.post('{}/register/{}/{}/{}'.format(host_address,username, email, password))).text))['status']
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
                res = api.login(email_, password)#json.loads((requests.get('{}/login/{}/{}'.format(host_address,email_, password))).text)
                present = res['status']
                if present:
                    session['uid'] = res['user_id']
                    session['username'] = res['username']
                    user = User()
                    user.id = email_
                    print(flask_login.current_user.is_authenticated)
                    flask_login.login_user(user)
                    return redirect(url_for('users.index'))
                Error_ = False
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

@user_print.route('/forget_password',methods=['GET','POST'])
def forget_password():
    form = forget_password_form()
    if request.method == 'POST':
        req = {'mail_id': str(form.mail_id.data)}
        res = api.send_forget_pass(json.dumps(req))#json.loads(requests.post(f'{host_address}/project/share', json.dumps(req)).text)
        print(str(res))
        if res['status']:
            flash('Project Shared Successfully!')
        else:
            flash('Project Not Shared!')
    return render_template('forget_password.html',form=form)

@user_print.route('/new_password/<string:data>')
def visiter(data):
    req ={'mail_id':str(data)}
    res= json.dumps(api.get_user_by_mail(json.dumps(req)))
    return redirect(url_for('users.change',data=res))

@user_print.route('/new_password_create/<string:data>',methods=['POST','GET'])
def change(data):
    form = new_password()
    data = json.loads(data)['user']
    print(data['username'])
    req=dict()
    status = False
    ERROR =""
    if request.method=='POST':
        new_pass1 = form.pass1.data
        new_pass2 = form.re_enter.data
        if len(new_pass1)>0 and len(new_pass2)>0:
            if new_pass1==new_pass2:
                req['mail_id'] =data['email']
                req['new_password'] =form.re_enter.data
                res = api.send_changed_pass(json.dumps(req))
                print(res)
                if(res['status']):
                    status = True
                else:
                    flash("Can't process your request.")
            else:
                flash("Password not matched.")
        else:
            flash("Please enter New password.")
    return render_template('new_password.html',form=form,data=data,status=status)
