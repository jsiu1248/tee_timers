from flask import render_template,  Blueprint

api = Blueprint('api' ,__name__ , url_prefix="/api/v1") 

# from . import authentication, comments, compositions, errors, users