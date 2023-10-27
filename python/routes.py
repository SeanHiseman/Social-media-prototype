from flask import Blueprint, redirect, render_template, request, session, url_for
from .models import Content, Profiles, Users
from .profiles import logged_in_profile_data

main = Blueprint('main', __name__)

@main.route('/home')
def home():
    #So that only logged in users can view
    if 'username' not in session:
        return redirect(url_for('authenticator.login'))
    
    profile_data = logged_in_profile_data(['profile_id', 'profile_photo'])
    if profile_data:
        logged_in_profile_id, logged_in_profile_photo = profile_data
        return render_template('home.html', 
                               username=session['username'], 
                               logged_in_profile_id=logged_in_profile_id, 
                               logged_in_profile_photo=logged_in_profile_photo)
    else:
        return render_template('home.html', username=session['username'])

@main.route('/recommended')
def recommended():
    if 'username' not in session:
        return redirect(url_for('authenticator.login'))

    # Displays correct profile photo when rendering page
    logged_in_profile_id, logged_in_profile_photo = logged_in_profile_data(['profile_id', 'profile_photo'])

    # Get all recommended content
    recommended_content = Content.query.all()

    # Usernames for recommended content
    user_ids = [item.user_id for item in recommended_content]
    users = Users.query.filter(Users.user_id.in_(user_ids)).all()
    username_map = {user.user_id: user.username for user in users}

    # profile details for recommended content
    profiles = Profiles.query.filter(Profiles.user_id.in_(user_ids)).all()
    profile_map = {profile.user_id: (profile.profile_id, profile.profile_photo) for profile in profiles}

    for item in recommended_content:
        item.username = username_map.get(item.user_id, 'Anonymous')
        item.profile_id, item.profile_photo = profile_map.get(item.user_id, (None, None))

    return render_template('contentFeed.html', 
                           content_items=recommended_content, 
                           username=session['username'], 
                           logged_in_profile_id=logged_in_profile_id, 
                           logged_in_profile_photo=logged_in_profile_photo)

@main.route('/following')
def following():
    if 'username' not in session:
        return redirect(url_for('authenticator.login'))

    # Displays correct profile photo when rendering page
    logged_in_profile_id, logged_in_profile_photo = logged_in_profile_data(['profile_id', 'profile_photo'])

    # Get all recommended content
    recommended_content = Content.query.all()

    # Usernames for recommended content
    user_ids = [item.user_id for item in recommended_content]
    users = Users.query.filter(Users.user_id.in_(user_ids)).all()
    username_map = {user.user_id: user.username for user in users}

    # profile details for recommended content
    profiles = Profiles.query.filter(Profiles.user_id.in_(user_ids)).all()
    profile_map = {profile.user_id: (profile.profile_id, profile.profile_photo) for profile in profiles}

    for item in recommended_content:
        item.username = username_map.get(item.user_id, 'Anonymous')
        item.profile_id, item.profile_photo = profile_map.get(item.user_id, (None, None))

    return render_template('contentFeed.html', 
                           content_items=recommended_content, 
                           username=session['username'], 
                           logged_in_profile_id=logged_in_profile_id, 
                           logged_in_profile_photo=logged_in_profile_photo)

@main.route('/personal')
def personal():
    if 'username' not in session:
        return redirect(url_for('authenticator.login'))

    # Displays correct profile photo when rendering page
    logged_in_profile_id, logged_in_profile_photo = logged_in_profile_data(['profile_id', 'profile_photo'])

    # Get all recommended content
    recommended_content = Content.query.all()

    # Usernames for recommended content
    user_ids = [item.user_id for item in recommended_content]
    users = Users.query.filter(Users.user_id.in_(user_ids)).all()
    username_map = {user.user_id: user.username for user in users}

    # profile details for recommended content
    profiles = Profiles.query.filter(Profiles.user_id.in_(user_ids)).all()
    profile_map = {profile.user_id: (profile.profile_id, profile.profile_photo) for profile in profiles}

    for item in recommended_content:
        item.username = username_map.get(item.user_id, 'Anonymous')
        item.profile_id, item.profile_photo = profile_map.get(item.user_id, (None, None))

    return render_template('contentFeed.html', 
                           content_items=recommended_content, 
                           username=session['username'], 
                           logged_in_profile_id=logged_in_profile_id, 
                           logged_in_profile_photo=logged_in_profile_photo)

@main.route('/search', methods=['GET'])
def search():
    if 'username' not in session:
        return redirect(url_for('authenticator.login'))
    #Displays correct profile photo when rendering page
    logged_in_profile_id, logged_in_profile_photo = logged_in_profile_data(['profile_id', 'profile_photo'])

    keyword = request.args.get('keyword', '')
    results = Content.query.filter(Content.title.like(f'%{keyword}%')).all()

    #Usernames for results
    user_ids = [item.user_id for item in results]
    users = Users.query.filter(Users.user_id.in_(user_ids)).all()
    username_map = {user.user_id: user.username for user in users}

    #profile details for results
    profiles = Profiles.query.filter(Profiles.user_id.in_(user_ids)).all()
    profile_map = {profile.user_id: (profile.profile_id, profile.profile_photo) for profile in profiles}

    for item in results:
        item.username = username_map.get(item.user_id, 'Anonymous')
        item.profile_id, item.profile_photo = profile_map.get(item.user_id, (None, None))

    return render_template('contentFeed.html', 
                           content_items=results, 
                           username=session['username'], 
                           logged_in_profile_id=logged_in_profile_id, 
                           logged_in_profile_photo=logged_in_profile_photo)



