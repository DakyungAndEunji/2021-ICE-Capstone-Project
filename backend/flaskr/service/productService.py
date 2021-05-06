### flaskr/service/productService.py

from flaskr.model import Product
from flaskr import db

def createNewProduct(data):
    try:
        item = Product.query.filter_by(product_name=data['product_name']).first()
        if not item:
            new_item = Product(
                product_name=data['product_name'],
                product_price=data['product_price'],
                product_sales=data['product_sales'],
                product_num=data['product_num']
            )
            save_changes(new_item)
            response_object = {
                'status': 'success',
                'message': 'Successfully created.'
            }
            return response_object, 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Product already exists.',
            }
            return response_object, 409
    except Exception as e:
        return {
            "error":str(e)
            }, 500

def getProductList():
    return Product.query.all()

def save_changes(data):
    db.session.add(data)
    db.session.commit()