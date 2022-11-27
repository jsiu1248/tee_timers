from . import main
from flask import render_template, session, redirect, url_for, flash, current_app, request, abort, make_response, g
from .. import db
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_
from ..models import User, Role, Permission, Comment, Post, Day, UserProfile, State, City, GolfCourse, Gender, TimeOfDay, RideOrWalk, Handicap, Smoking, Drinking, PlayingType
from ..decorators import permission_required, admin_required
from .forms import PostForm, TechSupportForm, MatchForm, EditProfileForm, AdminLevelEditProfileForm, CommentForm
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
    user = User.query.filter_by(username = username).first()
    userprofile = db.session.query(UserProfile, Day, State, City, 
    Gender, TimeOfDay, RideOrWalk, Handicap, Smoking,
    Drinking, PlayingType, GolfCourse ).filter_by(id=user.id).join(Day, 
    UserProfile.day_id == Day.id, 
    isouter = True).join(State, UserProfile.state_id == State.id).join(City,
        UserProfile.city_id == City.id).join(Gender,
        UserProfile.gender_id == Gender.id).join(TimeOfDay, 
        UserProfile.time_of_day_id == TimeOfDay.id).join(RideOrWalk, 
        UserProfile.ride_or_walk_id == RideOrWalk.id).join(Handicap,
        UserProfile.handicap_id == Handicap.id).join(Smoking,
        UserProfile.smoking_id == Smoking.id).join(Drinking, 
        UserProfile.drinking_id == Drinking.id).join(PlayingType, 
        UserProfile.playing_type_id == PlayingType.id).join(GolfCourse, 
        UserProfile.golf_course_id == GolfCourse.id).first()

    posts = user.post.order_by(Post.timestamp.desc()).all()

    # have to add back pagination later
    return render_template('user.html', user=user, userprofile = userprofile, 
    posts = posts
    )


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
        return redirect(url_for('.user', username = username))
    current_user.follow(user)
    db.session.commit()
    flash(f"You are now following {username}")
    return redirect(url_for('.user', username = username))


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
        page = page,
        per_page=current_app.config['FOLLOWERS_PER_PAGE']
        ,
        error_out=False
        )
    # convert to only follower and timestamp
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html',
                           user=user,
                           title_text="Followers of",
                           endpoint='.followers',
                           pagination=pagination,
                           follows=follows)

