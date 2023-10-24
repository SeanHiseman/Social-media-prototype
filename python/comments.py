import datetime
import uuid
from flask import Blueprint, jsonify, request
from .models import Comments, Content, Users, Profiles, db
from .profiles import logged_in_profile_data
comments = Blueprint('comments', __name__)

@comments.route('/get_comments/<content_id>', methods=['GET'])
def get_comments(content_id):
    #joins the Comments and Profiles tables
    comments = db.session.query(
        Comments, Users.username, Profiles.profile_photo
    ).join(
        Users, Comments.user_id == Users.user_id
    ).outerjoin(
        Profiles, Comments.user_id == Profiles.user_id
    ).filter(
        Comments.content_id == content_id
    ).all()
    
    # Convert results to dictionaries
    comments_dict = [{
        'id': comment[0].id,
        'content_id': comment[0].content_id,
        'user_id': comment[0].user_id,
        'comment_text': comment[0].comment_text,
        'likes': comment[0].likes,
        'dislikes': comment[0].dislikes,
        'timestamp': comment[0].timestamp,
        'parent_id': comment[0].parent_id,
        'username': comment[1],
        'profile_photo': comment[2]
    } for comment in comments]


    return jsonify(comments_dict)

@comments.route('/api/add_comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    user_id_tuple  = logged_in_profile_data(['user_id'])
    id = str(uuid.uuid4())
    content_id = data.get('content_id')
    parent_id = data.get('parent_id', None)
    comment_text = data.get('comment_text')
    
    if user_id_tuple:
        user_id = user_id_tuple[0]
    else:
        return jsonify({'success': False, 'message': 'Could not fetch user_id'})

    if content_id is None or comment_text is None:
        return jsonify({'success': False, 'message': 'Missing required fields'})
    
    try:
        timestamp = datetime.datetime.now()
        new_comment = Comments(id=id, content_id=content_id, user_id=user_id, comment_text=comment_text, 
                               likes=0, dislikes=0, timestamp=timestamp, parent_id=parent_id)
        db.session.add(new_comment)
        
        content_to_update = Content.query.filter_by(id=content_id).first()
        content_to_update.comments += 1

        db.session.commit()

        return jsonify({'success': True})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': str(e)})

@comments.route('/api/like_dislike', methods=['POST'])
def like_dislike_comment():
    data = request.get_json()
    comment_id = data.get('comment_id')
    reaction_type = data.get('reaction_type')

    if comment_id is None or reaction_type not in ['like', 'dislike']:
        return jsonify({'success': False, 'message': 'Invalid or missing parameters'})

    try:
        comment_to_update = Comments.query.filter_by(id=comment_id).first()
        if not comment_to_update:
            return jsonify({'success': False, 'message': 'Comment not found'})

        if reaction_type == 'like':
            comment_to_update.likes += 1
        elif reaction_type == 'dislike':
            comment_to_update.dislikes += 1

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})