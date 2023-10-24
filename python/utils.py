import os
import datetime
import uuid
from flask import Blueprint, current_app as app, jsonify, request, session
from .models import Content, Users, db
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip

utils = Blueprint('utils', __name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir,'ProjectDB','media.db')
db_path = db_path.replace('\\', '/')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'mp4', 'mkv', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@utils.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        title = request.form.get('title')
    
        if not title:
            return jsonify({"status": "error", "message": "Title cannot be empty"})
    
        if file and allowed_file(file.filename):
            id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['CONTENT_UPLOAD_FOLDER'], filename)
            file.save(filepath)
        
            file_size = os.path.getsize(filepath) // 1024  # size in KB
            content_type = 'image' if filepath.split('.')[-1] in ['jpg', 'jpeg', 'png', 'gif'] else 'video'
            duration = None
        
            if content_type == 'video':
                clip = VideoFileClip(filepath)
                duration = clip.duration  
        
            #user_id associated with session username
            user = Users.query.filter_by(username=session['username']).first()
            if user:
                user_id = user.user_id
            else:
                return jsonify({"status": "error", "message": "Could not fetch user_id"})

            timestamp = datetime.datetime.now()
            content = Content(id=id, title=title, path=f'content/{filename}', content_type=content_type, duration=duration, 
                              size=file_size, comments=0, views=0, likes=0, dislikes=0, user_id=user_id, timestamp=timestamp,)
            db.session.add(content)
            db.session.commit()

            return jsonify({"status": "success", "message": "File successfully uploaded."})
        else:
            return jsonify({"status": "error", "message": "File not allowed." }),400
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

@utils.route('/<action>/<contentId>', methods=['POST'])
def content_reaction(action, contentId):
    content = Content.query.get(contentId)
    if content:
        if action == 'like':
            content.likes += 1
        elif action == 'dislike':
            content.dislikes += 1
        db.session.commit()
        return jsonify(success=True), 200
    return jsonify(success=False), 404

@utils.route('/load_more', methods=['GET'])
def load_more():
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    content_items = Content.query.offset(offset).limit(limit).all()

    content_json = [
        {
            "id": item.id,
            "title": item.title,
            "path": item.path,
            "content_type": item.content_type,
            "duration": item.duration,
            "size": item.size,
            "comments": item.comments,
            "views": item.views,
            "likes": item.likes,
            "dislikes": item.dislikes,
            "timestamp": item.timestamp,
            "uploader_id": item.uploader_id,
        }
        for item in content_items
    ]

    return jsonify(content_json)






