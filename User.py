import functions 

class User(object):
	"""MongoDB-Backed User"""
	def __init__(self, username):
		self.username = username
		self.obj = functions.users.find_one({"username": username})
		
	def is_valid(self):
		return self.obj != None

	def get(self,attr):
		try:
			return self.obj[attr]
		except KeyError:
			return None

	def check_pass(self,passwd):
		return functions.hash_password(passwd) == self.obj["password"]	