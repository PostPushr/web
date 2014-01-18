#!/usr/bin/env python

from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
from functions import *
import tests
from User import User
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ['sk']

@app.route('/', methods=['POST', 'GET'])
def index():
	if session.get('userid'):
		return redirect(url_for('settings'))
	if request.method == "POST":
		user = User(request.form.get('email'))
		if user.is_valid():
			if user.check_pass(request.form.get('password')):
				session["userid"] = str(user.get("_id"))
				return redirect(url_for('settings'))
			else:
				flash("Your password was incorrect.")
		else:
			session["username"] = request.form.get('email')
			session["password"] = request.form.get('password')
			return redirect(url_for('signup'))
	return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if session.get('userid'):
		return redirect(url_for('settings'))
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
		return redirect(url_for('settings'))
	return render_template('signup.html',email=session["username"],smarty_key=os.environ['smarty_key'])

@app.route('/settings', methods=['POST', 'GET'])
def settings():
	if session.get('userid') == None:
		return redirect(url_for('index'))
	user = User(session["userid"])
	return render_template('settings.html',user=user)

@app.route('/logout')
def logout():
	session["userid"] = None
	session.clear()
	return redirect(url_for('index'))

@app.route('/incoming/letter/email', methods=['POST', 'GET'])
def incoming_letter_email():
	body = request.form.get('text')
	username = request.form.get('from')
	to_name = request.form.get('to')
	to_address = request.form.get('subject')

	if None in [body,username,to_name,to_address]:
		return Response(response=jfail("missing parameters"), status=200)

	user = User(username)
	if user.is_valid():
		send_letter(user,to_name,to_address,body)
	else:
		return_unknown_sender(username)
		return Response(response=jfail("unknown sender"), status=200)

	return Response(response=jsuccess(), status=200)


if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=False)
	else:
		app.run(host='0.0.0.0',port=5000,debug=True)
