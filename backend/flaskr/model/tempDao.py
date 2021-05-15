### flaskr/model/tempDao.py

from flaskr import db


class TempDao(db.Model):
    __tablename__ = 'temp'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    upper = db.Column(db.Integer, primary_key=True)
    #upper = db.Column(db.Integer)
    lower = db.Column(db.Integer)

    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower

    def __repr__(self):
        return 'upper : %s, lower : %s' % (self.upper, self.lower)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}




