from flaskr.service import orderService
from flask import request
from . import order_api as api

@api.route('/sale', methods = ['GET'])
def get_order():
    try:
        print('hello')
        start=request.args.get('startDate')
        end=request.args.get('endDate')
        type=request.args.get('type')
        if not start and not end and not type:
            return orderService.getAllOrders()
        elif not start and not end:
            return orderService.getAllTypeOrders(type)
        elif type:
            return orderService.getTypeOrderList(start, end, type)
        return orderService.getOrderList(start, end)
    except Exception as e:
        return {"error":str(e)}, 500

@api.route('/menu', methods = ['GET'])
def get_order_menu():
    try:
        start=request.args.get('startDate')
        end=request.args.get('endDate')
        type=request.args.get('type')
        return orderService.getTypeOrderMenuList(start, end, type)
    except Exception as e:
        return {"error":str(e)}, 500