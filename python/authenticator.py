import datetime
import os
from flask import Blueprint, redirect, render_template, request, session, url_for
import bcrypt
import uuid
from .models import Profiles, Users, db

authenticator = Blueprint('authenticator', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../ProjectDB/media.db')
db_path = db_path.replace('\\', '/')

@authenticator.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = str(uuid.uuid4())
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        UserSince = datetime.datetime.now()
        new_user = Users(user_id=user_id, username=username, password=hashed_password.decode('utf-8'), UserSince=UserSince)
        db.session.add(new_user)

        #set up initial profile
        default_photo = 'ProjectDB/images/site_images/blank-profile.png'
        profile_id = str(uuid.uuid4())
        new_profile = Profiles(profile_id=profile_id, user_id=user_id, profile_photo=default_photo, bio="")
        db.session.add(new_profile)
        db.session.commit()
        
        return redirect(url_for('user.login'))

    return render_template('site_entrance/register.html')

@authenticator.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        
        user = Users.query.filter_by(username=username).first()
        
        if user:
            hashed_password = user.password.encode('utf-8')
            if bcrypt.checkpw(password, hashed_password):
                session['username'] = username
                return redirect(url_for('main.home'))
        return render_template('site_entrance/login.html')

    return render_template('site_entrance/login.html')

@authenticator.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove username from session if it's there
    if 'username' in session:
        session.clear()
    return redirect(url_for('user.login')) 
