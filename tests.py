import functions,os

def run_simple():
	import hashlib
	import functions
	import datetime

	body = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
	user = "yasyf"
	message = {"to": {"prefix": "Dear", "name": "Test User"}, "_from": {"prefix": "Sincerely,", "name": "Yasyf Mohamedali"}, "body": body}

	to_address = functions.lob.Address.create(name=message["to"]["name"], address_line1='104 Printing Boulevard', address_city='Boston', address_state='MA', address_country='US', address_zip='12345')
	from_address = functions.lob.Address.create(name=message["_from"]["name"], address_line1='1251 Pintail Drive', address_city='Qualicum Beach', address_state='BC', address_country='CA', address_zip='V9K 1C7')

	message["to"]["address"] = functions.format_address(to_address)
	message["_from"]["address"] = functions.format_address(from_address)

	obj_loc = functions.save(functions.render_text(message), hashlib.md5(user).hexdigest())

	return "http://"+os.environ['domain']+"/"+obj_loc


def run_advanced():
	import hashlib
	import functions
	import datetime

	body = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
	user = "yasyf"
	message = {"to": {"prefix": "Dear", "name": "Test User"}, "_from": {"prefix": "Sincerely,", "name": "Yasyf Mohamedali"}, "body": body}

	to_address = functions.lob.Address.create(name=message["to"]["name"], address_line1='104 Printing Boulevard', address_city='Boston', address_state='MA', address_country='US', address_zip='12345')
	from_address = functions.lob.Address.create(name=message["_from"]["name"], address_line1='1251 Pintail Drive', address_city='Qualicum Beach', address_state='BC', address_country='CA', address_zip='V9K 1C7')

	message["to"]["address"] = functions.format_address(to_address)
	message["_from"]["address"] = functions.format_address(from_address)

	obj_loc = functions.save(functions.render_text(message), hashlib.md5(user).hexdigest())

	_object = functions.lob.Object.create(name=hashlib.md5(user+str(datetime.datetime.now())).hexdigest(), file="http://"+os.environ['domain']+"/"+obj_loc, setting_id='100', quantity=1)
	return functions.lob.Job.create(name=hashlib.md5(user+str(datetime.datetime.now())).hexdigest(), to=to_address.id, objects=_object.id, from_address=from_address.id, packaging_id='1').to_dict()