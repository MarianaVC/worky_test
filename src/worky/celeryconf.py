import os

from celery import Celery  
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worky.settings")

app = Celery('worky',include=['worky.tasks'])

CELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS=("tasks")

app.config_from_object('django.conf:settings')  


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
	# Calls test('hello') every 10 seconds.
	sender.add_periodic_task(10.0, test.s('verifying stock'), name='add every 10')
#	sender.add_periodic_task(3600.0, test.s('verifying stock'), name='add every 10')

@app.task
def test(arg):
	print(arg)
	from worky.tasks import send_mail
	send_mail()	