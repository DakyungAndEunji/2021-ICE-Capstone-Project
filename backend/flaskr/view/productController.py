from flask import Flask, request, jsonify, Blueprint
from flaskr.service import productService

bp = Blueprint('main', __name__, url_prefix='/api/product')

@bp.route('', methods = ['POST'])
def createProduct():
    try:
        item = request.json
        return productService.createNewProduct(item)
    except Exception as e:
        return {"error":str(e)}, 500

@bp.route('', methods = ['GET'])
def productList():
    try:
        return productService.getProductList()
    except Exception as e:
        return {"error":str(e)}, 500

@bp.route('/<string:product_name>', methods = ['PATCH'])
def updateProduct():
    try:
#        item=ProductService.createNewProduct(item)
        return jsonify({"message":"OK"}), 200
    except Exception as e:
        return {"error":str(e)}

@bp.route('/<string:product_name>', methods = ['DELETE'])
def deleteProduct():
    try:
#        item=ProductService.createNewProduct(item)
        return jsonify({"message":"OK"}), 200
    except Exception as e:
        return {"error":str(e)}