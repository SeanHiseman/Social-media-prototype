import datetime
import os
from flask import Blueprint, app, jsonify, redirect, render_template, request, session, url_for, flash
import uuid
from werkzeug.utils import secure_filename
from .models import Content, FriendRequests, Friends, Profiles, Users, db
from .utils import allowed_file

profiles = Blueprint('profiles', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../ProjectDB/media.db')
db_path = db_path.replace('\\', '/')

@profiles.route('/profile/<url_profile_id>')
def load_profile(url_profile_id):
    if 'username' not in session:
        return redirect(url_for('user.login'))
    
    #gets data for logged in user
    logged_in_data = logged_in_profile_data(['profile_id', 'profile_photo'])
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
                               logged_in_profile_photo=logged_in_profile_photo,
                               profile_bio=viewed_profile.bio)
        elif viewed_profile:
            return render_template('profiles/public_profile.html', 
                               content_items=user_content, 
                               logged_in_profile_id=logged_in_profile_id, 
                               logged_in_profile_photo=logged_in_profile_photo,
                               current_profile_id=viewed_profile.profile_id,
                               current_profile_photo=viewed_profile.profile_photo,
                               profile_bio=viewed_profile.bio)
        else:
            return "Profile not found", 404
    
@profiles.route('/send_friend_request/<receiver_profile_id>', methods=['POST'])
def send_friend_request(receiver_profile_id):
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

@profiles.route('/accept_friend_request/<request_id>', methods=['PUT'])
def accept_friend_request(request_id):
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

@profiles.route('/reject_friend_request/<request_id>', methods=['DELETE'])
def reject_friend_request(request_id):
    req = FriendRequests.query.get(request_id)
    if not req:
        return jsonify({"error": "Friend request not found"}), 404
    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Friend request rejected"})

@profiles.route('/get_friend_requests', methods=['GET'])
def get_friend_requests():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    requests = [{"request_id": req.request_id, "from": req.sender_id, "senderName": req.sender.username} for req in user.friend_requests]
    return jsonify(requests)

PROFILE_UPLOAD_FOLDER = 'static/images/profile_images'    
@profiles.route('/update_profile_photo', methods=['POST'])
def update_profile_photo():
    if 'username' not in session:
        return redirect(url_for('user.login'))
    
    profile_id = logged_in_profile_data(['profile_id'])[0]
    
    if 'new_profile_photo' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['new_profile_photo']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename))

        #Update the profile_photo in the database
        new_photo_path = os.path.join('images/profile_images', filename) 
        new_photo_path = os.path.normpath(new_photo_path).replace('\\', '/')
              
        profile = Profiles.query.filter_by(profile_id=profile_id).first()
        if profile:
            profile.profile_photo = new_photo_path
            db.session.commit()

        return redirect(url_for('user.profile', url_profile_id=profile_id))

    else:
        flash('File not allowed. Please upload an image.')
        return redirect(request.url)

@profiles.route('/update_bio', methods=['POST'])
def update_bio():
    try:
        bio = request.json.get('bio')
        profile_id = logged_in_profile_data(['profile_id'])[0]
        profile = Profiles.query.filter_by(profile_id=profile_id).first()
        if profile:
            profile.bio = bio
            db.session.commit()
            return redirect(url_for('user.profile', url_profile_id=profile_id))
        else:
            return jsonify({"message": "Profile not found"}), 404
    except Exception as e:
        print(str(e))
        return jsonify({"message": "Failed to update bio"}), 500

#Access specific data for logged in user
def logged_in_profile_data(columns=['profile_id', 'profile_photo']):
    #Prevent SQL injection
    valid_columns = {'profile_id', 'user_id', 'profile_photo', 'bio'}
    if not all(col in valid_columns for col in columns):
        raise ValueError("Invalid column names")
    
    username = session.get('username')
    if not username:
        return None

    user = Users.query.filter_by(username=username).first()
    if not user:
        return tuple(None for _ in columns)
    
    profile = Profiles.query.filter_by(user_id=user.user_id).first()
    if profile:
        return tuple(getattr(profile, col) for col in columns)
    else:
        return tuple(None for _ in columns)




