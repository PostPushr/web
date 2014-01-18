import os, subprocess
from celery import Celery, task

celery = Celery('tasks', broker=os.environ['db'])

@celery.task()
def execute_command(cmd):
	s = subprocess.Popen(cmd, shell=True, close_fds=True)
	s.wait()