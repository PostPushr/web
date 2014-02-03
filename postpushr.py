#!/usr/bin/env python

from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
from functions import *
import tasks
from User import User
from bson.objectid import ObjectId
from dateutil import parser
import arrow, urllib

app = Flask(__name__)
app.secret_key = os.environ['sk']

launch_celery()

@app.route('/api/login', methods=['POST'])
def api_login():
	username = request.form.get('email')
	password = request.form.get('password')

	if None in [username,password]:
		return Response(response=jfail("missing required parameters"), status=200)

	user = User(username)
	if user.is_valid():
		if user.check_pass_hash(password):
			return Response(response=jsuccess(), status=200)
		else:
			return Response(response=jfail("incorrect password"), status=200)
	else:
		return Response(response=jfail("user does not exist"), status=200)

@app.route('/api/token', methods=['POST'])
def api_token_request():
	username = request.form.get('email')
	password = request.form.get('password')
	token = request.form.get('token')

	if len([x for x in [username,password,token] if x == None]) > 1:
		return Response(response=jfail("missing required parameters"), status=200)

	user = User(username)
	if user.is_valid():
		if password:
			if user.check_pass_hash(password):
				return Response(response=jsuccess_with_token(user.get_token()), status=200)
			else:
				return Response(response=jfail("incorrect password"), status=200)
		else:
			checked = user.check_token(token)
			if checked == 1:
				return Response(response=jsuccess(), status=200)
			elif checked == 0:
				return Response(response=jfail("expired token"), status=200)
			else:
				return Response(response=jfail("invalid token"), status=200)
	else:
		return Response(response=jfail("user does not exist"), status=200)

@app.route('/api/user', methods=['POST'])
def api_user():
	username = request.form.get('email')
	token = request.form.get('token')

	if None in [username,token]:
		return Response(response=jfail("missing required parameters"), status=200)

	user = User(username)
	if user.is_valid():
		checked = user.check_token(token)
		if checked == 1:
			return Response(response=api_user_json(user), status=200)
		elif checked == 0:
			return Response(response=jfail("expired token"), status=200)
		else:
			return Response(response=jfail("invalid token"), status=200)
	else:
		return Response(response=jfail("user does not exist"), status=200)


@app.route('/api/register', methods=['POST'])
def api_register():
	username = request.form.get('email').strip()
	password = request.form.get('password')
	name = request.form.get('name').strip()
	address = request.form.get('address').lower().strip()
	token = request.form.get('token')

	if None in [username,password,name,address,token]:
		return Response(response=jfail("missing required parameters"), status=200)

	if User(username).is_valid():
		return Response(response=jfail('username taken'), status=200)
	cust = create_stripe_cust(token,username)
	if cust == None:
		return Response(response=jfail('card was declined'), status=200)

	userid = create_user(username,password,name=name,token=cust,address=address)
	return Response(response=jsuccess(), status=200)

@app.route('/api/create/callback', methods=['POST'])
def api_postcard_callback():
	txid = request.form.get('txid')

	if None in [txid]:
		return Response(response=jfail("missing required parameters"), status=200)

	job = postcards.find_one({'jobid': txid})
	if job == None:
		return Response(response=json.dumps({"status": "pending"}), status=200)

	cost = int(float(job["price"])*1.75*100)
	return Response(response=json.dumps({"status": "success", "results": {"price": '$%0.2f' % (float(cost)/100.0), "date": arrow.get(parser.parse(job["date_created"])).format("h:m A MMMM D, YYYY")}}), status=200) 

@app.route('/api/create/postcard', methods=['POST'])
def api_postcard_create():
	username = request.form.get('email')
	token = request.form.get('token')
	name = request.form.get('name')
	message = request.form.get('message')
	address = request.form.get('address')
	picture = request.files['picture']

	if None in [username,password,name,message,address,picture]:
		return Response(response=jfail("missing required parameters"), status=200)

	user = User(username)
	if user.is_valid():
		checked = user.check_token(token)
		if checked == 1:
			return Response(response=send_postcard(user,name,address,message,picture), status=200)
		elif checked == 0:
			return Response(response=jfail("expired token"), status=200)
		else:
			return Response(response=jfail("invalid token"), status=200)
	else:
		return Response(response=jfail("user does not exist"), status=200)

