from pasien.api import restplus
from pasien.models.table import Users
from flask_restplus import fields
from flask_jwt_extended import create_access_token
from werkzeug.datastructures import FileStorage
from sqlalchemy import or_
import enum
upload_parser = restplus.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

auth_model = restplus.model('AuthUser',{
                                'username':fields.String(description="Username/Email"),
                                'password':fields.String,
                            })

user_model = restplus.model('User',{
                                'email':fields.String,
                                'username':fields.String,
                                'password':fields.String,
                                'role' : fields.Integer,
                            })

user_model_edit = restplus.model('User',{
                                'email':fields.String,
                                'username':fields.String,
                                'active':fields.Boolean,
                                'role' : fields.Integer,
                            })

user_role_model = restplus.model('UserRole', {
                                "name" : fields.String,
                                "display_name" : fields.String,
                                "description" : fields.String,
                            })

change_password_model = restplus.model('PasswordChange', {
                                "old_password" : fields.String,
                                "password" : fields.String,
                            })

keluarga_model = restplus.model("Keluarga", {
                                "no_kk": fields.String,
                                "alamat" : fields.String,
                                "kepala_keluarga": fields.String,
                            })

pasien_model = restplus.model('Pasien', {
                                "nama" : fields.String,
                                "usia" : fields.Integer,
                                "goldar" : fields.String(enum=["A","B","O","AB"]),
                                "jk":fields.String(enum=["Laki-Laki","Perempuan"]),
                                "no_telp" : fields.String,
                                "kk" : fields.Nested(keluarga_model)
                            })

pasien_rj_model = restplus.model('PasienRJ', {
                                "nama" : fields.String,
                                "usia" : fields.Integer,
                                "goldar" : fields.String(enum=["A","B","O","AB"]),
                                "jk":fields.String(enum=["Laki-Laki","Perempuan"]),
                                "keluhan" : fields.String,
                                "tindakan" : fields.String,
                                "diagnosa" : fields.String,
                                "biaya" : fields.Integer,
                                "no_telp" : fields.String,
                                "status" : fields.String,
                            })

pasien_ri_model = restplus.model('PasienRI', {
                                "nama" : fields.String,
                                "usia" : fields.Integer,
                                "goldar" : fields.String(enum=["A","B","O","AB"]),
                                "jk":fields.String(enum=["Laki-Laki","Perempuan"]),
                                "diagnosa" : fields.String,
                                "biaya" : fields.Integer,
                                "status" : fields.String,
                            })

pasien_r_model = restplus.model('PasienR', {
                                "nama" : fields.String,
                                "usia" : fields.Integer,
                                "goldar" : fields.String(enum=["A","B","O","AB"]),
                                "jk":fields.String(enum=["Laki-Laki","Perempuan"]),
                                "no_kk": fields.String,
                                "alamat" : fields.String,
                                "kepala_keluarga": fields.String,
                                "asal" : fields.String,
                                "keterangan" : fields.String,
                                "diagnosa" : fields.String,
                                "biaya" : fields.Integer,
                                "status" : fields.String,
                            })

check_pasien = restplus.model('CheckPasien',{
    "nama" : fields.String,
    "no_kk" : fields.String
})

def auth(data):
    username = data["username"]
    password = data["password"]
    user = Users.query.filter(or_(Users.username==username,Users.email==username)).first()
    if user:
        if user.check_password(password):
            ret = {"access_token" : create_access_token(identity={"username":user.username, "role":user.role.name}), "user":user.username, "isadmin":user.isAdmin()}
            return ret
        else:
            return None
    return None
