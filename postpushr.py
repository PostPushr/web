#!/usr/bin/env python

from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
from functions import *
import tests
from User import User
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ['sk']

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/test')
def test():
    return tests.run_advanced()

@app.route('/incoming/letter/email')
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
