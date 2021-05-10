from flask import Flask, request, jsonify, Blueprint
from flaskr.service import productService
from . import product_api as api

@api.route('', methods = ['POST'])
def createProduct():
    try:
        item = request.json
        return productService.createNewProduct(item)
    except Exception as e:
        return {"error":str(e)}, 500

@api.route('', methods = ['GET'])
def productList():
    try:
        return productService.getAllProducts()
    except Exception as e:
        return {"error":str(e)}, 500

@api.route('/<int:product_id>', methods = ['GET'])
def getProduct(product_id):
    try:
        return productService.getAProduct(product_id)
    except Exception as e:
        return {"error":str(e)}, 500

@api.route('/<int:product_id>', methods = ['PATCH'])
def updateProduct(product_id):
    try:
        item = request.json
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