from flask import render_template, Blueprint
from flask_bootstrap import Bootstrap

main = Blueprint('main', __name__)

from . import views, errors