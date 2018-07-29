from flask_restplus import Api
from flask import jsonify
restplus = Api(version='1.0', title='Pasien APP API',
    description='List of Pasien app data api')
ns = restplus.namespace("v0.1", description="Restful api pasien app")

def make_response(status_code, message, error, data):
    response = jsonify({
        'status': status_code,
        'message': message,
        'error': error,
        'data' : data
    })
    response.status_code = status_code
    return response