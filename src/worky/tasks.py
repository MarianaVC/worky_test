from __future__ import absolute_import, unicode_literals
from celery import task
from worky.celeryconf import app  
from albums.models import Album
from django.core.mail import EmailMessage
from users.models import User
@app.task(bind=True)
def send_mail(self):
	albums = Album.objects.all()
	ids = []
	for album in albums:
		print(album.quantity)
		if album.quantity < 50:
			ids.append(album.id)

	if len(ids) > 0:
		albums_list = ','.join(map(str, ids))
		text = "The following albums with ids:(" + albums_list + ")have reached quantity less than 50. Try updating stock"		

		users = User.objects.filter(is_staff = True)
		for user in users:

			email = EmailMessage('Django Admin',text, to=[user.email])
		
		email.send()