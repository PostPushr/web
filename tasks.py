import os, subprocess, lob, hashlib, datetime
from celery import Celery, task
from var import *
celery = Celery('tasks', broker=os.environ['db'])

@celery.task()
def wkhtmltopdf_letters(cmd):
	s = subprocess.Popen(cmd, shell=True, close_fds=True)
	s.wait()
	_object = lob.Object.create(name=hashlib.md5(user.get("username")+str(datetime.datetime.now())).hexdigest(), file="http://www."+os.environ['domain']+"/"+obj_loc, setting_id='100', quantity=1)
	job = lob.Job.create(name=hashlib.md5(user.get("username")+str(datetime.datetime.now())).hexdigest(), to=to_address.id, objects=_object.id, from_address=from_address.id, packaging_id='1').to_dict()
	letters.insert(job)
	return job