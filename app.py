import os
from flask import Flask, send_from_directory
from python.routes import main as main_blueprint
from python.comments import comments as comments_blueprint
from python.utils import utils as utils_blueprint
from python.user import user as user_blueprint
from python.chat import chat as chat_blueprint
from python.models import db

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__,)

app.secret_key = 'khsVtN4iqXVFYncV6rkyd6SmtLZbjrUB'

db_path = os.path.join(basedir, 'static/ProjectDB/media.db')
profile_path = os.path.join(basedir, 'static/images/profile_images')
upload_path = os.path.join(basedir, 'static/content')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['PROFILE_UPLOAD_FOLDER'] = f'{profile_path}'
app.config['CONTENT_UPLOAD_FOLDER'] = f'{upload_path}'
db.init_app(app)

app.register_blueprint(main_blueprint)
app.register_blueprint(comments_blueprint)
app.register_blueprint(utils_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(chat_blueprint)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True, port=8000)