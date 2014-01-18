from jinja2 import Template, Environment, FileSystemLoader
import requests, hashlib, os, subprocess
import lob, pymongo

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

def format_address(address):
	address_dict = address.to_dict()
	address_str = ""
	to_add = [[address_dict["address_line1"]], [address_dict["address_line2"]], [address_dict["address_city"], ", ", address_dict["address_state"]], [address_dict["address_country"], " ", address_dict["address_zip"]]]
	for s in to_add:
		try:
			for ss in s:
				address_str += ss
			address_str += "<br />"
		except Exception:
			continue
	#ob.Address.delete(id=address.id)
	return address_str.strip()

def remove_addresses():
	for a in lob.Address.list():
		lob.Address.delete(id=a.id)

def create_user(username, hashed_password, **kwargs):
	#Expect: Name, Email, Token, Snapchat, ...
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

def send_letter(from_email,to_name,to_address,body):
	#TODO: Send letter, see tests
	raise NotImplementedError
