import requests
import json
from project import host_address


# All User operations here
class user_api():
    def check_mail(self, email):
        return Executer.get_json_wapper_('{}/user_check/{}'.format(host_address, email))['status']

    def register(self, username, email, password):
        return Executer.post_json_wapper_('{}/register/{}/{}/{}'.format(host_address, username, email, password))[
            'status']

    def login(self, email_, password):
        return Executer.get_json_wapper_('{}/login/{}/{}'.format(host_address, email_, password))

    def send_forget_pass(self, mail_id):
        return Executer.post_json_wapper('{}/password'.format(host_address), mail_id)

    def send_changed_pass(self, mail_id):
        return Executer.patch_json_wapper_('{}/password'.format(host_address), mail_id)

    def get_user_by_mail(self, mail):
        return Executer.post_json_wapper('{}/get_user'.format(host_address), mail)


# All project operations here
class project_api():
    def create(self, project_obj):
        return Executer.post_json_wapper(f'{host_address}/project', project_obj)

    def get_all(self, uid):
        return Executer.get_json_wapper_('{}/project/all/{}'.format(host_address, uid))

    def view(self, uid_pid):
        return Executer.post_json_wapper(f'{host_address}/project/view', json.dumps(uid_pid))

    def save_edited(self, project_obj):
        # this function must data in json
        return Executer.patch_json_wapper_(f'{host_address}/project', project_obj)

    def get_project_users(self, uid_pid):
        return Executer.post_json_wapper(f'{host_address}/project/users', json.dumps(uid_pid))

    def delete(self, uid_pid):
        return Executer.post_json_wapper(f'{host_address}/project/delete', json.dumps(uid_pid))

    def share(self, uid_pid_mail_id):
        return Executer.post_json_wapper(f'{host_address}/project/share', json.dumps(uid_pid_mail_id))

# All task operations here
class task_api():
    def create(self, task_obj):
        return Executer.post_json_wapper(f'{host_address}/task/create', task_obj)

    def get_all(self, task_obj):
        return Executer.post_json_wapper(f'{host_address}/task/all', json.dumps(task_obj))

    def delete(self, uid_pid_tid):
        return Executer.post(f'{host_address}/task/delete', json.dumps(uid_pid_tid))

    def complet_mark(self, uid_pid_tid):
        return Executer.post(f'{host_address}/task/marking', json.dumps(uid_pid_tid))

    def uncomplete_mark(self, uid_pid_tid):
        return Executer.patch(f'{host_address}/task/marking', json.dumps(uid_pid_tid))


# This is API executor class
class Executer():

    @staticmethod
    def get(url):
        return requests.get(url)

    @staticmethod
    def patch_(url):
        return requests.patch(url)

    @staticmethod
    def patch(url, json_data):
        return requests.patch(url, json_data)

    @staticmethod
    def post_(url):
        return requests.post(url)

    @staticmethod
    def post(url, json_data):
        return requests.post(url, json_data)

    @staticmethod
    def post_json_wapper(url, json_data):
        return json.loads(Executer.post(url, json_data).text)

    @staticmethod
    def post_json_wapper_(url):
        return json.loads(Executer.post_(url).text)

    @staticmethod
    def get_json_wapper_(url):
        return json.loads(Executer.get(url).text)

    @staticmethod
    def patch_json_wapper_(url, json_data):
        return json.loads(Executer.patch(url, json_data).text)
