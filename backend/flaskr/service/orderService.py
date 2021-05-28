from flask import jsonify
from flaskr.model import Order, Product
from .db import *
from .response import *
import datetime as pydatetime
from pytz import timezone

KST = pydatetime.timezone(pydatetime.timedelta(hours=9))

def get_now():
    return pydatetime.datetime.now(pydatetime.timezone.utc)

def get_now_timestamp():
    return get_now().timestamp()

def strToDatetime(date):
    rtn = pydatetime.datetime.strptime(date, "%Y-%m-%d")
    return rtn
    #return rtn

def strToEndDatetime(date):
    rtn = strToDatetime(date).replace(hour=23, minute=59, second=59, microsecond=999999)
    return rtn
    #return rtn

def strToBoolean(str):
    if str=='true':
        return True
    elif str=='false':
        return False
    return None

def createNewOrder(item, data):
    try:
        # 출고, 0
        if item.product_num < data['product_num']:
            orderType = False
        # 입고, 1
        elif item.product_num > data['product_num']:
            orderType = True
        new_item = Order(
            order_type = orderType,
            order_time = get_now(),
            product_id = item.product_id,
            order_num = abs(item.product_num-data['product_num'])
        )
        add_commit(new_item)
    except Exception as e:
        return {"error":str(e)}, 500

def getTypeOrderList(start, end, type):
    try:
        type = strToBoolean(type)
        if not start or not end or type is None:
            return bad_request("Please enter correct value.")
        start = strToDatetime(start)
        end = strToEndDatetime(end)
        rtn = Order.query.filter(Order.order_time.between(start, end), Order.order_type==type)
        rtn = [x.as_dict() for x in rtn]
        for item in rtn:
            item['order_time']=item['order_time'].astimezone(KST)
            pItem = Product.query.get(item['product_id'])
            item['order_price']=pItem.product_price * item['order_num']
            item['order_sales']=pItem.product_sales * item['order_num']
            item['product_name']=pItem.product_name
        return jsonify(rtn)
    except Exception as e:
        return {"error":str(e)}, 500

def getOrderList(start, end):
    try:
        start = strToDatetime(start) - pydatetime.timedelta(hours=9)
        end = strToEndDatetime(end) - pydatetime.timedelta(hours=9)
        data = Order.query.filter(Order.order_time.between(start, end))
        data = [x.as_dict() for x in data]
        rtn = {
            "data" : data,
            "totalSales" : 0,
            "totalIncome" : 0
        }
        totalSales = 0
        totalIncome = 0
        for item in data:
            pItem = Product.query.get(item['product_id'])
            item['order_price']=pItem.product_price * item['order_num']
            item['order_sales']=pItem.product_sales * item['order_num']
            item['product_name']=pItem.product_name
            totalSales += pItem.product_sales
            totalIncome += pItem.product_price
        rtn["totalSales"]=totalSales
        rtn["totalIncome"]=totalSales-totalIncome
        return jsonify(rtn)
    except Exception as e:
        return {"error":str(e)}, 500

def getAllOrders():
    try:
        rtn = Order.query.all()
        rtn = [x.as_dict() for x in rtn]
        return jsonify(rtn)
    except Exception as e:
        return {"error":str(e)}, 500

def getAllTypeOrders(type):
    try:
        type = strToBoolean(type)
        if type is None:
            return bad_request("Please enter correct value.")
        rtn = Order.query.filter_by(order_type=type).all()
        rtn = [x.as_dict() for x in rtn]
        return jsonify(rtn)
    except Exception as e:
        return {"error":str(e)}, 500

def getTypeOrderMenuList(start, end, type):
    try:
        type = strToBoolean(type)
        if not start or not end or type is None:
            return bad_request("Please enter correct value.")
        start = strToDatetime(start)
        end = strToEndDatetime(end)
        orderList = Order.query.filter(Order.order_time.between(start, end), Order.order_type==type)
        orderList = [x.as_dict() for x in orderList]
        rtn = []
        for item in orderList:
            pItem = Product.query.get(item['product_id'])
            idx = next((idx for (idx,it) in enumerate(rtn) if it['product_id']==pItem.product_id), None)
            if idx != None:
                rtn[idx]['order_price']+=pItem.product_price * item['order_num']
                rtn[idx]['order_sales']+=pItem.product_sales * item['order_num']
            else:
                rtn.append({
                    "product_id":pItem.product_id,
                    "product_name":pItem.product_name,
                    "order_price":pItem.product_price * item['order_num'],
                    "order_sales":pItem.product_sales * item['order_num']
                })
        return jsonify(rtn)
    except Exception as e:
        return {"error":str(e)}, 500