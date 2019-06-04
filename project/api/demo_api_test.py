from flask import Blueprint
from project.api.db_helper.users_data import get_all
api = Blueprint('api', __name__)


@api.route('/getdate')
def demo():
    return get_all()
