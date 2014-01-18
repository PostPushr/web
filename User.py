import functions
from bson.objectid import ObjectId

class User(object):
	"""MongoDB-Backed User"""
	def __init__(self, username, userid=None):
		self.username = username
		if userid:
			self.obj = functions.users.find_one({"_id": ObjectId(userid)})
		else:
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