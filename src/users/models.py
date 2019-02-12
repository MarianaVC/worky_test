from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import validators
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from rest_framework.authtoken.models import Token
from .choices import ORDER_STATUS
from albums.models import Album

class User(AbstractBaseUser,PermissionsMixin):
	"""Custom user based on Django Abstract User and PermissionMixin"""

	email = models.EmailField(
		('email address'),
		unique=True,
		error_messages={
			'unique': ("A user with that email already exists."),
		})	
	#date_joined = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	first_name = models.CharField(('first name'), max_length=100, null = True, blank = True)
	last_name = models.CharField(('last name'), max_length=100, null = True, blank = True)
	middle_name = models.CharField(max_length=64, verbose_name=('middle name'), blank=True, null = True)
	phone = models.CharField(max_length=64, verbose_name=('user phone'), null = True, blank = True)
	username = models.CharField(('username'),max_length=100,unique=True,help_text=('Required. 30 characters or fewer. Letters, digits and '
			'@/./+/-/_ only.'),validators=[validators.RegexValidator(
				r'^[\w.@+-]+$',
				('Enter a valid username. '
				 'This value may contain only letters, numbers '
				 'and @/./+/-/_ characters.'), 'invalid'),
		],
		error_messages={
			'unique': ("A user with that username already exists."),
		})	
	is_staff = models.BooleanField(
		('staff status'),
		default=False,
		help_text=('Designates whether the user can log into this admin '
				   'site.'))
	is_active = models.BooleanField(
		('active'),
		default=True,
		help_text=('Designates whether this user should be treated as '
				   'active.'))

	facebook_id = models.CharField(max_length=200, null = True, blank = True)
	profile_image = models.ImageField(upload_to='users/', max_length=500, blank=True, null = True)
	gender = models.CharField(max_length=10, blank=True, null = True)

	objects = UserManager()
	
	def image_tag(self):
		"""Set the image on edit view"""
		if self.pk is not None:
			if self.profile_image:
				return mark_safe('<img style="width:380px;height:auto" src="users/%s">' % self.profile_image)
	
	def get_short_name(self):
		return self.first_name

	image_tag.allow_tags = True
	image_tag.short_description = 'Current profile picture'

	# this is needed to use this model with django auth as a custom user class
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']



	class Meta:
		managed = True
		abstract = False
		db_table = 'auth_user'


#@receiver(post_save, sender=settings.AUTH_USER_MODEL)
#def create_auth_token(sender, instance=None, created=False, **kwargs):
	#"""Token for authorization, whenever a user is created a token is generated for API use"""
	#Token.objects.get_or_create(user=instance)	
	#Token.objects.get_or_create(user=instance)	

class Order(models.Model):
	"""Model for oder"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user_order')
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	status = models.CharField(choices = ORDER_STATUS, default = 'pending', max_length=200)
	total_payed = models.FloatField(default = 0.0)

	def save(self, *args, **kwargs):
		"""Save created at and updated at"""
		if not self.id:
			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Order, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Order'
		verbose_name_plural = 'Orders'

class OrderItem(models.Model):
	"""Items for oders"""
	order = models.ForeignKey(Order, related_name = 'order')
	album = models.ForeignKey(Album, related_name='album')
	quantity = models.IntegerField(default = 0)

	@property
	def total(self):
		album_price = Album.objects.get(pk = self.album.id).price
		total = self.quantity * album_price
		return total

	class Meta:
		verbose_name = 'Order Items'
		verbose_name_plural = 'Orders items '





