import os, subprocess, lob, hashlib, datetime, boto, stripe, codecs, arrow
from celery import Celery, task
from var import *
from emails import *

celery = Celery('tasks', broker=os.environ['db'], backend=os.environ['db'])

@celery.task()
def wkhtmltopdf_letters(cmd,user,_hash,to_address,to_address_coded,from_address):
	d = "static/gen/{0}/".format(_hash)
	obj_loc = d+"{0}.pdf".format(_hash)
	s = subprocess.Popen(cmd, shell=True, close_fds=True)
	s.wait()
	file_url = "http://www."+os.environ['domain']+"/"+obj_loc
	_object = lob.Object.create(name=_hash, file=file_url, setting_id='100', quantity=1)
	job = lob.Job.create(name=_hash, to=to_address.id, objects=_object.id, from_address=from_address.id, packaging_id='1').to_dict()
	letters.insert({"jobid": _hash, "job": job})
	s3_upload.delay(_hash)
	cost = int(float(job["price"])*1.75*100)
	stripe.Charge.create(amount=cost,currency="usd",customer=user.get("token"))
	return_confirmed_letter(user,to_address_coded,cost,_hash)
	return job

@celery.task()
def s3_upload(dest_hash, acl='public-read'):
    key_name = "letters/" + dest_hash + "/" + dest_hash + ".pdf"

    # Connect to S3 and upload file.
    conn = boto.connect_s3()
    b = conn.get_bucket(os.environ["S3_BUCKET"])

    if b.get_key(key_name) != None:
        return b.get_key(key_name).generate_url(expires_in=300)

    sml = b.new_key(key_name)
    sml.set_contents_from_filename("static/gen/" + dest_hash + "/" + dest_hash + ".pdf")
    sml.set_acl(acl)

    return sml.generate_url(expires_in=300)


@celery.task()
def s3_upload_image(_hash, image, acl='public-read'):
	key_name = "postcards/" + _hash + "/" + _hash + ".pdf"

	# Connect to S3 and upload file.
	conn = boto.connect_s3()
	b = conn.get_bucket(os.environ["S3_BUCKET"])

	if b.get_key(key_name) != None:
		url = b.get_key(key_name).generate_url(expires_in=300)
	else:
		sml = b.new_key(key_name)
		sml.set_contents_from_file(image)
		sml.set_acl(acl)

		url = sml.generate_url(expires_in=300)

@celery.task()
def wkhtmltopdf_postcards(_hash, image, message, user, to_address, from_address, template, acl='public-read'):

	generated_html = template.render(img=url)

	d = "static/gen/{0}/".format(_hash)
	pdf_file_name = d+"{0}.pdf".format(_hash)
	html_file_name = d+"{0}.html".format(_hash)
	if not os.path.exists(d):
		os.makedirs(d)
	html_file = codecs.open(html_file_name, "w+b", "utf-8-sig")
	html_file.write(html)
	cmd = "{0}/wkhtmltopdf --encoding utf8 --page-height 101.6 --page-width 152.4 {1} {2}".format(bin_dir,html_file_name,pdf_file_name)
	s = subprocess.Popen(cmd, shell=True, close_fds=True)
	s.wait()
	file_url = "http://www."+os.environ['domain']+"/"+pdf_file_name
	job = lob.Postcard.create(name=_hash, to=to_address, front=file_url,message=message,from_address=from_address)
	postcards.insert({"jobid": _hash, "job": job})
	cost = int(float(job["price"])*1.75*100)
	stripe.Charge.create(amount=cost,currency="usd",customer=user.get("token"))
	



