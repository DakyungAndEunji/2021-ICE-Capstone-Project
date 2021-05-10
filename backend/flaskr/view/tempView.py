from flask import jsonify
from api.model.tempDao import TempDao
from api.service.tempService import *

#view는 service에 의존적이기 때문에 아래 코드에서 create_endpoint 인자 중 app은 app.py에서 정의한
#Flask객체app = Flask(__name__)이고, services는 service의 user_serive에서 받을 로직 부분이다.
#(변수가 services.user_service인 이유는 app.py에서 Service 객체의 이름을 정의해주었기 때문이다)


def create_endpoints(app, services):
    read_temp_service = services.read_temp_service
    get_temp_service = services.get_temp_service

    @app.route('/temp', methods=['GET'])
    def read_temp():
        try:
            return 'hello !!!!!'
            #return read_temp_service.read_temp()
        except Exception as e:
            return {'error': str(e)}, 500

    @app.route('/range', methods=['PATCH'])
    def tempPatch():
        try:
            range = get_temp_service.get_temp()
            return jsonify({"message": "OK"}), 200
        except Exception as e:
            return {"error": str(e)}