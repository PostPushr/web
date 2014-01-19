from var import *
from flask import url_for
import sendgrid

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
	html = "Hello {0},<br /><br />You are receiving this email because you tried to send a physical document via PostPushr to an invalid address. PostPushr could not recognize <pre style='display: inline;'>{1}</pre>.<br /><br />Please try to to send your document again, or visit <a href='http://www.{2}'>our site</a> for more info.<br /><br />PostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	message = sendgrid.Message(("errors@support.{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(user.get("username"),user.get("name"))
	s.web.send(message)

def return_confirmed_letter(user,address,cost,_hash):
	subject = "PostPushr Letter Confirmation"
	text = "Hello {0},\n\nYou are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to \"{1}\", for a total cost of {2}.\n\nPlease {3} for more info.\n\nPostPushr Confirmation Bot".format(user.get("name"),address,'$%0.2f' % cost,os.environ['domain']+"/letter/"+_hash)
	html = "Hello {0},<br /><br />You are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to <pre style='display: inline;'>{1}</pre>, for a total cost of {2}.<br /><br />Please visit <a href='http://www.{3}'>our site</a> for more info.<br /><br />PostPushr Confirmation Bot".format(user.get("name"),address,'$%0.2f' % cost,os.environ['domain']+"/letter/"+_hash)
	message = sendgrid.Message(("confirmations@support.{0}".format(os.environ['domain']),"PostPushr Confirmation Bot"), subject, text, html)
	message.add_to(user.get("username"),user.get("name"))
	s.web.send(message)
