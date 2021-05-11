### flaskr/service/productService.py

from flask import jsonify
from flaskr.model import Product
from flaskr import db

def createNewItem(data):
    try:
        item = Product.query.filter_by(product_name=data['product_name']).first()
        if not item:
            new_item = Product(
                product_name=data['product_name'],
                product_price=data['product_price'],
                product_sales=data['product_sales'],
                product_num=data['product_num']
            )
            save_changes(new_item, 1)
            response_object = {
                "status": "success",
                "message": "Successfully created."
            }
            return response_object, 201
        else:
            response_object = {
                "status": "fail",
                "message": "Product already exists.",
            }
            return response_object, 409
    except Exception as e:
        return { "error":str(e) }, 500

def getAllItems():
    rtn = Product.query.all()
    rtn = [x.as_dict() for x in rtn]
    return jsonify(rtn)

def getAItem(id):
    return Product.query.filter_by(product_id=id).first().as_dict()

def updateItem(id, data):
    try:
        Product.query.filter_by(product_id=id).update(data)
        item = Product.query.filter_by(product_id=id).first().as_dict()
        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "result" : item
        }
        return response_object, 200
    except Exception as e:
        return { "error":str(e) }, 500   

def deleteItem(id):
    try:
        item = Product.query.filter_by(product_id=id).first()
        if not item:
            response_object = {
                "status": "fail",
                "message": "product dosen\'t exist."
            }
            return response_object, 404
        save_changes(item, 0)
        response_object = {
            "status": "success",
            "message": "Successfully deleted."
        }
        return response_object, 204
    except Exception as e:
        return { "error":str(e) }, 500  

def save_changes(data, mode):
    if mode == 1:
        db.session.add(data)
    else:
        db.session.delete(data)
    db.session.commit()