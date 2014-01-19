import os, subprocess, lob, hashlib, datetime, boto, stripe
from celery import Celery, task
from var import *

celery = Celery('tasks', broker=os.environ['db'])

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
	cost = float(job["price"])*1.75
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