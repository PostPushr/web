from flask import url_for
from jinja2 import Template, Environment, FileSystemLoader
import requests, hashlib, os, subprocess, json
import lob, pymongo, sendgrid, stripe, datetime, re, boto
from pygeocoder import Geocoder
from tasks import wkhtmltopdf_letters, s3_upload
from var import *


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
	wkhtmltopdf_letters.delay(cmd, user, _hash, to_address, to_address_coded, from_address)
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
	return str(users.find_one({"username": username}))

def sha1(text):
	m = hashlib.sha1()
	m.update(text)
	return m.hexdigest()

def hash_password(password):
	return sha1(sha1(password)+sha1(os.environ["salt"]))

def return_unknown_sender(email):
	subject = "Unregistered PostPushr User"
	text = "Hello,\n\nYou are receiving this email because you tried to send a physical document via PostPushr. PostPushr is a service that allows you to easily and affordably forward digital documents to physical locations.\n\nIn order to use our service, you must first register for an account. To sign up, please visit http://www.{0}.\n\nPostPushr Error Bot".format(os.environ['domain'])
	html = "Hello,<br /><br />You are receiving this email because you tried to send a physical document via PostPushr. PostPushr is a service that allows you to easily and affordably forward digital documents to physical locations.<br /><br />In order to use our service, you must first register for an account. To sign up, please visit <a href='http://www.{0}'>our site</a>.<br /><br />PostPushr Error Bot".format(os.environ['domain'])
	message = sendgrid.Message(("errors@support.{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(email)
	s.web.send(message)

def return_unknown_address(user,address):
	subject = "Unknown PostPushr Destination Address"
	text = "Hello {0},\n\nYou are receiving this email because you tried to send a physical document via PostPushr to an invalid address. PostPushr could not recognize \"{1}\".\n\nPlease try to to send your document again, or visit http://www.{2} for more info.\n\nPostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	html = "Hello {0},<br /><br />You are receiving this email because you tried to send a physical document via PostPushr to an invalid address. PostPushr could not recognize <pre>{1}</pre>.<br /><br />Please try to to send your document again, or visit <a href='http://www.{2}'>our site</a> for more info.<br /><br />PostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	message = sendgrid.Message(("errors@support.{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(user.get("username"),user.get("name"))
	s.web.send(message)

def return_confirmed_letter(user,address,cost,_hash):
	subject = "PostPushr Letter Confirmation"
	text = "Hello {0},\n\nYou are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to \"{1}\", for a total cost of {2}.\n\nPlease {3} for more info.\n\nPostPushr Confirmation Bot".format(user.get("name"),address,cost,url_for('get_document',_hash=_hash))
	html = "Hello {0},<br /><br />You are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to <pre>{1}</pre>, for a total cost of {2}.<br /><br />Please visit <a href='{3}'>our site</a> for more info.<br /><br />PostPushr Confirmation Bot".format(user.get("name"),address,cost,_hash=_hash)
	message = sendgrid.Message(("confirmations@support.{0}".format(os.environ['domain']),"PostPushr Confirmation Bot"), subject, text, html)
	message.add_to(user.get("username"),user.get("name"))
	s.web.send(message)

def create_address_from_geocode(name, address_coded, email=None):
	return lob.Address.create(name=name, address_line1=address_coded.street_number+" "+address_coded.route, address_city=address_coded.city, address_state=address_coded.state__short_name, address_country=address_coded.country__short_name, address_zip=address_coded.postal_code, email=email)

def ucfirst(txt):
	return ' '.join([x[:1].upper()+x[1:].lower() for x in txt.split(' ')])

def send_letter(user,to_name,to_address,body):
	to_address_coded = Geocoder.geocode(to_address)

	if to_address_coded.valid_address:

		to_name = to_name.replace("_"," ")
		to_name = re.sub("@\w+."+os.environ["domain"],"",to_name)
		to_name = ucfirst(to_name)

		message = {"to": {"prefix": "Dear", "name": to_name}, "_from": {"prefix": "Sincerely,", "name": user.get("name")}, "body": body}

		to_address = create_address_from_geocode(message["to"]["name"], to_address_coded)

		from_address_coded = Geocoder.geocode(user.get('address'))
		from_address = create_address_from_geocode(message["_from"]["name"], from_address_coded, email=user.get('username'))

		message["to"]["address"] = str(to_address_coded).replace(",","<br>")
		message["_from"]["address"] = str(from_address_coded).replace(",","<br>")

		obj_loc = save(render_text(message), user, to_address, to_address_coded, from_address)
		return obj_loc
	else:
		return_unknown_address(user,to_address)

