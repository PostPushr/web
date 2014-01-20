from jinja2 import Template, Environment, FileSystemLoader
from werkzeug import secure_filename
import requests, hashlib, os, subprocess, json, time, codecs
import lob, pymongo, stripe, datetime, re, boto
from pygeocoder import Geocoder, GeocoderError
from tasks import wkhtmltopdf_letters, s3_upload, wkhtmltopdf_postcards
from flask import g
from var import *
from emails import *


def launch_celery():
	if os.environ.get('dev') == "True":
		p = subprocess.Popen("celery worker -q -A tasks &", shell=True, close_fds=True)
	else:
		p = subprocess.Popen("celery worker -q -A tasks > /dev/null 2>&1 &", shell=True, close_fds=True)
	p.wait()

def create_stripe_cust(token,email):
	try:
		customer = stripe.Customer.create(card=token,description="PostPushr: "+email)
		return customer.id
	except Exception:
		return None
	
def jsuccess():
	return json.dumps({"status": "success"})

def jsuccess_with_txid(txid):
	return json.dumps({"status": "success", "txid": txid})

def jfail(reason):
	return json.dumps({"status": "error","error": reason})

def jfail_address(address):
	try:
		if g.over_api:
			return json.dumps({"status": "error","error": "over geocoding query limit"})
	except Exception:
		pass
	return json.dumps({"status": "error","error": "invalid address " + address})

def save_letter(html, user, to_address, to_address_coded, from_address):
	_hash = hashlib.md5(user.get("username")+str(datetime.datetime.now())).hexdigest()
	d = "static/gen/{0}/".format(_hash)
	pdf_file_name = d+"{0}.pdf".format(_hash)
	html_file_name = d+"{0}.html".format(_hash)
	if not os.path.exists(d):
		os.makedirs(d)
	html_file = codecs.open(html_file_name, "w+b", "utf-8-sig")
	html_file.write(html)
	cmd = "{0}/wkhtmltopdf --encoding utf8 -s Letter {1} {2}".format(bin_dir,html_file_name,pdf_file_name)
	wkhtmltopdf_letters.delay(cmd, user, _hash, to_address, to_address_coded, from_address)
	return pdf_file_name

def save_postcard(_hash, image, message, user, to_address, from_address):
	env = Environment(loader=FileSystemLoader('templates'))
	template = env.get_template('postcard.html')
	tasks.wkhtmltopdf_postcards.delay(_hash, image, message, user, to_address, from_address, template)

def render_text(message):
	env = Environment(loader=FileSystemLoader('templates'))
	template = env.get_template('pdf.html')
	generated_html = template.render(message=message)
	return generated_html


def render_html(html):
	return html

def render_url(url):
	html = requests.get(url).text
	return html

def remove_addresses():
	for a in lob.Address.list():
		lob.Address.delete(id=a.id)

def create_user(username, hashed_password, **kwargs):
	#Expect: Username, Password, Name, Token, Snapchat, Address, ...
	kwargs["username"] = username
	kwargs["password"] = hashed_password
	users.insert(kwargs)
	return str(users.find_one({"username": username})["_id"])

def sha1(text):
	m = hashlib.sha1()
	m.update(text)
	return m.hexdigest()

def hash_password(password):
	return sha1(sha1(password)+sha1(os.environ["salt"]))

def create_address_from_geocode(name, address_coded, email=None):
	return lob.Address.create(name=name, address_line1=address_coded.street_number+" "+address_coded.route, address_city=address_coded.city, address_state=address_coded.state__short_name, address_country=address_coded.country__short_name, address_zip=address_coded.postal_code, email=email)

def ucfirst(txt):
	return ' '.join([x[:1].upper()+x[1:].lower() for x in txt.split(' ')])

