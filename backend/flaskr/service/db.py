from flaskr import db

def commit():
	db.session.commit()

def add_commit(data):
	db.session.add(data)
	commit()

def delete_commit(data):
	db.session.delete(data)
	commit()