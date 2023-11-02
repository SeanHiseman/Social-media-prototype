from uuid import uuid4
from flask import Blueprint, jsonify, session
from sqlalchemy import and_, or_
from flask_socketio import emit
from .models import Conversations, Friends, UserConversations, Users, Messages, db
from .socketIOConfig import socketio

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
        conversation = Conversations.query.filter_by(friendship_id=friendship.friendship_id).first()
        friends_data.append({
            "friend_id": friend.user_id,
            "friend_name": friend.username,
            "conversation_id": conversation.conversation_id if conversation else None
        })
    
    return jsonify(friends_data)

@dm.route('/get_chat_messages/<conversation_id>', methods=['GET'])
def get_chat_messages(conversation_id):
    username = session.get('username')
    user = Users.query.filter_by(username=username).first()

    user_conversation = UserConversations.query.filter_by(user_id=user.user_id, conversation_id=conversation_id).first()
    if not user_conversation:
        return jsonify({"error": "Conversation not found"}), 403
    
    messages = Messages.query.filter_by(conversation_id=conversation_id).order_by(Messages.timestamp.asc()).all()

    messages_data = [{
        "sender_id": m.sender_id,
        "content": m.content,
        "timestamp": m.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    } for m in messages]

    return jsonify(messages_data)

@socketio.on('send_message', namespace='/chat')
def handle_messages(message):
    new_message = Messages(
        sender_id = message["sender_id"],
        conversation_id=message["conversation_id"],
        message_content = message["content"]
    )
    db.session.add(new_message)
    db.session.commit()

    emit('receive_message', message, broadcast=True, namespace='/chat')
