from flask import Blueprint, jsonify, session
from python.models import Friends, Users
from sqlalchemy import or_

chat = Blueprint('chat', __name__)

@chat.route('/get_messages', methods=['GET'])
def get_messages():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    
    #Get friends for user, checks which user_id they are in the table
    friendships = Friends.query.filter(or_(Friends.user1_id == user.user_id,
                                           Friends.user2_id == user.user_id)).order_by(Friends.FriendSince.asc()).all()
    
    #Get the user id's
    friend_ids = [f.user1_id if f.user1_id != user.user_id else f.user2_id for f in friendships] 
    
    #Get friends for the user.
    friends = Users.query.filter(Users.user_id.in_(friend_ids)).all()
    friend_names = [f.username for f in friends]
    friend_data = [{"friend_name": name} for name in friend_names]
    return jsonify(friend_data)

