### flaskr/model/orderDao.py

from flaskr import db
import json

class Order(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_type = db.Column(db.Boolean, nullable=False)
    order_time = db.Column(db.TIMESTAMP, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    order_num = db.Column(db.Integer, nullable=False)

    def __init__(self, order_type, order_time, product_id, order_num):
        self.order_type = order_type
        self.order_time = order_time
        self.product_id = product_id
        self.order_num = order_num

    def __repr__(self):
        return '{order_id : %s, order_type : %s, order_time : %s, product_id : %s, order_num : %s}' % (self.order_id, self.order_type, self.order_time, self.product_id, self.order_num)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}