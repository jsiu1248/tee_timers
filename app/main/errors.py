from . import main
from flask import jsonify, request, render_template

@main.app_errorhandler(404)
def page_not_found(e):
    # accept_mimetypes is a shortcut to the contents of the Accept header
    # this head tells the server what type of response that the client expects
    # only accepting json and not html
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        # jsonify takes a dictionary and returns a response
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    error_title="Page Not Found"
    error_msg="That page doesn't exist."
    return render_template(
        'error.html',
        error_title=error_title,
        error_msg=error_msg), 404          

@main.app_errorhandler(500)
def internal_server_error(e):
    # accept_mimetypes is a shortcut to the contents of the Accept header
    # this head tells the server what type of response that the client expects
    # only accepting not json and html
    if not request.accept_mimetypes.accept_json and \
            request.accept_mimetypes.accept_html:
        # jsonify takes a dictionary and returns a response
        response = jsonify({'error': 'server error'})
        response.status_code = 500
        return response
    error_title="Internal Server Error"
    error_msg="Sorry, technical difficulties."
    return render_template(
        'error.html',
        error_title=error_title,
        error_msg=error_msg), 500       