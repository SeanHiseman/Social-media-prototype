from flask import Blueprint, jsonify, session
from python.models import Friends, Users
from sqlalchemy import and_, or_
from flask_socketio import emit
from python.shared import socketio
from .models import Messages, db

dm = Blueprint('dm', __name__) #dm = direct messages

@dm.route('/get_friends', methods=['GET'])
def get_friends():
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()
    
    #Get friends for user, checks which user_id they are in the table
    friendships = Friends.query.filter(or_(Friends.user1_id == user.user_id,
                                           Friends.user2_id == user.user_id)).order_by(Friends.FriendSince.asc()).all()
    #Get friend data
    friends_data = []
    for friendship in friendships:
        #check if user1 is the logged in user
        friend_id = friendship.user1_id if friendship.user1_id != user.user_id else friendship.user2_id
        friend = Users.query.get(friend_id)
        if friend:
            friends_data.append({
                "friend_id": friend.user_id,
                "friend_name": friend.username
            })
    
    return jsonify(friends_data)

@dm.route('/get_chat_messages/<friend_id>', methods=['GET'])
def get_chat_messages(friend_id):
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()

    messages = Messages.query.filter(
        or_(
            and_(Messages.sender_id == user.user_id, Messages.receiver_id == friend_id),
            and_(Messages.receiver_id == user.user_id, Messages.sender_id == friend_id)
        )
    ).order_by(Messages.timestamp.asc()).all()

    messages_data = [{
        "sender_id": m.sender_id,
        "receiver_id": m.receiver_id,
        "content": m.content,
        "timestamp": m.timestamp
    } for m in messages]

    return jsonify(messages_data)

@socketio.on('send_message', namespace='/chat')
def handle_messages(message):
    new_message = Messages(
        sender_id = message["sender_id"],
        receiver_id = message["receiver_id"],
        content = message["content"]
    )
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', message, broadcast=True, namespace='/chat')
