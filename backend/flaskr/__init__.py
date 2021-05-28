### flaskr/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.view import product_api, temp_api, order_api

db = SQLAlchemy()

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:toor!@localhost:3306/tps?charset=utf8'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:colferpi@localhost:3306/temp?charset=utf8'  # 이건 경이거^^
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.secret_key = 'manyrandombyte'

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    from flaskr.service import productService
    from flaskr.view import productController, tempView, orderController

    app.register_blueprint(product_api, url_prefix='/api/product')
    app.register_blueprint(temp_api, url_prefix='/api/temp')
    app.register_blueprint(order_api, url_prefix='/api/order')

    @app.route('/stock/<int:product_id>/<string:method>')
    def passing_product(product_id, method):
        return productService.updateAItem(product_id, method)

    return app