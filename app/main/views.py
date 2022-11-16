from . import main
from flask import render_template, session, redirect, url_for, flash, current_app, request, abort, make_response, g
from .. import db
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from ..models import User, Role, Permission, Comment
from ..decorators import permission_required, admin_required
from .forms import CommentForm, TechSupportForm, SimpleForm, MatchForm
from ..email import send_email

""" was trying to fix CSRF error"""
# @main.before_app_request
# def fix_missing_csrf_token():
#     if current_app.config['WTF_CSRF_FIELD_NAME'] not in session:
#         if current_app.config['WTF_CSRF_FIELD_NAME'] in g:
#             g.pop(current_app.config['WTF_CSRF_FIELD_NAME'])

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    """route will require login and user to have admin permission"""
    return f"Welcome, Administrator! {Permission.ADMIN}"

# route will pass user_name variable
@main.route('/user/<username>')
def user(username):
    # query user or return error
    user = User.query.filter_by(username = username).first_or_404()
    # have to add back pagination later
    return render_template('user.html', user=user)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderators_only():
    """
    route will require login and the user to have moderate permissions
    """
    return "Greetings, moderator!"

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    """ follow a destinated user and making sure the user exists and if they are already following them.
    Args: user who you want to follow
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("That is not a valid user.")
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash("Looks like you are already following that user.")
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are now following {username}")
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    """ unfollow a user. Checks if following already
    Args: user who you want to unfollow
    Returns: user.html takes you back to user profile"""
    user = User.query.filter_by(username=username).first()
    # if not a user
    if user is None:
        flash("That is not a valid user.")
        return redirect(url_for('.index'))
    # if not already following that user
    if not current_user.is_a_follower(user):
        flash("You are not following that user.")
        return redirect(url_for('.user', username=username))
    # unfollow user and take row out from database
    current_user.unfollow(user)
    db.session.commit()
    flash(f"You have unfollowed {username}")
    # redirects to user profile
    return redirect(url_for('.user', username=username))






@main.route('/followers/<username>')
def followers(username):
    """ Get and paginate users. Get the user in question and if they don't exist then go 
    through a notification. A pagination object is created from the user's followers. Query for followers returns a list of
    follow instances. Only the follower users are needed. Another list is created that gives only
    the follower users and the timestamp
        Args: username (str): name of the user who has followers
        Returns: followers.html returns a page displaying the followers of the user
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("That is not a valid user.")
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page,
        per_page=current_app.config['RAGTIME_FOLLOWERS_PER_PAGE'],
        error_out=False)
    # convert to only follower and timestamp
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',
                           user=user,
                           title_text="Followers of",
                           endpoint='.followers',
                           pagination=pagination,
                           follows=follows)





@main.route('/following/<username>')
def following(username):
    """
    Show users a particular user is already following
    Args: username(str) : showing who this user follows
    Return: following.html returns page displaying user following who
    """
    user = User.query.filter_by(username=username).first()
    # if not a user
    if user is None:
        flash("That is not a valid user.")
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    # display page with list of users who user is following
    pagination = user.following.paginate(
        page,
        per_page=current_app.config['RAGTIME_FOLLOWERS_PER_PAGE'],
        error_out=False)
    # convert to only follower and timestamp
    follows = [{'user': item.following, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('following.html',
                           user=user,
                           title_text="Following",
                           endpoint='.following',
                           pagination=pagination,
                           follows=follows)

@main.route('/all')
@login_required
def show_all():
    #  automatically makes response objects out of whatever you pass in the return statement,
    # make_response() function takes the name of the cookie first, then the value it will take on
    resp = make_response(redirect(url_for('.index')))
    # max_age argument sets the number of seconds until the cookie expires
    resp.set_cookie('show_followed', '', max_age=30*24*60*60) # 30 days
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60) # 30 days
    return resp

# @main.route('/match/<slug>')
# @login_required
# def match(slug):
#     # passes user contained in a list to template
#     user = User.query.filter_by(username = username).first_or_404()
#     return render_template('match.html',
#                            user=[user])

@main.route('/match', methods=["GET","POST"])
@login_required
def match():
    form = MatchForm()
    # passes users contained in a list to template
    users = User.query.all()
    # if request.method == 'POST': 
    #     print(request.form.getlist('mycheckbox'))
    #     return 'Done'
    if request.method == 'POST':
        data = dict((key, request.form.getlist(key) if len(
            request.form.getlist(key)) > 0 else request.form.getlist(key)[0])
            for key in request.form.keys())
        users = User.query.filter(User.gender.in_( data['gender']) | 
        User.day_id.in_(data['day']) |  User.time_of_day_id.in_(data['time_of_day']) | 
        User.ride_or_walk_id.in_(data['ride_or_walk']) | User.handicap_id.in_(data['handicap']) |
        User.smoking_id.in_(data['smoking']) | User.alcohol_id.in_(data['drinking']) | 
        User.playing_type.in_(data['playing_type']))
          
        print (data) 


    return render_template('match.html',
                           users = users, form = form)


@main.route('/comment/<slug>',  methods=["GET", "POST"])
@login_required
def comment(slug):
    # passes comment contained in a list respresented as comment to template
    comment = Comment.query.filter_by(slug=slug).first_or_404()
    return render_template('comment.html', comment=[comment])


@main.route('/forum', methods=["GET","POST"])
@login_required
def forum():
    form = CommentForm()
    return render_template('forum.html',
                           form = form)

# @main.route('/tech_support', methods=["GET","POST"])
# @login_required
# def tech_support():
#     form = TechSupportForm()
#     if form.validate_on_submit():
#         title_entered = form.title.data
#         tech_message_entered = form.tech_message.data
#         send_email('flaskwebdev.js@gmail.com', title_entered, tech_message_entered)
#     return render_template('tech_support.html', form = form)


# @main.route('/test', methods=['POST', 'GET'])
# def test():
#     categories = ['Gender', 'Day', 'Time of Day', 'Ride or Walk', 'Handicap', 'Smoking', 'Drinking', 'Playing Type']
#     cells = [['Male','Female','Other'],['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday'],
#     ['Morning','Afternoon'], ['Cart','Walk'], ['20+','15-20','10-15','5-10','0-5'],['Yes','No'],['Yes','No'],
#     ['Leisure','Betting','Competitive','Driving Range']
#     ]

#     if request.method == "POST":
#         data = dict((key, request.form.getlist(key) if len(
#             request.form.getlist(key)) > 1 else request.form.getlist(key)[0])
#             for key in request.form.keys())
#         print (data) 

#     return render_template('match.html',
#        categories = categories,
#     cells = cells,
#        )
