### flaskr/model/productDao.py

from flaskr import db
import json

class Product(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(30), unique=True, nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_sales = db.Column(db.Integer, nullable=False)
    product_num = db.Column(db.Integer, nullable=False)

    def __init__(self, product_name, product_price, product_sales, product_num):
        self.product_name = product_name
        self.product_price = product_price
        self.product_sales = product_sales
        self.product_num = product_num

    def __repr__(self):
        return '{product_id : %s, product_name : %s, product_price : %s, product_sales : %s, product_num : %s}' % (self.product_id, self.product_name, self.product_price, self.product_sales, self.product_num)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}