@main.route('/edit_profile_admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    userprofile = UserProfile.query.get_or_404(id)

    form = AdminLevelEditProfileForm(user=user, userprofile = userprofile)
    if form.validate_on_submit():
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        userprofile.bio = form.bio.data
        userprofile.age = form.age.data
        # userprofile.city_id = form.city.data
        # current_user.state_id = form.state.data
        userprofile.gender_id = request.form.getlist('gender')
        userprofile.day_id = request.form.getlist('day')
        print(userprofile.gender_id)
        print( userprofile.day_id)
        days = "0000000"
        for i in userprofile.day_id:
            days_list = list(days)
            days_list[int(i)-1] = "1"
            days_changed = ''.join(days_list)
            days = days_changed
            # userprofile.avaliable_days = days_changed
        # print(days_changed) # 1100110
            
        # current_user.time_of_day_id = form.time_of_day.data
        # current_user.ride_or_walk_id = form.ride_or_walk.data
        # current_user.handicap_id = form.handicap.data
        # current_user.smoking_id = form.smoking.data
        # current_user.drinking_id = form.drinking.data
        # current_user.playing_type = form.playing_type.data

        # user.bio = form.bio.data
        ### need to add more info here
        # db.session.add(current_user._get_current_object())
        # db.session.commit()
        flash('The profile was updated.')
        return redirect(url_for('.user', username=user.username))
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    # We must ensure role field gets int data
    form.role.data = user.role_id
    form.name.data = user.name
    form.bio.data = userprofile.bio
    form.age.data = userprofile.age
    # form.city.data = userprofile.city_id
    # form.state.data = current_user.state_id
    # form.gender.data = userprofile.gender_id
    # form.day.data = current_user.day_id
    # form.time_of_day.data = current_user.time_of_day_id
    # form.ride_or_walk.data = current_user.ride_or_walk_id
    # form.handicap.data = current_user.handicap_id
    # form.smoking.data = current_user.smoking_id
    # form.drinking.data = current_user.drinking_id
    # form.playing_type.data = current_user.playing_type_id

    return render_template('edit_profile.html', form=form, user=user)






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
        page = page
        ,
        per_page=current_app.config['FOLLOWERS_PER_PAGE']
        ,
        error_out=False
        )
    # convert to only follower and timestamp
    follows = [{'user': item.following, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('following.html',
                           user = user,
                           title_text = "Following",
                           endpoint = '.following',
                           pagination = pagination,
                           follows = follows)

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
    """
    Filters users for user to message. 
    Return: redirects to match page
    """
    form = MatchForm()
    # passes users contained in a list to template
    # users = User.query.all()
    users = db.session.query(User, UserProfile).join(UserProfile, 
                UserProfile.id == User.id, 
                isouter = True).all()

    if request.method == 'POST':
        data = dict((key, request.form.getlist(key) if len(
            request.form.getlist(key)) > 0 else request.form.getlist(key)[0])
            for key in request.form.keys())
        gender_filter = UserProfile.gender_id.in_( data['gender'] if ('gender') in data else [] )
        day_filter = UserProfile.day_id.in_(data['day'] if ('day') in data else [])
        time_of_day_filter = UserProfile.time_of_day_id.in_(data['time_of_day'] if ('time_of_day') in data else [])
        ride_or_walk_filter = UserProfile.ride_or_walk_id.in_(data['ride_or_walk'] if ('ride or walk') in data else [])
        handicap_filter = UserProfile.handicap_id.in_(data['handicap'] if ('handicap') in data else [])
        smoking_filter = UserProfile.smoking_id.in_(data['smoking'] if 'smoking' in data else [])
        drinking_filter = UserProfile.drinking_id.in_(data['drinking'] if 'drinking' in data else [])
        playing_type_filter = UserProfile.playing_type_id.in_(data['playing_type'] if ('playing_type') in data else [])
        

        filter_list = []
        data_values = []
        data_columns = ['gender', 'day', 'time_of_day','ride_or_walk', 'handicap',
        'smoking','drinking','playing_type']
  
        for k in data_columns:
            try:
                if data[k]:
                    data_values.append(data[k])
                    
            except:
                    data_values.append([])
        data_filter = (gender_filter, day_filter, time_of_day_filter, ride_or_walk_filter, 
        handicap_filter, smoking_filter, drinking_filter, playing_type_filter)
        for i,j in zip(data_values, data_filter):
            try:
                if len(i) > 0:
                    filter_list.append(j)
            except:
                pass


        users = db.session.query(User, UserProfile).join(UserProfile, 
                UserProfile.id == User.id, 
                isouter = True).filter(and_(k for k in filter_list))
    return render_template('match.html',
                           users = users, form = form)


@main.route('/post/<slug>',  methods=["GET", "POST"])
@login_required
def post(slug):
    # passes post contained in a list respresented as post to template
    post = Post.query.filter_by(slug = slug).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body = form.body.data,
                          comment = post,
                          users = current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Comment submission successful.')
        return redirect(url_for('.composition', slug = post.slug, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        # Calculate last page number
        page = (post.comments.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page = page,
        per_page = current_app.config['COMMENTS_PER_PAGE'],
        error_out = False)
    comments = pagination.items
    # Use list so we can pass to _compositions template
    return render_template('post.html',
                           post = [post],
                           form = form,
                           comments = comments,
                           pagination = pagination)


@main.route('/comment/<slug>',  methods=["GET", "POST"])
@login_required
def comment(slug):
    form = CommentForm()
    comment = Comment(body=form.body.data,
                          comment = comment,
                          users = current_user._get_current_object())

    # passes post contained in a list respresented as post to template
    comment = Comment.query.filter_by(slug=slug).first_or_404()
    return render_template('_comment.html', comment=[comment], form = form)

@main.route('/comment_form',  methods=["GET", "POST"])
@login_required
def comment_form():
    form = CommentForm()
    # post = Post.query.filter_by(slug = slug).first_or_404()

    if form.validate_on_submit():
        # how to query the id of the post that just clicked and also the userid
        
        comment = Comment(description = form.description.data,
                            post_id = post.id , user_id = post.user_id)
        db.session.add(comment)
        db.session.commit()
    return render_template('comment_form.html',  form = form)

@main.route('/forum', methods=["GET","POST"])
@login_required
def forum():
    """
    showing all of the posts and paging it. 
    Return: redirects to forum page
    """
    form = PostForm()
    page = request.args.get('page', 1, type = int)
    # Pagination of the posts for all users
    pagination = \
        Post.query.order_by(Post.timestamp.desc()).paginate(
            page = page,
            per_page = current_app.config['POSTS_PER_PAGE'],
            error_out = False)
    # Convert to list
    posts = pagination.items

    return render_template('forum.html',
                           form = form, posts = posts, pagination = pagination)

# @main.route('/tech_support', methods=["GET","POST"])
# @login_required
# def tech_support():
#     form = TechSupportForm()
#     if form.validate_on_submit():
#         title_entered = form.title.data
#         tech_message_entered = form.tech_message.data
#         send_email('flaskwebdev.js@gmail.com', title_entered, tech_message_entered)
#     return render_template('tech_support.html', form = form)



@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    editing the profile. The user's profile is blank initially. 
    Return: redirects to edit_profile link
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        # current_user.age = form.age.data
        # current_user.city_id = form.city.data
        # current_user.state_id = form.state.data
        # current_user.bio = form.bio.data
        # current_user.gender_id = form.gender.data
        # current_user.day_id = form.day.data
    #     current_user.time_of_day_id = form.time_of_day.data
    #     current_user.ride_or_walk_id = form.ride_or_walk.data
    #     current_user.handicap_id = form.handicap.data
    #     current_user.smoking_id = form.smoking.data
    #     current_user.drinking_id = form.drinking.data
    #     current_user.playing_type_id = form.playing_type_id.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('You successfully updated your profile! Looks great.')
        return redirect(url_for('.user', username = current_user.username, Day = Day))
    form.name.data = current_user.name
    # form.age.data = current_user.age
    # form.city.data = current_user.city_id
    # form.state.data = current_user.state_id
    # form.bio.data = current_user.bio
    # form.gender.data = current_user.gender_id
    # form.day.data = current_user.day_id
    # form.time_of_day.data = current_user.time_of_day_id
    # form.ride_or_walk.data = current_user.ride_or_walk_id
    # form.handicap.data = current_user.handicap_id
    # form.smoking.data = current_user.smoking_id
    # form.drinking.data = current_user.drinking_id
    # form.playing_type.data = current_user.playing_type_id
    return render_template('edit_profile.html', form=form)


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    Editting the posts or creating them, or replyies. 
    NOTE: Maybe the functionality needs to be changed. 
    Return: Returns the edit_posts page
    """
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title = form.title.data, 
        post = form.description.data)
        db.session.add(posts)
        db.session.commit()
        posts.generate_slug()
        return render_template('create_post.html', form = form)
    return render_template('forum.html', form = form)


# @main.route('/edit/<slug>',  methods=["GET", "POST"])
# @login_required
# def edit_post(slug):
#     """
#     Edit each post. Login is required. 
#     Args: slug
#     Returns: edit_post.html to render the form and then edit
#     """
#     form = PostForm()
#     # searches for post by slug or 404
#     post = Post.query.filter_by(slug=slug).first_or_404()
#     # if not the user nor admin abort
#     if current_user.username != post.user.username and not current_user.can(Permission.ADMIN):
#         abort(403)  
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.description = form.post.data
#         composition.generate_slug()
#         db.session.add(post)
#         db.session.commit()
#         flash("Post updated")

#         # which slug is it directing to?
#         return redirect(url_for('.post', slug = post.slug))
        
#     # why is the data equaled back and forth - seems like it is doing the same thing twice
#     form.title.data = composition.title
#     form.post.data = post.description
#     return render_template('post.html', form=form)

# duplicated 
# @main.route('/editprofile/<int:id>', methods = ['GET', 'POST'])
# @login_required
# @admin_required
# def admin_edit_profile(id):
#     """
#     Admin access to editting other's profiles. Admin access and login is required. 
#     Args: id of user
#     """
#     form = AdminLevelEditProfileForm()

#     # Search for user based on ID and return 404 if None
#     user = User.query.filter_by(id = id).first_or_404()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.confirmed = form.confirmed.data
#         current_user.name = form.name.data
#         current_user.age = form.age.data
#         current_user.city_id = form.city.data
#         current_user.state_id = form.state.data
#         current_user.bio = form.bio.data
#         current_user.gender_id = form.gender.data
#         current_user.day_id = form.day.data
#         current_user.time_of_day_id = form.time_of_day.data
#         current_user.ride_or_walk_id = form.ride_or_walk.data
#         current_user.handicap_id = form.handicap.data
#         current_user.smoking_id = form.smoking.data
#         current_user.drinking_id = form.drinking.data
#         current_user.playing_type = form.playing_type.data
#         # filtering for the first role name by form.role.data
#         current_user.role = Role.query.filter_by(id = form.role.data).first()


#         db.session.add(current_user._get_current_object())
#         db.session.commit()
#         flash('You successfully updated {user.username}\'s profile.')
#         return redirect(url_for('.user', username=current_user.username))

#     # why is the data equaled back and forth - seems like it is doing the same thing twice
#     form.username.data = current_user.username
#     form.confirmed.data = current_user.confirmed
#     form.role.data = current_user.role_id
#     form.name.data = current_user.name
#     form.age.data = current_user.age
#     form.city.data = current_user.city_id
#     form.state.data = current_user.state_id
#     form.bio.data = current_user.bio
#     form.gender.data = current_user.gender_id
#     form.day.data = current_user.day_id
#     form.time_of_day.data = current_user.time_of_day_id
#     form.ride_or_walk.data = current_user.ride_or_walk_id
#     form.handicap.data = current_user.handicap_id
#     form.smoking.data = current_user.smoking_id
#     form.drinking.data = current_user.drinking_id
#     form.playing_type.data = current_user.playing_type_id
#     return render_template('edit_profile.html', form=form)
