from flask import Blueprint
from reasearch.api.demo_hit import get_all
api = Blueprint('api', __name__)


@api.route('/getdate')
def demo():
    return get_all()
