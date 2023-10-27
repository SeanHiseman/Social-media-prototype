import os
from flask import Flask, send_from_directory
from flask_socketio import socketio
from python.authenticator import authenticator as authenticator_blueprint
from python.routes import main as main_blueprint
from python.comments import comments as comments_blueprint
from python.utils import utils as utils_blueprint
from python.profiles import profiles as profiles_blueprint
from python.directMessages import dm as dm_blueprint
from python.models import db
from python.shared import socketio

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,)
socketio.init_app(app)
app.secret_key = 'randomKey'

db_path = os.path.join(basedir, 'static/ProjectDB/media.db')
profile_path = os.path.join(basedir, 'static/images/profile_images')
upload_path = os.path.join(basedir, 'static/content')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['PROFILE_UPLOAD_FOLDER'] = f'{profile_path}'
app.config['CONTENT_UPLOAD_FOLDER'] = f'{upload_path}'
db.init_app(app)

app.register_blueprint(authenticator_blueprint)
app.register_blueprint(dm_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(profiles_blueprint)
app.register_blueprint(utils_blueprint)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True, port=8000)