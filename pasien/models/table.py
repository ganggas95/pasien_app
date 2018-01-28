from pasien import app
from flask_sqlalchemy import SQLAlchemy
import hashlib, json, datetime, enum
from flask_migrate import Migrate
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)
class Users(db.Model):
    __tablename__ = "user"
    __table_args__={'extend_existing':True}
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True)
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    active = db.Column(db.Boolean, default=False)
    auth = False

    def is_active(self):
        return self.active

    def get_id(self):
        return self.id_user

    def is_authenticated(self):
        return self.auth

    def check_password(self, password):
        self.auth = self.password == hashlib.md5(str(hashlib.sha256(str(password).encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
        return self.auth

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __serialize__(self):
        return {
            "id_user" : self.id_user,
            "email" : self.email,
            "username" : self.username,
        }

class Goldar(enum.Enum):
    A = "A"
    B = "B"
    O = "O"
    AB = "AB"

class Keluarga(db.Model):
    __tablename__ = 'keluarga'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    no_kk = db.Column(db.String(45), unique=True)
    kepala_keluarga = db.Column(db.String(45))
    alamat = db.Column(db.Text)
    def save(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Pasien(db.Model):
    __tablename__ = 'pasien'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    no_pasien = db.Column(db.String(45), unique=True)
    nik = db.Column(db.String(45), unique=True)
    nama = db.Column(db.String(45))
    usia = db.Column(db.Integer)
    goldar = db.Column(db.Enum(Goldar))
    jk = db.Column(db.String(15))
    status = db.Column(db.String(15), default="Umum")
    no_telp = db.Column(db.String(12))
    keluarga_id = db.Column(db.Integer, db.ForeignKey("keluarga.id"))
    keluarga = db.relationship('Keluarga', backref='pasien')
    riwayat_rj = db.relationship('RawatJalan', foreign_keys="RawatJalan.pasien_id")
    riwayat_ri = db.relationship('RawatInap', foreign_keys="RawatInap.pasien_id")
    riwayat_rujukan = db.relationship('PasienRujukan', foreign_keys="PasienRujukan.pasien_id")
    riwayat_regular = db.relationship('Regular', foreign_keys="Regular.pasien_id")
    create_at = db.Column(db.DateTime)
    update_at = db.Column(db.DateTime)

    def __serialize__(self):
        return {
            "id" : self.id,
            "no_pasien" : self.no_pasien,
            "nama" : self.nama,
            "usia" : self.usia,
            "goldar" :self.goldar.name,
            "jk" : self.jk,
            "no_telp" : self.no_telp,
            "update_at" : self.update_at,
            "create_at" : self.create_at,
            "keluarga" : {
                "id" : self.keluarga.id,
                "no_kk" : self.keluarga.no_kk,
                "kepala_keluarga" : self.keluarga.kepala_keluarga,
                "alamat" : self.keluarga.alamat,
            }
        }
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    def delete(self):
        db.session.delete(self)
        db.session.commit()
class PasienRujukan(db.Model):
    __tablename__= 'pasien_rujukan'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    asal = db.Column(db.String(45))
    keterangan = db.Column(db.Text)
    rawat_inap_id = db.Column(db.Integer, db.ForeignKey('rawat_inap.id'))
    rawat_inap = db.relationship('RawatInap', backref="pasien_r_rawat_inap")
    pasien_id = db.Column(db.Integer, db.ForeignKey('pasien.id'))
    pasien = db.relationship('Pasien', backref="pasien_rujukan")

    def __serialize__(self):
        return {
            "id":self.id,
            "pasien":self.pasien.__serialize__(),
            "asal":self.asal,
            "keterangan":self.keterangan,
            "rawat_inap":self.rawat_inap.__serialize__(),
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

class RawatInap(db.Model):
    __tablename__= 'rawat_inap'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    tanggal_masuk = db.Column(db.DateTime)
    tanggal_keluar = db.Column(db.DateTime)
    diagnosa = db.Column(db.Text)
    status = db.Column(db.String(20))
    pasien_id = db.Column(db.Integer, db.ForeignKey('pasien.id'))
    pasien = db.relationship('Pasien', backref="rawat_inap")

    def __serialize__(self):
        return {
            "id":self.id,
            "pasien" : self.pasien.__serialize__(),
            "tanggal_masuk":self.tanggal_masuk,
            "tanggal_keluar":self.tanggal_keluar,
            "diagnosa":self.diagnosa,
            "status":self.status,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

class RawatJalan(db.Model):
    __tablename__= 'rawat_jalan'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date)
    keluhan = db.Column(db.Text)
    tindakan = db.Column(db.Text)
    diagnosa = db.Column(db.Text)
    status = db.Column(db.String(20))
    pasien_id = db.Column(db.Integer, db.ForeignKey('pasien.id'))
    pasien = db.relationship('Pasien', backref="rawat_jalan")

    def __serialize__(self):
        return{
            "id":self.id,
            "pasien":self.pasien.__serialize__(),
            "tanggal":self.tanggal,
            "keluhan":self.keluhan,
            "tindakan":self.tindakan,
            "diagnosa":self.diagnosa,
            "status":self.status,
        }
    def save(self):
        self.tanggal = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()

class Regular(db.Model):
    __tablename__= 'regular'
    __table_args__={"extend_existing":True}
    id= db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date)
    keluhan = db.Column(db.Text)
    tindakan = db.Column(db.Text)
    status = db.Column(db.String(20))
    pasien_id = db.Column(db.Integer, db.ForeignKey('pasien.id'))
    pasien = db.relationship('Pasien', backref="regular")

    def __serialize__(self):
        return{
            "id":self.id,
            "pasien":self.pasien.__serialize__(),
            "tanggal":self.tanggal,
            "tindakan":self.tindakan,
            "status":self.status,
        }
    def save(self):
        self.tanggal = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()
