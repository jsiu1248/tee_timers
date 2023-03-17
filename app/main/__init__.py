from flask import render_template, Blueprint
from flask_bootstrap import Bootstrap

from app.models import Permission

main = Blueprint('main', __name__)

from . import views, errors

@main.app_context_processor
def inject_permissions():
    """ 
    Adding Permission to app_context
    """
    return dict(Permission=Permission)