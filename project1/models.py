import app 

class Book(app.db.Model):
	_tablename_='books'

	id = app.db.Column(app.db.Integer, primary_key=True)
	name = app.db.Column(app.db.String())
	author = app.db.Column(app.db.String())
	published = app.db.Column(app.db.String())

	def __init__(self, name, author, published):
		self.name=name
		self.author=author
		self.published=published

	def __repr__(self):
		return '<id {}>'.format(self.id)

	def serialize(self):
		return{
			'id': self.id, 
            'name': self.name,
            'author': self.author,
            'published':self.published
		}
