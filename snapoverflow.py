#!/usr/bin/env python

from flask import Flask, Response, session, redirect, url_for, escape, request, render_template, g, flash, make_response
from functions import *
import tests
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = os.environ['sk']

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/test')
def test():
    return tests.run_simple()

@app.route('/send')
def send():
	return ""


if __name__ == '__main__':
	if os.environ.get('PORT'):
		app.run(host='0.0.0.0',port=int(os.environ.get('PORT')),debug=False)
	else:
		app.run(host='0.0.0.0',port=5000,debug=True)
