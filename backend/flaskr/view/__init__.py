# service/__init__.py
from flask import Blueprint

product_api = Blueprint('product_api', __name__)
temp_api = Blueprint('temp_api', __name__)

__all__ = [
  	'productController',
	'tempView'
]