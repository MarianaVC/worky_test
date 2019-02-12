from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from .choices import SCORE_CHOICES
from django.db.models import Avg
# Create your models here.


class Artist(models.Model):
	"""Model for Album Artist"""
	artistic_name =  models.CharField('Artistic name', max_length = 200, blank = False, null = False )
	original_name =  models.CharField('Original name', max_length = 200, null = True)
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at',auto_now = True, null = True) 
	author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = 'Uploaded by',related_name = 'album_artist', blank = True, default=None,null=True,on_delete=models.SET_NULL)
	slug = models.SlugField('Slug', max_length = 150, unique = True, editable = False)
	profile_picture = models.ImageField(upload_to = 'artists/', max_length=500, blank = True, null = True, default=None)

	def __str__(self):
		"""Get human-readable representation"""				
		return self.artistic_name

	def save(self, *args, **kwargs):
		"""Generate the slug based on artistic name on first save and modify created_at and updated_at"""
		if not self.id:
			# Newly created object, so set slug and created_at
			self.slug = slugify(self.artistic_name)
			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Artist, self).save(*args, **kwargs)

	def image_tag(self):
		"""Set the image on edit view"""
		if self.pk is not None:
			if self.profile_picture:
				return mark_safe('<img style="width:380px;height:auto" src="%s">' % self.profile_picture.url)

	image_tag.allow_tags = True
	image_tag.short_description = 'Current profile picture'
	

	class Meta:
		ordering = ["artistic_name"]
		verbose_name = 'Album artist'
		verbose_name_plural = "Album artists"


class Genre(models.Model):
	"""Musical genre Model"""
	parent = models.ForeignKey('self', null = True, blank=True,related_name = 'sub_genre', default = None, on_delete=models.CASCADE)	
	author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = 'Uploaded by',related_name = 'author_genre', blank = True,null=True,default=None,on_delete=models.SET_NULL)
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	name = models.CharField('Name', max_length = 200, blank = False, null = False )
	slug = models.SlugField('Slug', max_length = 150, unique = True, editable = False)
	description = models.TextField('Description', blank = True, null = True, default = None ) 

	def __str__(self):
		"""Get human-readable representation"""				
		return self.name
	
	@property
	def is_top_level(self):
		"""Check if genre is a main genre"""
		return bool(self.parent)

	def main_genre(self):
		return bool(not self.parent)

	main_genre.short_description = 'Main musical Genre'


	def save(self, *args, **kwargs):
		"""Generate the slug based on genre name on first save and modify created_at and updated_at"""
		if not self.id:
			# Newly created object, so set slug and created_at
			self.slug = slugify(self.name)
			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Genre, self).save(*args, **kwargs)


	class Meta:
		ordering = ["name"]
		verbose_name = 'Album genre'
		verbose_name_plural = "Album genres"


class Album(models.Model):
	"""Album model"""
	title = models.CharField('Name', max_length = 200, blank = False, null = False )
	slug = models.SlugField('Slug', max_length = 150, unique = True, editable = False)
	lauch_date = models.DateTimeField('Lauch date', null = False)
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = 'Uploaded by',related_name = 'album_author', blank = True,null = True,default = None,on_delete=models.SET_NULL)
	artist = models.ManyToManyField(Artist)
	genre = models.ManyToManyField(Genre)
	cover = models.ImageField(upload_to = 'albums/', max_length=500, blank = True, null = True)
	quantity = models.IntegerField('Quantity in stock', default = 0)
	price = models.FloatField('Price', default = 0.0)
	total_sales = models.FloatField('Total sales', default = 0.0)
	
	def __str__(self):
		"""Get human-readable representation"""			
		return self.title

	@property
	def score(self):
		total = Score.objects.filter(album = self.id)
		stars_average = total.aggregate(Avg('score'))
		try:
			avarage = int(stars_average['score__avg'])
		except TypeError as e:
			avarage = 0
		return avarage

	def save(self, *args, **kwargs):
		"""Generate the slug based on album title on first save and modify created_at and updated_at"""
		if not self.id:
			# Newly created object, so set slug and created_at
			self.slug = slugify(self.title)
			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Album, self).save(*args, **kwargs)

	def image_tag(self):
		"""Set the image on edit view"""
		if self.pk is not None:
			if self.cover:
				return mark_safe('<img style="width:100px;height:auto" src="%s">' % self.cover.url)

	image_tag.allow_tags = True
	image_tag.short_description = 'Current cover picture'

class Score(models.Model):
	"""Score model for Albums"""
	album = models.ForeignKey(Album, related_name = 'rating_album', on_delete = models.CASCADE)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'rating_author')
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	score = models.IntegerField(choices = SCORE_CHOICES, default = 0)

	class Meta:
		verbose_name = 'Album Score'
		verbose_name_plural = 'Albums scores'
		unique_together = ('album', 'author')
		indexes = [
			models.Index(fields=['album'])
		]

	def save(self, *args, **kwargs):
		"""Set created at on save and updated at on update"""
		if not self.id:
			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Score, self).save(*args, **kwargs)

class Comment(models.Model):
	""" Model Comment for each album"""
	album = models.ForeignKey(Album, related_name = 'comments')
	created_at = models.DateTimeField('Created at ',auto_now_add = True)
	updated_at = models.DateTimeField('Updated at ',auto_now = True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = 'Written by',related_name = 'comment_author', blank = True)
	text = models.TextField('Text', null = False, blank = False)

	def save(self, *args, **kwargs):
		"""Set created at on save and updated at on update"""
		if not self.id:

			self.created_at = timezone.now()
		else:
			self.updated_at = timezone.now()

		super(Comment, self).save(*args, **kwargs)


