from pasien import jwt, app
from flask import request, jsonify, abort
from pasien.core import requires_roles, create_password, random_filename, allowed_file
from pasien.api import restplus, ns
from pasien.models.table import Users, db, Keluarga, RawatInap,\
                                RawatJalan, Pasien, PasienRujukan
from pasien.api.schema import user_model, auth, upload_parser, auth_model, user_role_model, user_model_edit, change_password_model
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
import logging

@ns.route("/auth")
@restplus.response(403, "Forbidden")
@restplus.doc('auth_post')
class Authentication(Resource):
    @restplus.expect(auth_model)
    def post(self):
        token = auth(request.get_json(force=True))
        if token is None:
            abort(403,"Error credential")
        return jsonify(token)        
        

# @ns.route("/roles")
# @restplus.response(403, 'Forbidden Access')
# @restplus.doc('roles')
# class UserRoleApi(Resource):
#     @restplus.header("Authorization", 'Bearer', required=True)
#     @jwt_required
#     @requires_roles('admin')
#     def get(self):
#         roles = UserRole.query.all()
#         data = []
#         for role in roles:
#             data.append(role.__serialize__())
#         return jsonify(data)

#     @restplus.header("Authorization", 'Bearer', required=True)
#     @jwt_required
#     @requires_roles('admin')
#     @restplus.expect(user_role_model)
#     def post(self):
#         data = request.get_json(force=True)
#         if data:
#             role = UserRole()
#             role.name = data['name']
#             role.display_name = data['display_name']
#             role.description = data['description']
#             try:
#                 db.session.add(role)
#                 db.session.commit()
#             except Exception as e:
#                 abort(500, "Save data with error : {}".format(e))
#             return jsonify({"success":"Data success added!!!"})
#         abort(400, "Bad request")

# @ns.route('/roles/<int:id>')
# @restplus.response(403, 'Forbidden Access')
# @restplus.doc('user_role')
# class UserRoleApi(Resource):
#     @restplus.header("Authorization", 'Bearer', required=True)
#     @jwt_required
#     @requires_roles('admin')
#     def get(self, id):
#         role = UserRole.query.get(id)
#         if role:
#             return jsonify(role.__serialize__())
#         abort(404, "Data not found")
#     @restplus.header("Authorization", 'Bearer', required=True)
#     @jwt_required
#     @requires_roles('admin')
#     @restplus.expect(user_role_model)
#     def post(self, id):
#         data = request.get_json(force=True)
#         if data:
#             role = UserRole.query.get(id)
#             if role:
#                 role.name = data['name']
#                 role.display_name = data['display_name']
#                 role.description = data['description']
#                 try:
#                     db.session.add(role)
#                     db.session.commit()
#                 except Exception as e:
#                     abort(500, "Data saved with error: {}".format(e))
#                 return jsonify({"success":"Data saved success..."})
#             abort(404, "Data not found")
#         abort(400, "Bad request")
#     @restplus.header("Authorization", 'Bearer', required=True)
#     @jwt_required
#     @requires_roles('admin')
#     def delete(self, id):
#         role = UserRole.query.get(id)
#         if role:
#             try:
#                 db.session.delete(role)
#                 db.session.commit()
#             except Exception as e:
#                 abort(500, "Delete data with error: {}".format(e))
#             return jsonify({"success":"Data success deleted!!!"})
#         abort(404, "Data not found!!!")
@ns.route('/users')
@restplus.response(403, 'Forbidden Access')
@restplus.doc('users')
class UsersApi(Resource):
    @restplus.header("Authorization", 'Bearer', required=True)
    @jwt_required
    @restplus.doc(params={"page":"number of page"})
    @restplus.doc(params={"search" : "Username/Email User"})
    @restplus.doc(params={"role" : "User Role"})
    @requires_roles("admin")
    def get(self):
        users = Users.query
        # if request.args.get('role'):
        #     users = users.join(UserRole).filter(UserRole.name==request.args.get('role'))
        if request.args.get('search'):
            users = users.filter(Users.username.like("%"+request.args.get('search')+"%"), Users.email.like('%'+request.args.get('search')+'%'))
        users = users.all()
        if len(users)>0:
            data = []
            for user in users:
                data.append(user.__serialize__())
            page = request.args.get('page', type=int, default=1)
            startfrom = (page-1)*20
            return jsonify({"items": data[startfrom:startfrom+20], "totalItem":len(data)})
        abort(404, "Data not found")

    @restplus.header("Authorization", 'Bearer', required=True)
    @jwt_required
    @requires_roles("admin")
    @restplus.expect(user_model)
    def post(self):
        data = request.get_json(force=True)
        if data:
            user = Users()
            user.email = data['email']
            user.username = data['username']
            user.password = create_password(data['password'])
            # user.role = UserRole.query.get(data['role'])
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                abort(500, "Save data with error : {}".format(e))
            return jsonify({"success":"Data success saved!!"})
        abort(400, "Bad Request")

