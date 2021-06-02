from flaskr.model import TempDao
from flask import Response
from .response import *
from .db import *
import json
import time

import os
import glob

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

# custom 400 error handler
def bad_request():
    return {"status": "Bad request", "message": "Please enter the correct value."}, 400


def read_temp():  # 현재 온도 값 가져오기
    tempRange = TempDao.query.first().as_dict()
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        time.sleep(180)
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        if temp_c > float(tempRange['upper']) or temp_c < float(tempRange['lower']):
            # push 알림보내기
            return '온도 범위 벗어남', 400

        d = {'temp_c': format(temp_c, '.2f')}
        return jsonify(d)


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def update_tempRange(data):
    try:
        if not data:
            return bad_request()

        tempRange = TempDao.query.first()

        if not tempRange:
            new_temp = TempDao(upper=data['upper'], lower=data['lower'])
            add_commit(new_temp)
            new_temp = TempDao.query.first().as_dict()
            return created()

        else:  # same range(upper or lower or both)
            new_temp = db.session.query(TempDao).first()
            
            if 'upper' in data: # 데이터 동일해도 무조건 upper로 들어오는다..ㅎㅋㅎ하지만 잘 반영되므로 무시하도록 하자
                if not is_float(data['upper']):
                    return bad_request()
                new_temp.upper = float(data['upper'])
            if 'lower' in data:
                if not is_float(data['lower']):
                    return bad_request()
                new_temp.lower = float(data['lower'])

            if new_temp.upper < new_temp.lower:
                return bad_request()

            new_temp, tempRange = tempRange, new_temp
            commit()

        return ok(tempRange.as_dict(), "Successfully updated.")

    except Exception as e:
        return {"error": str(e)}, 500


def read_tempRange():
    js = json.dumps(TempDao.query.first().as_dict())
    resp = Response(js, status=200, mimetype='application/json')
    return resp