from var import *
from flask import url_for, g
import sendgrid

def return_unknown_sender(email):
	subject = "Unregistered PostPushr User"
	text = "Hello,\n\nYou are receiving this email because you tried to send a physical document via PostPushr. PostPushr is a service that allows you to easily and affordably forward digital documents to physical locations.\n\nIn order to use our service, you must first register for an account. To sign up, please visit http://www.{0}.\n\nPostPushr Error Bot".format(os.environ['domain'])
	html = "Hello,<br /><br />You are receiving this email because you tried to send a physical document via PostPushr. PostPushr is a service that allows you to easily and affordably forward digital documents to physical locations.<br /><br />In order to use our service, you must first register for an account. To sign up, please visit <a href='http://www.{0}'>our site</a>.<br /><br />PostPushr Error Bot".format(os.environ['domain'])
	message = sendgrid.Message(("errors@{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(email)
	s.web.send(message)

def return_over_geocode_api(user):
	subject = "PostPushr API Error"
	text = "Hello {0},\n\nYou are receiving this email because you tried to send a physical document via PostPushr. Unfortunately, PostPushr has currently exceeded the daily limit of the API we use for address normalization.\n\nPlease try to to send your document again tomorrow, or visit http://www.{2} for more info.\n\nPostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	html = "Hello {0},<br /><br />ou are receiving this email because you tried to send a physical document via PostPushr. Unfortunately, PostPushr has currently exceeded the daily limit of the API we use for address normalization.<br /><br />Please try to to send your document again tomorrow, or visit <a href='http://www.{2}'>our site</a> for more info.<br /><br />PostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	message = sendgrid.Message(("errors@{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(user.get("mailing"),user.get("name"))
	s.web.send(message)

def return_unknown_address(user,address):
	try:
		if g.over_api:
			return_over_geocode_api(user)
			return
	except Exception:
		pass
	
	subject = "Unknown PostPushr Destination Address"
	text = "Hello {0},\n\nYou are receiving this email because you tried to send a physical document via PostPushr to an invalid address. PostPushr could not recognize \"{1}\".\n\nPlease try to to send your document again, or visit http://www.{2} for more info.\n\nPostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	html = "Hello {0},<br /><br />You are receiving this email because you tried to send a physical document via PostPushr to an invalid address. PostPushr could not recognize <tt style='display: inline;'>{1}</tt>.<br /><br />Please try to to send your document again, or visit <a href='http://www.{2}'>our site</a> for more info.<br /><br />PostPushr Error Bot".format(user.get("name"),address,os.environ['domain'])
	message = sendgrid.Message(("errors@{0}".format(os.environ['domain']),"PostPushr Error Bot"), subject, text, html)
	message.add_to(user.get("mailing"),user.get("name"))
	s.web.send(message)

def return_confirmed_letter(user,address,cost,_hash):
	subject = "PostPushr Letter Confirmation"
	text = "Hello {0},\n\nYou are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to \"{1}\" at \"{2}\", for a total cost of {3}.\n\nPlease visit http://www.{4} for more info.\n\nPostPushr Confirmation Bot".format(user.get("name"),address.name,str(address),'$%0.2f' % (float(cost)/100.0),os.environ['domain']+"/letter/"+_hash)
	html = "Hello {0},<br /><br />You are receiving this email because you have sent a physical document via PostPushr. PostPushr has successfully posted your letter to <tt style=\"display:inline;\">{1}</tt> at <tt style=\"display:inline;\">{2}</tt>, for a total cost of {3}.<br /><br />Please visit <a href='http://www.{4}'>our site</a> for more info.<br /><br />PostPushr Confirmation Bot".format(user.get("name"),address.name,str(address),'$%0.2f' % (float(cost)/100.0),os.environ['domain']+"/letter/"+_hash)
	message = sendgrid.Message(("confirmations@{0}".format(os.environ['domain']),"PostPushr Confirmation Bot"), subject, text, html)
	message.add_to(user.get("mailing"),user.get("name"))
	s.web.send(message)

def confirm_email_addition(user,new_email):
	subject = "PostPushr Email Addition Confirmation"
	text = "Hello {0},\n\nYou are receiving this email because you have added a new email address to your account on PostPushr. PostPushr will now recognize <tt style=\"display:inline;\">{1}</tt> as being associated with your account.\n\nPostPushr Confirmation Bot".format(user.get("name"),new_email)
	html = "Hello {0},<br /><br />You are receiving this email because you have added a new email address to your account on PostPushr. PostPushr will now recognize <tt style=\"display:inline;\">{1}</tt> as being associated with your account.<br /><br />PostPushr Confirmation Bot".format(user.get("name"),new_email)
	message = sendgrid.Message(("confirmations@{0}".format(os.environ['domain']),"PostPushr Confirmation Bot"), subject, text, html)
	message.add_to(user.get("username"),user.get("name"))
	message.add_to(new_email,user.get("name"))
	s.web.send(message)

def forward_email(_from,subject,text,html):
	if html:
		message = sendgrid.Message(_from, subject, text, html)
	else:
		message = sendgrid.Message(_from, subject, text)
	message.add_to(os.environ['admin_email'])
	s.web.send(message)
