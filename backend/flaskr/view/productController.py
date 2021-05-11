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
        return productService.getAllItems()
    except Exception as e:
        return {"error":str(e)}, 500

@bp.route('/<int:product_id>', methods = ['GET'])
def getProduct(product_id):
    try:
        return productService.getAItem(product_id)
    except Exception as e:
        return {"error":str(e)}, 500

@bp.route('/<int:product_id>', methods = ['PATCH'])
def updateProduct(product_id):
    try:
        item = request.json
        return productService.updateItem(product_id, item)
    except Exception as e:
        return {"error":str(e)}

@bp.route('/<int:product_id>', methods = ['DELETE'])
def deleteProduct(product_id):
    try:
        return productService.deleteItem(product_id)
    except Exception as e:
        return {"error":str(e)}