import functions 

class User(object):
	"""MongoDB-Backed User"""
	def __init__(self, username):
		self.username = username
		
		