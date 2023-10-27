from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Content(db.Model):
    __tablename__ = 'Content'
    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(120), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    size = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Integer,nullable=False)
    views = db.Column(db.Integer,nullable=False)
    likes = db.Column(db.Integer,nullable=False)
    dislikes = db.Column(db.Integer,nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.String(36), nullable=True)

class Comments(db.Model):
    __tablename__ = "Comments"
    id = db.Column(db.String(36), primary_key=True)
    content_id = db.Column(db.String(36), db.ForeignKey('Content.id',ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.String(36), nullable=True)
    comment_text = db.Column(db.String(1000), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    dislikes = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    parent_id = db.Column(db.String(36), nullable=True)

class Profiles(db.Model):
    __tablename__ = "Profiles"
    profile_id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), nullable=False)
    profile_photo = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.String(1000), nullable=True)

class FriendRequests(db.Model):
    __tablename__ = 'FriendRequests'
    request_id = db.Column(db.String(36), primary_key=True,)
    sender_id = db.Column(db.String(36), db.ForeignKey('Users.user_id'))
    receiver_id = db.Column(db.String(36), db.ForeignKey('Users.user_id'))

#All conversations that each user is a part of 
class UserConversations(db.Model):
    __tablename__ = "UserConversations"
    user_id = db.Column(db.String(36), db.ForeignKey('Users.user_id'), primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('Conversations.conversation_id'), primary_key=True)

class Users(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    UserSince = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    friend_requests = relationship("FriendRequests", foreign_keys=[FriendRequests.receiver_id], backref="receiver")
    sent_requests = relationship("FriendRequests", foreign_keys=[FriendRequests.sender_id], backref="sender")
    conversations = db.relationship('Conversations', secondary='UserConversations', back_populates='users')

class Friends(db.Model):
    __tablename__ = 'Friends'
    friendship_id = db.Column(db.String(36), primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))
    FriendSince = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#Stores all conversations
class Conversations(db.Model):
    __tablename__ = "Conversations"
    conversation_id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Messages', backref='Conversations', lazy=True)
    users = db.relationship('Users', secondary='UserConversations', back_populates='conversations')

class Messages(db.Model):
    __tablename__ = "Messages"
    message_id = db.Column(db.String(36), primary_key=True)
    conversation_id = db.Column(db.String(36), db.ForeignKey('Conversations.conversation_id'), nullable=False)
    sender_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    message_content = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)