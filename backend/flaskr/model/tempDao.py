### flaskr/model/tempDao.py

from flaskr import db
#from raspi_db import db

class TempDao(db.Model):
    __tablename__ = 'temp'
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    upper = db.Column(db.Integer, primary_key=True)
    lower = db.Column(db.Integer)

    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower

    def __repr__(self):
        return 'upper : %s, lower : %s' % (self.upper, self.lower)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns}

# class TempDao:
#     def __init__(self, database):
#         self.db = database
#     def get_db_temp(self):
#         cursor = self.db.cursor()
#         row = cursor.execute(text("""
#             SELECT upper, lower
#             FROM temp           
#         """), {'upper': self.upper, 'lower': self.lower}).fetchall() #fetchclone이 모냐
#         #execute메소드는 ResultProxy 객체를 리턴하는데 ResultProxy의 fetchall메소드를 사용해 실제 데이터들을 리스트의 형태로 리턴
#         for i in row: # 리스트형식으로 잘 반환되는지 확인
#             print(row[i])
#         return row
#     def insert_temp(self, upper, lower):
#         cursor = self.db.cursor()
#         sql= """
#                 insert into temp~~~~(
#                 upper_temp) values(%s)
#                 (lower_temp) values(%s)
#             """
#         cursor.execute(sql, ())
#         self.db.commit()
#         self.db.close()



    ##for row in rows:
#    print(f"upper: {row['upper']}")
#    print(f"lower: {row['lower']}")v
