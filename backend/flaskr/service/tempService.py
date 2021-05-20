from flaskr.model import TempDao
from flaskr import db
from flask import Response, jsonify
from . import save_changes
import time
import json

import os
import glob

#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


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
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        if temp_c > float(tempRange['upper']) or temp_c < float(tempRange['lower']):
            # push 알림보내기
            return '온도 범위 벗어남', 400
            # d = {'temp_c': format(temp_c, '.2f')}
            # return jsonify(d)  # 온도 전송됨

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
            # if True:

            # temp table has not value
            new_temp = TempDao(upper=data['upper'], lower=data['lower'])
            db.session.add(new_temp)
            db.session.commit()

            new_temp = db.session.query(TempDao).first()
            new_temp.upper = data['upper']
            new_temp.lower = data['lower']
            db.session.commit()
            new_temp = TempDao.query.first().as_dict()
            response_object = {
                "status1": "success",
                "message1": "Successfully updated.",
                "result1": new_temp  # new_temp  #new_temp.as_dict()
            }
            return jsonify(response_object)

            # response_object = {
            #   "status1": "success",
            # "message1": "Successfully updated.",
            # "result1": new_temp  # new_temp.as_dict()
            # }
            # return jsonify(response_object)

        else:
            new_temp = db.session.query(TempDao).first()

            if 'upper' in data:
                if str(type(data['upper'])) != "<class 'int'>":
                    return bad_request()
                new_temp.lower = data['lower']
                db.session.commit()

            if 'lower' in data:
                if str(type(data['lower'])) != "<class 'int'>":
                    return bad_request()
                new_temp.upper = data['upper']
                db.session.commit()

            if new_temp.upper < new_temp.lower:
                return bad_request()

            new_temp, tempRange = tempRange, new_temp

            response_object = {
                "status2": "success",
                "message2": "Successfully updated.",
                "result2": tempRange.as_dict()
            }

        return jsonify(response_object), 200

    except Exception as e:
        return {"error": str(e)}, 500


def read_tempRange():
    js = json.dumps(TempDao.query.first().as_dict())
    resp = Response(js, status=200, mimetype='application/json')
    return resp
    # return TempDao.query.first().as_dict()

