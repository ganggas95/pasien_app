from functools import wraps
from flask import abort
from pasien.models.table import Pasien
from sqlalchemy import  desc
from flask_jwt_extended import get_jwt_identity
import logging, hashlib, uuid, datetime

ALLOWED_EXTENSIONS = set(['csv', 'png', 'jpg', 'jpeg', 'gif'])
number_pasien = 0
curdate_number = datetime.datetime.now().date()
def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in roles:
               abort(403, 'Forbidden Access')
            return f(*args, **kwargs)
        return wrapped
    return wrapper

def create_password(password):
    return hashlib.md5(str(hashlib.sha256(str(password).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def random_filename():
    unique_filename = uuid.uuid4()
    return str(unique_filename)

def create_no_pasien():
    global curdate_number
    global number_pasien
    number_pasien = number_pasien + 1
    curday = datetime.datetime.now().day
    curmont = datetime.datetime.now().month
    curyear = datetime.datetime.now().year
    pasien = Pasien.query.order_by(desc(Pasien.no_pasien)).filter(Pasien.no_pasien.like("%{}{}{}%".format(curyear, curmont, curday))).all()
    if len(pasien)==0:
        number_pasien = 0
        number_pasien = number_pasien + 1
        curdate_number = datetime.datetime.now().date()
    else:
        pasien = pasien[0]
        number_pasien = int(str(pasien.no_pasien).split("-")[1])+1
        curdate_number = datetime.datetime.now().date()
    number_ = ""
    if number_pasien<10:
        number_ = "00{}".format(number_pasien)
    if number_pasien>=10 and number_pasien<=99:
        number_ = "0{}".format(number_pasien)
    if number_pasien>99:
        number_ = "{}".format(number_pasien)
    return '{}{}{}-{}'.format(curyear,curmont,curday, number_)
