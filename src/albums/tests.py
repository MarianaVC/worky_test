from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from users.models import User
# Create your tests here.

from .models import *

class ArtistTestCase(TestCase):
	"""Model test case for Artist"""
	
	def setUp(self):		
		self.artistic_name = "Justin Timberlake"
		self.original_name = "Justin Randall Timberlake"
		self.artist = Artist(artistic_name = self.artistic_name, original_name = self.original_name)
	
	def test_model_can_create_an_artist(self):
		"""Test can create an artist."""
		old_count = Artist.objects.count()
		self.artist.save()
		new_count = Artist.objects.count()
		self.assertNotEqual(old_count, new_count)


class GenreTestCase(TestCase):
	""" Model test case for Genre"""

	def setUp(self):
		self.name = 'Rock'
		self.description = "Super cool genre"
		self.genre = Genre(name = self.name, description = self.description)

	def test_model_can_create_genre(self):
		"""Test can create a gerne with minimun required fields"""	
		old_count = Genre.objects.count()
		self.genre.save()
		new_count = Genre.objects.count()
		self.assertNotEqual(old_count, new_count)

class AlbumTestCase(TestCase):
	""" Model test case for Album"""
	
	def setUp(self):
		self.title = "Super album"
		self.lauch_date = timezone.now()
		self.album = Album(
				title = self.title,
				lauch_date = self.lauch_date,
			)

	def test_model_can_create_album(self):
		"""Test album can be created"""
		old_count = Album.objects.count()
		self.album.save()
		new_count = Album.objects.count()
		self.assertNotEqual(old_count, new_count)

class ScoreTestCase(TestCase):
	""" Model test case for Score """
	def setUp(self):
		self.album = Album.objects.create(
				title =  "Super album",
				lauch_date = timezone.now(),
			)
		self.author = User.objects.create(
					username='foo', email='foo@bar', 
					password='bar'
			)
		self.grade = 5
		self.score = Score(score = self.grade, author = self.author, album = self.album)

	def test_model_can_create_score(self):
		"""Test we can add scores to albums"""
		old_count = Score.objects.count()
		self.score.save()
		new_count = Score.objects.count()
		self.assertNotEqual(old_count, new_count)			

class CommentTestCase(TestCase):
	""" Model test case for Comment model"""

	def setUp(self):
		self.album = Album.objects.create(
				title =  "Super album",
				lauch_date = timezone.now(),
			)
		self.author = User.objects.create(
					username='foo', email='foo@bar', 
					password='bar'
			)		
		self.text = "This is a super cool album"
		self.comment = Comment(text = self.text, album = self.album, author = self.author)

	def test_model_can_create_a_comment(self):
		"""Test we can create comments"""
		old_count = Comment.objects.count()
		self.comment.save()
		new_count = Comment.objects.count()
		self.assertNotEqual(old_count, new_count)

		