@app.route('/', methods=['POST', 'GET'])
def index():
	if 'userid' in session:
		return redirect(url_for('documents'))
	if request.method == "POST":
		user = User(request.form.get('email'))
		if user.is_valid():
			if user.check_pass(request.form.get('password')):
				session["userid"] = str(user.get("_id"))
				return redirect(url_for('documents'))
			else:
				flash("Your password was incorrect.")
		else:
			session["username"] = request.form.get('email').lower()
			session["password"] = request.form.get('password')
			return redirect(url_for('signup'))
	return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if 'userid' in session:
		return redirect(url_for('documents'))
	if request.method == "POST":
		username = session.pop("username").strip()
		password = session.pop("password")
		name = request.form.get("name").strip()
		snapchat = request.form.get("snapchat").strip()
		token = request.form.get("stripeToken")
		address = request.form.get("address").lower().strip()
		if User(username).is_valid():
			flash("That email has already been registered.")
			return redirect(url_for('index'))
		cust = create_stripe_cust(token,username)
		if cust == None:
			flash("Your card was declined.")
			return redirect(url_for('signup'))
		userid = create_user(username,hash_password(password),name=name,snapchat=snapchat,token=cust,address=address)
		session["userid"] = userid
		return redirect(url_for('documents'))
	return render_template('signup.html',email=session["username"],smarty_key=os.environ['smarty_key'])

@app.route('/documents', methods=['POST', 'GET'])
def documents():
	if session.get('userid') == None:
		return redirect(url_for('index'))
	user = User(None,userid=session["userid"])
	if user.is_valid():
		return render_template('documents.html',user=user)
	else:
		return redirect(url_for('logout'))

@app.route('/letter/<_hash>')
def get_letter(_hash):
	l = letters.find_one({"jobid": _hash})
	if session.get('userid') == None or l == None:
		return redirect(url_for('index'))
	user = User(None,userid=session["userid"])
	if user.is_valid():
		return render_template('document.html',l=l)
	else:
		return redirect(url_for('logout'))

@app.route('/logout')
def logout():
	session["userid"] = None
	session.clear()
	return redirect(url_for('index'))

@app.route('/incoming/letter/email', methods=['POST', 'GET'])
def incoming_letter_email():
	body = unicode(request.form.get('text')).encode('ascii','xmlcharrefreplace').replace("\n","<br />")
	regexp = re.findall(r'[\w\.-]+@[\w\.-]+',request.form.get('from'))

	if len(regexp) > 0:
		username = regexp[len(regexp)-1].lower()
	else:
		return Response(response=jfail("missing parameters"), status=200)

	to_name = request.form.get('to')
	to_address = unicode(request.form.get('subject')).encode('ascii','xmlcharrefreplace').lower().replace("fw:","").replace("re:","").strip()

	if None in [body,username,to_name,to_address]:
		return Response(response=jfail("missing parameters"), status=200)

	user = User(username)
	if user.is_valid():
		send_letter(user,to_name,to_address,body)
	else:
		return_unknown_sender(username)
		return Response(response=jfail("unknown sender"), status=200)

	return Response(response=jsuccess(), status=200)

@app.route('/incoming/email/add', methods=['POST', 'GET'])
def add_new_email():
	regexp = re.findall(r'[\w\.-]+@[\w\.-]+',request.form.get('from'))
	if len(regexp) > 0:
		new_email = regexp[len(regexp)-1].lower()
	else:
		return Response(response=jfail("missing parameters"), status=200)

	userid = unicode(request.form.get('subject')).encode('ascii','xmlcharrefreplace')
	user = User(None,userid=userid)
	if user.is_valid():
		user.add_email(new_email)
		confirm_email_addition(user, new_email)
	else:
		return Response(response=jfail("unknown sender"), status=200)

	return Response(response=jsuccess(), status=200)

@app.route('/incoming/email', methods=['POST', 'GET'])
def incoming_email():
	text = unicode(request.form.get('text')).encode('ascii','xmlcharrefreplace')
	html = unicode(request.form.get('html')).encode('ascii','xmlcharrefreplace')
	regexp = re.findall(r'[\w\.-]+@[\w\.-]+',request.form.get('from'))

	if len(regexp) > 0:
		_from = regexp[len(regexp)-1]
	else:
		_from = request.form.get('from')

	to = request.form.get('to')

	subject = unicode(request.form.get('subject')).encode('ascii','xmlcharrefreplace')

	forward_email(_from,subject,text,html)

	return Response(response=jsuccess(), status=200)

@app.template_filter('ucfirst')
def ucfirst_filter(txt):
	return ucfirst(txt)

@app.template_filter('dt')
def dt_filer(dt):
	return arrow.get(parser.parse(dt)).format("MMMM D, YYYY")

@app.template_filter('s3URL')
def s3URL(_hash):
	return bitly.shorten(tasks.s3_upload(_hash))["url"]

@app.template_filter('escURL')
def escURL(url):
	return urllib.quote_plus(url)

if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=(os.environ.get('dev') == "True"))
	else:
		app.run(host='0.0.0.0',port=5000,debug=(os.environ.get('dev') == "True"))
