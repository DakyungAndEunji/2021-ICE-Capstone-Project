from flaskr.model import TempDao
from flaskr import db
from flask import Response, jsonify
from . import save_changes
import time
import json

from sqlalchemy.orm import scoped_session, sessionmaker

import os
import glob

# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# base_dir = '/sys/bus/w1/devices/'
# device_folder = glob.glob(base_dir + '28*')[0]
# device_file = device_folder + '/w1_slave'


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
            # return '온도 범위 벗어남', 400
            d = {'temp_c': temp_c}
            return jsonify(d)  # 온도 전송됨

        d = {'temp_c': temp_c}
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
        #tempRange = TempDao.query.first()

        #tempRange = json.dumps(TempDao.query.first().as_dict())
        #resp = Response(tempRange, status=200, mimetype='application/json')
        #return(resp) # present temp range in temp db

        tempRange = TempDao.query.first()

        if not tempRange:
        #if True:
            # new_temp = {'upper': data['upper'], 'lower': data['lower']}

            # print(dict(new_temp)) #ok {'upper': 50, 'lower': 24}
            # new_range = TempDao(upper=data['upper'], lower=data['lower'])
            # db.session.update(new_range)
            # db.session.commit()
            # js = json.dumps(TempDao.query.first().as_dict())
            # return js

            #new_range = db.session.query(TempDao).first()
            #new_range.upper = data['upper']
            #new_range.lower = data['lower']
            #db.session.commit() #"error": "(pymysql.err.IntegrityError) (1062, \"Duplicate entry '36' for key 'PRIMARY'\")

            #new_temp = TempDao.query.first()
            #new_temp.upper = data['upper']
            #new_temp.lower = data['lower']
            #TempDao.query.update(new_temp)
            #db.session.commit()

            new_temp = TempDao(upper=data['upper'], lower=data['lower'])
            db.session.add([new_temp])
            db.session.commit()


            new_temp = TempDao.query.first().as_dict()

            #new_range = TempDao(upper=data['upper'], lower=data['lower'])
            #db.session.add([new_range])
            #db.session.commit()


            #row = db.session.query(TempDao).first()
            #row.upper = data['upper']
            #row.lower = data['lower']
            #db.session.add([row])
            #db.session.commit()

            #print(type(data['upper'])) #<class 'int'>

            #new_range = TempDao(upper=data['upper'], lower=data['lower'])
            #db.session.add([new_range])
            #db.session.commit()

            # print(new_range.as_dict()) #ok {'upper': 50, 'lower': 24}

            # print(json.dumps(new_range.upper)) # ok 50

            # return json.dumps(new_range.as_dict()) # ok {"upper": 50, "lower": 24}

            # db.session.add(new_range.as_dict())
            # db.session.commit()

            # entries = []
            # for i in data:
            #    new_range = TempDao(upper=data['upper'], lower=data['lower'])
            #    entries.append(new_range)
            #    print(entries) #print ok
            # return jsonify(new_temp)

            # new_range = TempDao(upper=data['upper'], lower=data['lower'])
            # print(new_range.upper, new_range.lower) #ok

            # new_range = json.dumps(TempDao(data['upper'], data['lower']).query.update().as_dict())
            # resp = Response(new_range, status=200, mimetype='application/json')
            # print(new_range)

            # new_range = TempDao.query.first()
            # new_range.upper = str(data['upper'])
            # new_range.lower = str(data['lower'])
            # db.session.flush()
            # db.session.commit()

            # db.session.add(new_range)
            # new_temp = TempDao(upper=data['upper'], lower=data['lower'])
            # db.session.add(json.dumps(entries))
            # db.session.commit()
            # TempDao.db.session.add(temp)
            # TempDao.db.session.commit()

            # save_changes(new_temp)

            response_object = {
                "status1": "success",
                "message1": "Successfully updated.",
                "result1": new_temp  # new_temp.as_dict()
                }
            return jsonify(response_object)

        else:  # same range(upper or lower or both)

            #tempRange = json.dumps(TempDao.query.first().as_dict())

            new_temp = db.session.query(TempDao).first()

            # new_temp = TempDao(tempRange.upper, tempRange.lower)
            if 'upper' in data:
                if str(type(data['upper'])) != "<class 'int'>":
                    return bad_request()
                new_temp.lower = data['lower']
                db.session.commit()
                # new_temp.lower = data['lower']
                # new_temp.upper=data['upper']
                # TempDao.db.session.commit()

            if 'lower' in data:
                if str(type(data['lower'])) != "<class 'int'>":
                    return bad_request()
                new_temp.upper = data['upper']
                db.session.commit()
                #new_temp.upper = data['upper']
                # new_temp.lower=data['lower']
                # db.session.commit()

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
