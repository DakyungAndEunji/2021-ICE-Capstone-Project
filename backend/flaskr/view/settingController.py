from flaskr.service import pushService
from flask import request
from . import setting_api as api

@api.route('/token', methods = ['PUT'])
def tokenChange():
    try:
        item = request.json
        pushService.TOKEN=item
    except Exception as e:
        return {"error":str(e)}