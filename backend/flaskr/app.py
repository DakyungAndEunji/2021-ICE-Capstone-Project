import os
import glob
import time
import pymysql
from flask import Flask, render_template, request, jsonify, json, Response
from api.model.tempDao import TempDao
from api.service.tempService import ReadTemp, GetTemp
from api.view.tempView import create_endpoints

from sqlalchemy import create_engine, text
#from jsonpatch import JsonPatch, JsonPatchException
#from dictalchemy import make_class_dictable
#from flask_sqlalchemy import SQLAlchemy

class Services:
    pass

def create_app(test_config = None):
    app = Flask(__name__)
    app.debug = True

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    temp_database = pymysql.connect(host='localhost',
                               user='root',
                               password='colferpi',
                               db='temp',
                               charset='utf8'
                               )
    cursor = temp_database.cursor()
    cursor.execute("show tables")

    # temp_dao = TempDao(temp_database)
    #
    # services = Services
    # services.read_temp_service = ReadTemp(temp_dao, app.config)
    # services.get_temp_service = GetTemp(temp_dao, app.config)
    #
    # create_endpoints(app, services)


    #database = create_engine(app.config['DB_URL'], encoding = 'utf-8', maxoverflow=0)
    #app.database = database

    return app

#app = Flask(__name__)
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

#base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28*')[0]
#device_file = device_folder + '/w1_slave'


#if __name__ == '__main__':
#    app.run()