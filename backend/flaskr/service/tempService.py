from backend.flaskr.model.tempDao import TempDao
from backend.flaskr.model.tempDao import TempDao
import time
from flask import Response
import json

class ReadTemp:
    def __init__(self, temp_dao, config):
        self.temp_dao = temp_dao
        self.config = config
        self.row = self.temp_dao.get_db_temp()

    def read_temp(self):  # 현재 온도 값 가져오기
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(300)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            if temp_c > self.row[0] or temp_c < self.row[1]:
                # push 알림보내기
                return '온도 범위 벗어남', 400
            d = {'temp_c': temp_c}
            return Response(json.dumps(d), mimetype='application/json')

    def read_temp_raw(self):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

        #else  # flask서버로 온도 값 전송
        #return render_template('post.html')

class GetTemp:
    def __init__(self, temp_Dao, config):
        self.temp_Dao = temp_Dao
        self.config = config

    def get_temp(self, up, low):
        # 사용자가 입력한 온도 범위를 서버로 받아오는 것
        # DB에 값 저장
        #초기값이 없으면 가져와야지
        try:
            row = self.temp_Dao.get_db_temp()
            if row == -1: return {'message': 'no content, enter the range of the temperature'}, 412
            elif up == row[0] and low == row[1]:
                return {'message': 'no change'}, 200
            elif up == row[0] and low != row[1]:
                self.temp_Dao.insert_temp(row[0], low)
            elif up != row[0] and low == row[1]:
                self.temp_Dao.insert_temp(up, row[1])
            else:
                self.temp_Dao.insert_temp(up, low)
            #db에 저장된 온도 값 가져오기
        except Exception as e:
            return {
                       "error": str(e)
                   }, 500

        #u = request.args.get("upper")
        #l = request.args.get("lower")
        #데이터베이스.patch('/tempdb', {'upper': u, 'lower': l})
        #return '', 204


