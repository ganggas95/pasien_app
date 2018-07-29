from pasien import jwt, app
from flask import request

from pasien.core import requires_roles, create_no_pasien
from pasien.api import restplus, ns, make_response
from pasien.models.table import db, Keluarga, RawatInap,RawatJalan, Pasien, PasienRujukan
from pasien.api.schema import check_pasien, pasien_model
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
import logging, datetime

@ns.route("/pasien/<int:id>")
class PasienAPI(Resource):
    def get(self, id):
        pasien = Pasien.query.get(id)
        if pasien:
            return make_response(200, "Data pasien found", False, pasien.__serialize__())
        return make_response(404, 'Data pasien not found', True, None)
    def post(self, id):
        pasien = Pasien.query.get(id)
        data = request.get_json(force=True)
        if pasien:
            pasien.nama = data['nama']
            pasien.usia = data['usia']
            pasien.goldar = data['goldar']
            pasien.jk = data['jk']
            no_telp = data['telp']
            try:
                pasien = pasien.save()
                return make_response(201, "Data saved successfully", False, pasien.__serialize___())
            except Exception as e:
                return make_response(500, "Error when save data. Error : {}".format(e), True, None)        
        return make_response(500, "Data not found", True, None)
    def delete(self, id):
        pasien = Pasien.query.get(id)
        if pasien:
            try:
                pasien.delete()
                return make_response(201, "Data delete successfully", False, {"id" : id})
            except Exception as e:
                return make_response(500, "Error when delete data. Error: {}".format(e), True, None)
        return make_response(500, "Data not found", True, None)

@ns.route("/pasien/check")
class CheckPasien(Resource):
    @ns.expect(check_pasien)
    def post(self):
        data = request.get_json(force=True)
        if data:
            no_kk = data['no_kk']
            nama = data['nama']
            pasien = Pasien.query.filter(Pasien.nama.like('%{}%'.format(nama))).all()
            datas = []
            for p in pasien:
                datas.append(p.__serialize__())
            return make_response(200, "Data found with {} result".format(len(pasien)), False, datas)
        return make_response(400, "Bad Request", True, None)

@ns.route("/pasiens")
class PasiensAPI(Resource):
    @restplus.doc(params={"nama" : "Nama Pasien", 
                            "no_kk":"No KK", 
                            "no_pasien":"No Pasien", 
                            "page":"Page data", 
                            "perpage" : "Data per-page"})
    def get(self):
        pasien = Pasien.query.join(Keluarga)
        if request.args.get('nama'):
            pasien = pasien.filter(Pasien.nama.like('%{}%'.format(request.args.get('nama'))))
        if request.args.get('no_kk'):
            pasien = pasien.filter(Keluarga.no_kk == request.args.get('no_kk'))
        if request.args.get('no_pasien'):
            pasien = pasien.filter(Pasien.no_pasien == request.args.get('no_pasien'))
        
        pasien = pasien.all()
        datas = []
        for p in pasien:
            datas.append(p.__serialize__())
        page = request.args.get('page',type=int, default=1)
        perpage = request.args.get('perpage',type=int, default=10)
        startfrom = (page-1) * perpage
        return make_response(200, "Data found with {} result".format(len(datas[startfrom:startfrom+perpage])), False, 
                        {"items" : datas[startfrom:startfrom+perpage], "totalItem" : len(pasien)})
    @restplus.expect(pasien_model)
    def post(self):
        data = request.get_json(force=True)
        if data:
            pasien = Pasien()
            pasien.no_pasien = create_no_pasien()
            pasien.nama = data['nama']
            pasien.usia = data['usia']
            pasien.goldar = data['goldar']
            pasien.jk = data['jk']
            pasien.no_telp = data['no_telp']
            keluarga = Keluarga.query.filter(Keluarga.no_kk==data['no_kk']).first()
            if keluarga:
                pasien.keluarga = keluarga
            else:
                keluarga = Keluarga()
                keluarga.no_kk = data['no_kk']
                keluarga.kepala_keluarga = data['kepala_keluarga']
                keluarga.alamat = data['alamat']
                pasien.keluarga = keluarga
            try:
                pasien.save()
                return make_response(201, "Data success saved.", False, pasien.__serialize__())
            except Exception as e:
                return make_response(500, "Error when saving data. Error : {}".format(e), True, None)
        return make_response(400, "Bad request", True, None)