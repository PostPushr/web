from jinja2 import Template, Environment, FileSystemLoader
import requests, hashlib, os, subprocess, json
import lob, pymongo, stripe, datetime, re, boto
from pygeocoder import Geocoder, GeocoderError
from tasks import wkhtmltopdf_letters, s3_upload
from var import *
from emails import *


def launch_celery():
    p = subprocess.Popen("celery worker -q -A tasks > /dev/null 2>&1 &", shell=True, close_fds=True)
    p.wait()

def create_stripe_cust(token,email):
	try:
		customer = stripe.Customer.create(card=token,description="PostPushr: "+email)
		return customer.id
	except stripe.error.CardError:
		return None
	
def jsuccess():
	return json.dumps({"status": "success"})

def jfail(reason):
	return json.dumps({"status": "error","error": reason})

def save(html, user, to_address, to_address_coded, from_address):
	_hash = hashlib.md5(user.get("username")+str(datetime.datetime.now())).hexdigest()
	d = "static/gen/{0}/".format(_hash)
	pdf_file_name = d+"{0}.pdf".format(_hash)
	html_file_name = d+"{0}.html".format(_hash)
	if not os.path.exists(d):
		os.makedirs(d)
	html_file = open(html_file_name, "w+b")
	html_file.write(html)
	cmd = "{0}/wkhtmltopdf -s Letter {1} {2}".format(bin_dir,html_file_name,pdf_file_name)
	wkhtmltopdf_letters.delay(cmd, user, _hash, to_address, str(to_address_coded), from_address)
	return pdf_file_name

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

def send_letter(user,to_name,to_address,body):
	try:
		to_address_coded = Geocoder.geocode(to_address)
	except GeocoderError:
		return_unknown_address(user,to_address)
		return

	if to_address_coded.valid_address:

		to_name = to_name.replace("_"," ")
		to_name = re.sub("@\w+."+os.environ["domain"],"",to_name)
		to_name = ucfirst(to_name)

		message = {"to": {"prefix": "", "name": to_name}, "_from": {"prefix": "", "name": user.get("name")}, "body": body}

		to_address = create_address_from_geocode(message["to"]["name"], to_address_coded)

		from_address_coded = Geocoder.geocode(user.get('address'))
		from_address = create_address_from_geocode(message["_from"]["name"], from_address_coded, email=user.get('username'))

		message["to"]["address"] = str(to_address_coded).replace(",","<br>")
		message["_from"]["address"] = str(from_address_coded).replace(",","<br>")

		obj_loc = save(render_text(message), user, to_address, to_address_coded, from_address)
		return obj_loc
	else:
		return_unknown_address(user,to_address)
		return

