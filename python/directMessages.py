import datetime
from uuid import uuid4
import uuid
from flask import Blueprint, jsonify, session
from sqlalchemy import and_, or_
from flask_socketio import emit
from .models import Conversations, Friends, UserConversations, Users, Messages, db
from .socketIOConfig import socketio

dm = Blueprint('dm', __name__) #dm = direct messages

@dm.route('/get_friends', methods=['GET'])
def get_friends():
    user_id = session.get('user_id')
    user = Users.query.filter_by(user_id=user_id).first()
    
    #Get friends for user, checks which user_id they are in the table
    friendships = Friends.query.filter(or_(Friends.user1_id == user.user_id,
                                           Friends.user2_id == user.user_id)).order_by(Friends.FriendSince.asc()).all()
    #Get friend data
    friends_data = []
    for friendship in friendships:
        #check if user1 is the logged in user
        friend_id = friendship.user1_id if friendship.user1_id != user.user_id else friendship.user2_id
        friend = Users.query.get(friend_id)
        conversation = UserConversations.query.filter(
            UserConversations.user_id.in_([user.user_id, friend_id])
        ).join(Conversations).first()
        friends_data.append({
            "friend_id": friend.user_id,
            "friend_name": friend.username,
            "conversation_id": conversation.conversation_id if conversation else None
        })
    
    return jsonify(friends_data)

@dm.route('/get_chat_messages/<conversation_id>', methods=['GET'])
def get_chat_messages(conversation_id):
    user_id = session.get('user_id')
    user = Users.query.filter_by(user_id=user_id).first()

    user_conversation = UserConversations.query.filter_by(user_id=user.user_id, conversation_id=conversation_id).first()
    if not user_conversation:
        return jsonify({"error": "Conversation not found"}), 403
    
    messages = Messages.query.filter_by(conversation_id=conversation_id).order_by(Messages.timestamp.asc()).all()

    messages_data = [{
        "senderId": m.sender_id,
        "content": m.message_content,
        "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for m in messages]

    return jsonify(messages_data)

@socketio.on('send_message', namespace='/chat')
def send_message(message):
    new_message = Messages(
        message_id = str(uuid.uuid4()),
        conversation_id=message["conversationId"],
        sender_id = message["senderId"],
        message_content = message["content"],
        timestamp=datetime.datetime.now()
    )
    print(len(message["content"]))
    if len(message["content"]) > 1000:
        return jsonify({"Message too long"}), 200
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', message, broadcast=True, namespace='/chat')