@ns.route("/users/<int:id>")
@restplus.response(403, "Forbidden access")
class UserApi(Resource):
    @restplus.header("Authorization", "Bearer", required=True)
    @jwt_required
    @restplus.doc('get_user')
    @requires_roles('admin', 'pegawai')
    def get(self, id):
        user = Users.query.get(id)
        if user:
            return jsonify(user.__serialize__())
        abort(404, "Data not found")

    @restplus.header("Authorization", "Bearer", required=True)
    @jwt_required
    @requires_roles('admin', 'pegawai')
    @restplus.expect(user_model_edit)
    def post(self, id):
        user = Users.query.get(id)
        if user:
            data = request.get_json(force=True)
            if data:
                user.username = data['username']
                user.email = data['email']
                user.active = data['active']
                # user.role = UserRole.query.get(data['role'])
                try:
                    db.session.add(user)
                    db.session.commit()
                except Exception as e:
                    abort(500, "Data save with error : {}".format(e))
                return jsonify({"success":"Data saved success!!"})
            abort(400, "Bad request")
        abort(404, "Data not found")

    @restplus.header("Authorization", "Bearer", required=True)
    @jwt_required
    @requires_roles('admin', 'pegawai')
    @restplus.expect(change_password_model)
    def put(self,id):
        data = request.get_json(force=True)
        if data:
            user = Users.query.get(id)
            if user:
                if user.check_password(data['old_password']):
                    user.password = create_password(data['password'])
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({"success":"Password change with no error"})
                abort(403, "Password lama salah")
            abort(404, "Data not found")
        abort(400, "Bad request")
    @restplus.header("Authorization", "Bearer", required=True)
    @jwt_required
    @requires_roles('admin')
    def delete(self, id):
        user = Users.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"success":"Data success deleted!!"})
        abort(404, "Data not found!!")




# @ns.route("/")


'''
@ns.route("/upload")
@restplus.response(403, "Forbidden")
class ImportCSV(Resource):
    @restplus.expect(upload_parser)
    def post(self):
        upload_file = request.files['file']
        if upload_file and allowed_file(upload_file.filename):
            filename = random_filename()+".csv"
            basedir = os.path.join(app.config['DATA_FOLDER'], filename)
            upload_file.save(basedir)
            with open(basedir, 'r') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(1024))
                reader = csv.DictReader(csv_file)
                reader.dialect = dialect
                filter_column = ["Nomor", ":", "", "1","2","3","4","5","6", "7","8","9","10","11","12","13","14"]
                for row in reader:
                    logging.warning("-----------------------------------------------------")
                    test = [data for data in row.values() if data not in filter_column]
                    logging.warning(test[1])
                    # data_ = [t for t in test[4] if t not in filter_column]
                    # for d in data_:
                    #     logging.warning(d)
                #
                # for row in reader:
                #     test = [line for line in row if line not in filter_column]
                #     logging.warning("------")
                #     for t in test:
                #         logging.warning(t)
            return jsonify({"success":"OK"})
'''