def gcode_serialize(address_coded):
	c = {}
	c["valid_address"] = address_coded.valid_address
	c["street_number"] = address_coded.street_number
	c["route"] = address_coded.route
	c["city"] = address_coded.city
	c["state__short_name"] = address_coded.state__short_name
	c["country__short_name"] = address_coded.country__short_name
	c["postal_code"] = address_coded.postal_code
	return c

def gcode(address):
	coded = gcode_cache.find_one({'a': address})
	if coded:
		return coded["b"]
	try:
		coded = Geocoder.geocode(address)
		gcode_cache.insert({'a': address, 'b': gcode_serialize(coded)})
		return coded
	except GeocoderError, e:
		if str(e) == "OVER_QUERY_LIMIT":
			g.over_api = True
		return None

def send_letter(user,to_name,to_address,body):
	to_address_coded = gcode(to_address)
	if to_address_coded == None:
		return_unknown_address(user,to_address)
		return

	if to_address_coded.valid_address:

		to_name = to_name.replace("_"," ").replace('"','')
		to_name = re.sub("@\w+."+os.environ["domain"],"",to_name)
		to_name = ucfirst(to_name)

		message = {"to": {"prefix": "", "name": to_name}, "_from": {"prefix": "", "name": user.get("name")}, "body": body}

		to_address = create_address_from_geocode(message["to"]["name"], to_address_coded)
		from_address_coded = gcode(user.get('address'))
		if from_address_coded == None:
			time.sleep(0.5)
			from_address_coded = gcode(user.get('address'))
			if from_address_coded == None:
				return_unknown_address(user,user.get('address'))
				return

		from_address = create_address_from_geocode(message["_from"]["name"], from_address_coded, email=user.get('username'))

		message["to"]["address"] = str(to_address_coded).replace(",","<br>")
		message["_from"]["address"] = str(from_address_coded).replace(",","<br>")

		obj_loc = save_letter(render_text(message), user, to_address, to_address_coded, from_address)
		return obj_loc
	else:
		return_unknown_address(user,to_address)
		return

def send_postcard(user,to_name,to_address,message,picture):
	to_address_coded = gcode(to_address)
	if to_address_coded == None:
		return jfail_address(to_address)

	if to_address_coded.valid_address:

		back = {"to": {"prefix": "", "name": to_name}, "_from": {"prefix": "", "name": user.get("name")}, "message": message}

		to_address = create_address_from_geocode(back["to"]["name"], to_address_coded)
		from_address_coded = gcode(user.get('address'))
		
		if from_address_coded == None:
			time.sleep(0.5)
			from_address_coded = gcode(user.get('address'))
			if from_address_coded == None:
				return jfail_address(user.get('address'))

		from_address = create_address_from_geocode(back["_from"]["name"], from_address_coded, email=user.get('username'))

		body["to"]["address"] = str(to_address_coded)
		body["_from"]["address"] = str(from_address_coded)

		_hash = hashlib.md5(user.get("username")+str(datetime.datetime.now())).hexdigest()
		save_postcard(_hash, picture, message, user, to_address, from_address)
		return jsuccess_with_txid(_hash)
	else:
		return jfail("invalid address")


def api_user_json(user):
	toReturn = {"status": "success"}
	postcards = user.get_postcards()
	postcards_json = []
	for p in postcards:
		p_obj = {}
		p_obj["date"] = arrow.get(parser.parse(p["job"]["date_created"])).format("h:m A MMMM D, YYYY")
		p_obj["picture"] = p["picture"]
		p_obj["price"] = float(p["job"]["price"])*1.75
		p_obj["name"] = ucfirst(p["job"]["to"]["name"])
		p_obj["message"] = p["job"]["message"]
		p_obj["address"] = ucfirst(p["job"]["to"]["address_line1"]) + ", " + ucfirst(p["job"]["to"]["address_city"]) + ", " + p["job"]["to"]["address_state"] + p["job"]["to"]["address_zip"]

	toReturn["results"] = postcards_json
	return json.dumps(toReturn)

