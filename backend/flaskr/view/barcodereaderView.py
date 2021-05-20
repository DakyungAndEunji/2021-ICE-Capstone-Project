from flask import Flask, request, jsonify, Blueprint
from flaskr.service import barcodereaderService
from flaskr.service import productService
from . import product_api as api

@api.route('', methods = ['POST'])
def createProduct():
    try:
        qrcode = barcodereaderService.barcode() #큐알코드에 json 데이터 입력했다면
        item = jsonify(qrcode)
        return productService.createNewProduct(item)
    except Exception as e:
        return {"error":str(e)}, 500


@api.route('/<int:product_id>', methods = ['PATCH'])
def updateProduct(product_id):
    try:
        qrcode = barcodereaderService.barcode()
        item = jsonify(qrcode)
        return productService.updateProduct(product_id, item)
    except Exception as e:
        return {"error":str(e)}

@api.route('/<int:product_id>', methods = ['DELETE'])
def deleteProduct(product_id):
    try:
#        item=ProductService.createNewProduct(item)
        return jsonify({"message":"OK"}), 200
    except Exception as e:
        return {"error":str(e)}