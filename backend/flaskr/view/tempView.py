from flask import jsonify, request
from flaskr.service import tempService
from . import temp_api as api

@api.route('', methods=['GET'])
def read_temp():
    try:
        #return 'hello !!!!!'
        return tempService.read_temp()
    except Exception as e:
        return {'error': str(e)}, 500

@api.route('/range', methods=['GET'])
def read_tempRange():
    try:
        return tempService.read_tempRange()
    except Exception as e:
        return {'error': str(e)}, 500

@api.route('/range', methods=['PATCH'])
def tempPatch():
    try:
        range = request.json
        return tempService.update_tempRange(range)
    except Exception as e:
        return {"error": str(e)}