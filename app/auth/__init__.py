from flask import render_template,  Blueprint

auth = Blueprint('auth' ,__name__ , url_prefix="/auth") 

from . import views
