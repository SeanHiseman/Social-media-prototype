import datetime
import os
from flask import Blueprint, jsonify, redirect, render_template, request, session, url_for
import bcrypt
import uuid
from .models import Content, FriendRequests, Friends, Profiles, Users, db
from .utils import fetch_profile_data

user = Blueprint('user', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../ProjectDB/media.db')
db_path = db_path.replace('\\', '/')

@user.route('/register', methods=['GET', 'POST'])
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

@user.route('/login', methods=['GET', 'POST'])
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

@user.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove username from session if it's there
    if 'username' in session:
        session.clear()
    return redirect(url_for('user.login')) 

@user.route('/profile/<url_profile_id>')
def profile(url_profile_id):
    if 'username' not in session:
        return redirect(url_for('user.login'))
    
    logged_in_data = fetch_profile_data(['profile_id', 'profile_photo'])
    if logged_in_data:
        logged_in_profile_id, logged_in_profile_photo = logged_in_data
    else: 
        logged_in_profile_id, logged_in_profile_photo = None, None    

    viewed_profile = Profiles.query.filter_by(profile_id=url_profile_id).first()
    viewed_user = Users.query.filter_by(user_id=viewed_profile.user_id).first()
    user_content = Content.query.filter_by(user_id=viewed_profile.user_id).order_by(Content.timestamp.desc()).all()
    for item in user_content:
        item.username = viewed_user.username
        item.profile_photo = viewed_profile.profile_photo
        #if user is viewing their own profile
        if url_profile_id == logged_in_profile_id:
            return render_template('profiles/personal_profile.html', 
                               username=session['username'], 
                               content_items=user_content,
                               logged_in_profile_id=logged_in_profile_id, 
                               logged_in_profile_photo=logged_in_profile_photo)
        elif viewed_profile:
            return render_template('profiles/public_profile.html', 
                               content_items=user_content, 
                               logged_in_profile_id=logged_in_profile_id, 
                               logged_in_profile_photo=logged_in_profile_photo,
                               current_profile_id=viewed_profile.profile_id,
                               current_profile_photo=viewed_profile.profile_photo)
        else:
            return "Profile not found", 404
    
@user.route('/send_request/<receiver_profile_id>', methods=['POST'])
def send_request(receiver_profile_id):
    receiverProfile = Profiles.query.filter_by(profile_id=receiver_profile_id).first()
    if not receiverProfile:
        return jsonify({"message": "Receiver profile not found"}), 404
    
    receiver_id = receiverProfile.user_id
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Sender user not found"}), 404
    
    sender_id = user.user_id
    request_id = str(uuid.uuid4()) 
    request = FriendRequests(request_id=request_id, sender_id=sender_id, receiver_id=receiver_id)

    existing_request = FriendRequests.query.filter_by(sender_id=sender_id, receiver_id=receiver_id).first()
    if existing_request:
        return jsonify({"message": "Friend request already sent"})

    db.session.add(request)
    db.session.commit()
    return jsonify({"message": "Friend request sent"})

@user.route('/accept_request/<request_id>', methods=['PUT'])
def accept_request(request_id):
    req = FriendRequests.query.get(request_id)
    if not req:
        return jsonify({"error": "Friend request not found"}), 404
    
    friendship_id = str(uuid.uuid4())
    FriendSince = datetime.datetime.now()
    friendship = Friends(friendship_id=friendship_id, user1_id=req.sender_id, user2_id=req.receiver_id, FriendSince=FriendSince)
    db.session.add(friendship)
    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Friend request accepted"})

@user.route('/reject_request/<request_id>', methods=['DELETE'])
def reject_request(request_id):
    req = FriendRequests.query.get(request_id)
    if not req:
        return jsonify({"error": "Friend request not found"}), 404
    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Friend request rejected"})

@user.route('/get_requests', methods=['GET'])
def get_requests():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    requests = [{"request_id": req.request_id, "from": req.sender_id, "senderName": req.sender.username} for req in user.friend_requests]
    return jsonify(requests)




