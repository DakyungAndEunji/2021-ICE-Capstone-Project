# service/__init__.py

def save_changes(data):
    db.session.add(data)
    db.session.commit()

__all__ = [
  	'productService',
	'tempService'
]