import functions
from var import *
from bson.objectid import ObjectId

class User(object):
	"""MongoDB-Backed User"""
	def __init__(self, username, userid=None):
		self.alt = None
		if userid:
			self.obj = functions.users.find_one({"_id": ObjectId(userid)})
			self.username = self.obj["username"]
		else:
			self.username = username
			self.obj = functions.users.find_one({"username": username})
			if self.obj == None:
				self.obj = functions.users.find_one({"emails":{"$in":[username]}})
				if self.obj != None:
					self.alt = username
					self.username = self.obj["username"]
		
	def is_valid(self):
		return self.obj != None

	def get(self,attr):
		if attr == 'mailing':
			return self.alt if self.alt else self.username
		try:
			return self.obj[attr]
		except KeyError:
			return None

	def check_pass(self,passwd):
		return self.check_pass_hash(functions.hash_password(passwd))	

	def check_pass_hash(self,passwd):
		return passwd == self.obj["password"]	

	def add_email(self,email):
		if functions.users.find({"emails":{"$in":[email]}}).count() == 0:
			return functions.users.update({"username": self.username}, {'$push': {'emails': email}}, True)

	def get_letters(self):
		return letters.find({"job.from_address.email": self.get("username")})

	def get_postcards(self):
		return postcards.find({"job.from_address.email": self.get("username")})