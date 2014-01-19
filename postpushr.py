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

@app.route('/api/login', methods=['POST', 'GET'])
def api_login():
	email = request.form.get('email')
	password = request.form.get('password')

	user = User(email)
	if user.is_valid():
		if user.check_pass(password):
			return Response(response=api_user_json(user), status=200)
		else:
			return Response(response=jfail("incorrect password"), status=200)
	else:
		return Response(response=jfail("user does not exist"), status=200)

@app.route('/', methods=['POST', 'GET'])
def index():
	if session.get('userid'):
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
	if session.get('userid'):
		return redirect(url_for('documents'))
	if request.method == "POST":
		username = session.pop("username")
		password = session.pop("password")
		name = request.form.get("name")
		snapchat = request.form.get("snapchat")
		token = request.form.get("stripeToken")
		address = request.form.get("address")

		cust = create_stripe_cust(token,username)
		if cust == None:
			flash("Your card was declined.")
			return redirect(url_for('logout'))
		userid = create_user(username,hash_password(password),name=name,snapchat=snapchat,token=cust,address=address)
		session["userid"] = userid
		return redirect(url_for('documents'))
	return render_template('signup.html',email=session["username"],smarty_key=os.environ['smarty_key'])

@app.route('/documents', methods=['POST', 'GET'])
def documents():
	if session.get('userid') == None:
		return redirect(url_for('index'))
	user = User(None,userid=session["userid"])
	return render_template('documents.html',user=user)

@app.route('/letter/<_hash>')
def get_letter(_hash):
	if session.get('userid') == None:
		return redirect(url_for('index'))
	l = letters.find_one({"jobid": _hash})
	return render_template('document.html',l=l)

@app.route('/logout')
def logout():
	session["userid"] = None
	session.clear()
	return redirect(url_for('index'))

@app.route('/incoming/letter/email', methods=['POST', 'GET'])
def incoming_letter_email():
	print request.form.get('charsets')
	body = unicode(request.form.get('text')).replace("\n","<br />")
	regexp = re.findall(r"\w+@\w+.\w+",request.form.get('from'))

	if len(regexp) > 0:
		username = regexp[len(regexp)-1].lower()
	else:
		return Response(response=jfail("missing parameters"), status=200)

	to_name = request.form.get('to')
	to_address = unicode(request.form.get('subject'))

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
	regexp = re.findall(r"\w+@\w+.\w+",request.form.get('from'))
	if len(regexp) > 0:
		new_email = regexp[len(regexp)-1].lower()
	else:
		return Response(response=jfail("missing parameters"), status=200)

	userid = unicode(request.form.get('subject'))

	user = User(None,userid=userid)
	if user.is_valid():
		user.add_email(new_email)
		confirm_email_addition(user, new_email)
	else:
		return Response(response=jfail("unknown sender"), status=200)

	return Response(response=jsuccess(), status=200)

@app.route('/incoming/email', methods=['POST', 'GET'])
def incoming_email():
	text = unicode(request.form.get('text'))
	html = unicode(request.form.get('html'))
	regexp = re.findall(r"\w+@\w+.\w+",request.form.get('from'))

	if len(regexp) > 0:
		_from = regexp[len(regexp)-1]
	else:
		_from = request.form.get('from')

	to = request.form.get('to')
	subject = request.form.get('subject')

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
