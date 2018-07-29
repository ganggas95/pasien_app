from flask import Flask
from flask import jsonify
from flask import abort
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask_cors import CORS
from flask_compress import Compress
from flask_jwt_extended import JWTManager
from flask_login import current_user
from pasien.api import restplus
import os
import datetime



app = Flask(__name__)
cors = CORS(app)
app.config['SESSION_TYPE'] = "memcached"
app.config['SECRET_KEY'] = "PUSKESMAS Bismillah!#@$$%^()"
DATA_FOLDER = os.path.sep+"data"+os.path.sep
app.config['DATA_FOLDER'] = app.root_path + DATA_FOLDER
app.config['THREADS_PER_PAGE'] = 2
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://uqkoptfi4dswoven:MWdsDu7z0hTiZUA7JH4@byoo9phnm-mysql.services.clever-cloud.com:3306/byoo9phnm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
app.config["COMPRESS_LEVEL"] = 6
app.config["COMPRESS_MIN_SIZE"] = 500
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=10)
app.debug = True
Compress(app)

jwt = JWTManager(app)
@jwt.expired_token_loader
def loader_handler():
    abort(401, "Token Expired")

@app.route("/")
def index():
    return redirect(url_for('admin_login'))

from pasien import view, api, url
from pasien.api.administration import ns as ns_admin
from pasien.api.pasien import ns as ns_pasien
blueprint = Blueprint('api',__name__, url_prefix="/service")
restplus.init_app(blueprint)
restplus.add_namespace(ns_admin)
restplus.add_namespace(ns_pasien)
app.register_blueprint(blueprint)


if __name__ == "__main__":
    app.run()
