### flaskr/service/productService.py

from flask import jsonify
from flaskr.model import Product
from flaskr import db
from . import save_changes


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


def bad_request():
    response_object = {
        "status": "Bad request",
        "message": "Please enter correct value."
    }
    return jsonify(response_object), 400


def not_found():
    response_object = {
        "status": "Not Found",
        "message": "product dosen\'t exist."
    }
    return jsonify(response_object), 404


def createNewItem(data):
    try:
        item = Product.query.filter_by(product_name=data['product_name']).first()
        if not item:
            if not verifyType(data):
                return bad_request()
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
            return jsonify(response_object), 201
        else:
            response_object = {
                "status": "fail",
                "message": "Product already exists.",
            }
            return jsonify(response_object), 409
    except Exception as e:
        return {"error": str(e)}, 500


def getAllItems():
    rtn = Product.query.all()
    rtn = [x.as_dict() for x in rtn]
    return jsonify(rtn)


def getAItem(id):
    return jsonify(Product.query.filter_by(product_id=id).first().as_dict())


def updateItem(id, data):
    try:
        if not verifyType(data):
            return bad_request()

        if 'product_num' in data and data['product_num'] < 0:
            return bad_request()

        if 'product_id' in data:
            del data['product_id']

        item = Product.query.filter_by(product_id=id).first()

        if not item:
            return not_found()

        Product.query.filter_by(product_id=id).update(data)
        db.session.commit()
        item = Product.query.filter_by(product_id=id).first().as_dict()
        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "result": item
        }
        return jsonify(response_object), 200
    except Exception as e:
        return {"error": str(e)}, 500


def deleteItem(id):
    try:
        item = Product.query.filter_by(product_id=id).first()
        if not item:
            return not_found()
        save_changes(item, 0)
        response_object = {
            "status": "success",
            "message": "Successfully deleted."
        }
        return jsonify(response_object), 204
    except Exception as e:
        return {"error": str(e)}, 500


id_list = []
num_list = []
id_and_num = []


def updateAItem(id, mode):
    if mode == 'ADD':
        id = int(id)
        item = Product.query.get(id)
        if not item:
            return not_found()
        item.product_num += 1

        if id in id_list:
            t = id_list.index(id)
            num_list[t] += 1
            print(id_list, num_list)
        else:
            num = item.product_num
            print('im in')
            id_list.append(id)
            num_list.append(num)
            print(id_list, num_list)

        # db.session.commit()
        item = Product.query.get(id).as_dict()
        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "result": item
        }
        return jsonify(response_object), 200
    elif mode == 'DELETE':
        item = Product.query.get(id)
        if not item:
            return not_found()
        if item.product_num <= 0:
            return 'product is empty'
        item.product_num -= 1

        if id in id_list:
            t = id_list.index(id)
            num_list[t] -= 1
            print(id_list, num_list)
        else:
            num = item.product_num
            print('im in')
            id_list.append(id)
            num_list.append(num)
            print(id_list, num_list)

            # db.session.commit()
        item = Product.query.get(id).as_dict()
        response_object = {
            "status": "success",
            "message": "Successfully updated.",
            "result": item
        }
        return jsonify(response_object), 200

    elif mode == 'END':
        cnt = 0
        for id in id_list:
            item = Product.query.get(id)
            if num_list[cnt] < 0:
                item.product_num = 0
            else:
                item.product_num = num_list[cnt]
                cnt += 1

        db.session.commit()


def save_changes(data, mode):
    if mode == 1:
        db.session.add(data)
    else:
        db.session.delete(data)
    db.session.commit()


