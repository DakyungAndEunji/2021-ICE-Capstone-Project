# service/__init__.py
from flask import Blueprint

product_api = Blueprint('product_api', __name__)
order_api = Blueprint('order_api', __name__)
temp_api = Blueprint('temp_api', __name__)
setting_api = Blueprint('setting_api', __name__)

__all__ = [
  	'productController',
	'orderController',
	'tempView'
	'settingcontroller'
]