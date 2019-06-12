import requests, json
from project import host_address


class user_api():
    def check_mail(self, email):
        return executer.get_json_wapper_('{}/user_check/{}'.format(host_address, email))['status']

    def register(self, username, email, password):
        return executer.post_json_wapper_('{}/register/{}/{}/{}'.format(host_address, username, email, password))[
            'status']

    def login(self, email_, password):
        return executer.get_json_wapper_('{}/login/{}/{}'.format(host_address, email_, password))


class project_api():
    def create(self, project_obj):
        return executer.post_json_wapper(f'{host_address}/project', project_obj)
        # return json.loads(requests.post(f'{host_address}/project', project_obj).text)

    def get_all(self, uid):
        return executer.get_json_wapper_('{}/project/all/{}'.format(host_address, uid))
        # return json.loads(requests.get('{}/project/all/{}'.format(host_address, uid)).text)

    def view(self, uid_pid):
        return executer.post_json_wapper(f'{host_address}/project/view', json.dumps(uid_pid))
        # return json.loads(requests.post(f'{host_address}/project/view', json.dumps(uid_pid)).text)

    def save_edited(self, project_obj):
        # this function must data in json
        return executer.patch_json_wapper_(f'{host_address}/project', project_obj)
        # return json.loads(requests.patch(f'{host_address}/project', project_obj).text)

    def get_project_users(self, uid_pid):
        return executer.post_json_wapper(f'{host_address}/project/users', json.dumps(uid_pid))
        # return json.loads(requests.post(f'{host_address}/project/users', json.dumps(uid_pid)).text)

    def delete(self, uid_pid):
        return executer.post_json_wapper(f'{host_address}/project/delete', json.dumps(uid_pid))
        # return json.loads(requests.post(f'{host_address}/project/delete', json.dumps(uid_pid)).text)

    def share(self, uid_pid_mail_id):
        return executer.post_json_wapper(f'{host_address}/project/share', json.dumps(uid_pid_mail_id))
        # return json.loads(requests.post(f'{host_address}/project/share', json.dumps(uid_pid_mail_id)).text)


class task_api():
    def create(self, task_obj):
        return executer.post_json_wapper(f'{host_address}/task/create', task_obj)
        # return json.loads(requests.post(f'{host_address}/task/create', task_obj).text)

    def get_all(self, task_obj):
        return executer.post_json_wapper(f'{host_address}/task/all', json.dumps(task_obj))
        # return json.loads(requests.post(f'{host_address}/task/all', json.dumps(task_obj)).text)

    def delete(self, uid_pid_tid):
        return executer.post(f'{host_address}/task/delete', json.dumps(uid_pid_tid))
        # return requests.post(f'{host_address}/task/delete', json.dumps(uid_pid_tid))

    def complet_mark(self, uid_pid_tid):
        return executer.post(f'{host_address}/task/marking', json.dumps(uid_pid_tid))
        # return requests.post(f'{host_address}/task/marking', json.dumps(uid_pid_tid))

    def uncomplete_mark(self, uid_pid_tid):
        return executer.patch(f'{host_address}/task/marking', json.dumps(uid_pid_tid))
        # return requests.patch(f'{host_address}/task/marking', json.dumps(uid_pid_tid))


class executer():

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
        return json.loads(executer.post(url, json_data).text)

    @staticmethod
    def post_json_wapper_(url):
        return json.loads(executer.post_(url).text)

    @staticmethod
    def get_json_wapper_(url):
        return json.loads(executer.get(url).text)

    @staticmethod
    def patch_json_wapper_(url, json_data):
        return json.loads(executer.patch(url, json_data).text)
