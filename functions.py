from jinja2 import Template, Environment, FileSystemLoader
import requests, hashlib, os, subprocess
import lob

bin_dir = os.environ['bin_dir']
lob.api_key = os.environ['lob_api_key']
client = pymongo.MongoClient(os.environ['db'])
db = client.postpushr
users = db.users

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

def create_user(username, password, **kwargs):
	return str(users.insert({"username": username, "password": hash_password(password), **kwargs}))