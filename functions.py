from jinja2 import Template, Environment, FileSystemLoader
import requests, hashlib, os, subprocess
import lob, pymongo
from pygeocoder import Geocoder

bin_dir = os.environ['bin_dir']
lob.api_key = os.environ['lob_api_key']
client = pymongo.MongoClient(os.environ['db'])
db = client.postpushr
users = db.users
letters = db.letters
postcards = db.postcards

def save(html,user_id):
	d = "static/gen/{0}/".format(user_id)
	pdf_file_name = d+"{0}.pdf".format(user_id)
	html_file_name = d+"{0}.html".format(user_id)
	if not os.path.exists(d):
		os.makedirs(d)
	html_file = open(html_file_name, "w+b")
	html_file.write(html)
	s = subprocess.Popen("{0}/wkhtmltopdf {1} {2}".format(bin_dir,html_file_name,pdf_file_name), shell=True, close_fds=True)
	s.wait()
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
	#Expect: Username, Password, Name, Email, Token, Snapchat, Address, ...
	kwargs["username"] = username
	kwargs["password"] = hashed_password
	return str(users.insert(**kwargs))

def sha1(text):
	m = hashlib.sha1()
	m.update(text)
	return m.hexdigest()

def hash_password(pasword):
	return sha1(sha1(password)+sha1(os.environ["salt"]))

def return_unknown_sender(email):
	#TODO: Sendgrid email in response, with form to registration
	raise NotImplementedError

def create_address_from_geocode(name, address_coded):
	return functions.lob.Address.create(name=name, address_line1=address_coded.street_number+address_coded.route, address_city=address_coded.city, address_state=address_coded.state__short_name, address_country=address_coded.country__short_name, address_zip=address_coded.postal_code)

def send_letter(user,to_name,to_address,body):
	to_address_coded = Geocoder.geocode(to_address)

	if to_address_coded.valid_address:

		to_name = to_name.replace("_"," ")
		message = {"to": {"prefix": "Dear", "name": to_name}, "_from": {"prefix": "Sincerely,", "name": user.get("name")}, "body": body}

		to_address = create_address_from_geocode(message["to"]["name"], to_address_coded)

		from_address_coded = Geocoder.geocode(user.get('address'))
		from_address = create_address_from_geocode(message["_from"]["name"], from_address_coded)

		message["to"]["address"] = str(to_address)
		message["_from"]["address"] = str(from_address)

		obj_loc = functions.save(functions.render_text(message), hashlib.md5(user).hexdigest())
		_object = functions.lob.Object.create(name=hashlib.md5(user+str(datetime.datetime.now())).hexdigest(), file="http://"+os.environ['domain']+"/"+obj_loc, setting_id='100', quantity=1)
		job = functions.lob.Job.create(name=hashlib.md5(user+str(datetime.datetime.now())).hexdigest(), to=to_address.id, objects=_object.id, from_address=from_address.id, packaging_id='1').to_dict()
		letters.insert(job)
		return job

