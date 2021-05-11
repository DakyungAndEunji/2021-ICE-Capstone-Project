from flaskr.model import TempDao
from flaskr import db
from flask import Response
from . import save_changes
import time
import json

# custom 400 error handler
def bad_request():
    return {"status": "Bad request", "message":"Please enter the correct value."}, 400

def read_temp():  # 현재 온도 값 가져오기
    tempRange = TempDao.query.first().as_dict()
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(300)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        if temp_c > float(tempRange['upper']) or temp_c < float(tempRange['lower']):
            # push 알림보내기
            return '온도 범위 벗어남', 400
        d = {'temp_c': temp_c}
        return Response(json.dumps(d), mimetype='application/json')

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

    #else  # flask서버로 온도 값 전송
    #return render_template('post.html')

def update_tempRange(data):
    # 사용자가 입력한 온도 범위를 서버로 받아오는 것
    # DB에 값 저장
    #초기값이 없으면 가져와야지
    try:
        if not data:
            return bad_request()
        tempRange = TempDao.query.first()
        if not tempRange:
            new_temp = TempDao(upper=up, lower=low)
            save_changes(new_temp)
        else:
            new_temp = TempDao(tempRange.upper, tempRange.lower)
            if 'upper' in data:
                if str(type(data['upper']))!="<class 'int'>":
                    return bad_request()
                new_temp.upper=data['upper']
            if 'lower' in data:
                if str(type(data['lower']))!="<class 'int'>":
                    return bad_request()
                new_temp.lower=data['lower']

            if new_temp.upper<new_temp.lower:
                return bad_request()
            
            new_temp, tempRange = tempRange, new_temp
            response_object = {
                "status": "success",
                "message": "Successfully updated.",
                "result" : tempRange.as_dict()
            }
        return response_object, 200
        #db에 저장된 온도 값 가져오기
    except Exception as e:
        return { "error": str(e) }, 500

    #u = request.args.get("upper")
    #l = request.args.get("lower")
    #데이터베이스.patch('/tempdb', {'upper': u, 'lower': l})
    #return '', 204

def read_tempRange():
    return TempDao.query.first().as_dict()