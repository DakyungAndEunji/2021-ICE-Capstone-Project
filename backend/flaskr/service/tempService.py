from flaskr.model import TempDao
from flask import Response, jsonify
from .response import *
from .db import *
import time
import json

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
    try:
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            d = {'temp_c': format(temp_c, '.2f')}
            return jsonify(d)

    except Exception as e:
        return {"error": str(e)}, 500            


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
            new_temp = TempDao(tempRange.upper, tempRange.lower)

            if 'upper' in data:
                if not is_float(data['upper']):
                    return bad_request()
                new_temp.upper = float(data['upper'])
            if 'lower' in data:
                if not is_float(data['lower']):
                    return bad_request()
                new_temp.lower = float(data['lower'])
            if new_temp.upper < new_temp.lower:
                return bad_request()
            
            tempRange.lower=new_temp.lower
            tempRange.upper=new_temp.upper
            commit()
        return ok(tempRange.as_dict(), "Successfully updated.")

    except Exception as e:
        return {"error": str(e)}, 500


def read_tempRange():
    js = json.dumps(TempDao.query.first().as_dict())
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    # return TempDao.query.first().as_dict()

