### flaskr/service/productService.py

from flask import jsonify
from flaskr.model import Product
from . import orderService
from .db import *
from .response import *


def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def verifyType(data):
    for idx, val in data.items():
        if idx == 'product_name':
            continue
        if not is_integer(val):
            return False
        data[idx] = int(val)
    return True

def createNewItem(data):
    try:
        item = Product.query.filter_by(product_name=data['product_name']).first()
        if not item:
            if not verifyType(data):
                return bad_request("Please enter correct value.")
            new_item = Product(
                product_name=data['product_name'],
                product_price=data['product_price'],
                product_sales=data['product_sales'],
                product_num=data['product_num']
            )

            add_commit(new_item)

            if data['product_num']>0:
                data['product_num'] *= 2
                orderService.createNewOrder(new_item, data)
                commit()

            return created()
        else:
            return conflict("Product already exists.")
    except Exception as e:
        return {"error": str(e)}, 500


def getAllItems():
    rtn = Product.query.all()
    rtn = [x.as_dict() for x in rtn]
    return jsonify(rtn)


def getAItem(id):
    return jsonify(Product.query.get(id).as_dict())


def updateItem(id, data):
    try:
        if not verifyType(data):
            return bad_request("Please enter correct value.")

        if 'product_num' in data and data['product_num'] < 0:
            return bad_request("Please enter correct value.")       

        if 'product_id' in data:
            del data['product_id']

        item = Product.query.get(id)
        if not item:
            return not_found("product dosen\'t exist.")          

        orderService.createNewOrder(item, data)

        Product.query.filter_by(product_id=id).update(data)
        commit()
        item = Product.query.get(id).as_dict()
        return ok(item, "Successfully updated.")
    except Exception as e:
        return {"error": str(e)}, 500


def deleteItem(id):
    try:
        item = Product.query.get(id)
        if not item:
            return not_found("product dosen\'t exist.")
        delete_commit()
        return ok(None, "Successfully deleted.")
    except Exception as e:
        return {"error": str(e)}, 500


def updateAItem(id, mode):
    if mode == 'ADD':
        id = int(id)
        item = Product.query.get(id)
        if not item:
            return not_found("product dosen\'t exist.")
        item.product_num += 1
        commit()
        item = Product.query.get(id).as_dict()
        return ok(item, "Successfully updated.")
    elif mode == 'DELETE':
        item = Product.query.get(id)
        if not item:
            return not_found("product dosen\'t exist.")
        if item.product_num <= 0:
            return 'product is empty'
        item.product_num -= 1
        commit()
        item = Product.query.get(id).as_dict()
        return ok(item, "Successfully updated.")
