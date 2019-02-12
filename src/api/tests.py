from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from albums.models import *
from users.models import User
import json
# Create your tests here.

class ArtistViewTestCase(TestCase):
	"""Test suite for Artist api views."""
	pass	

class GenreViewTestCase(TestCase):
	"""Test suite for Genre api views."""
	
	pass

class AlbumViewTestCase(TestCase):
	"""Test suite for Album api views."""
	def setUp(self):
		### obtain jwt bearer token with admin credentials
		self.admin = User.objects.create_superuser(
					username='foo', email='foo@bar', 
					password='bar'
			)
		self.client = APIClient()
		self.auth = self.client.post(
			reverse('token_obtain_pair'),{'username':'foo','password':'bar'},format="json")	
		self.bearer = json.loads(self.auth.content.decode('utf-8'))['access']
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.bearer)
		self.data = {'title':'New Album','launch_date':'1979-01-01'}
	
	def test_api_can_create_album(self):
		"""Test we can create an album with admin auth"""
		self.response = self.client.post(
			reverse('albums'),
			self.data,
			format="json")		

class ScoreViewTestCase(TestCase):
	"""Test suite for Score api views."""
	
	pass

class UserViewTestCase(TestCase):
	"""Test suite for User api vies"""
	def setUp(self):
		pass
		

class CommentViewTestCase(TestCase):
	"""Test suite for Comment api views."""
	
	def setUp(self):
		self.client = APIClient()
		self.album = Album.objects.create(
				title =  "Super album",
				lauch_date = timezone.now(),			
			)
		self.author_1 = User.objects.create(
					username='foo', 
					email='foo@bar', 
					password='bar'
			)
		
		self.author_2 = User.objects.create(
					username='foo2', 
					email='foo2@bar', 
					password='bar2'
			)

		self.parent_comment_data = {
			'text':'This is a super cool album',
			'album':self.album.id, 
			'author':self.author_1.id
			}
		
		self.response_1 = self.client.post(
			reverse('comments'),
			self.parent_comment_data,
			format="json")

		self.parent_comment = Comment.objects.create(
			text = 'Super cool album',
			author = self.author_1,
			album = self.album			
		)
		
		self.nested_comment_data = {
			'text':'You are right', 
			'album':self.album.id, 
			'author':self.author_2.id, 
			'parent': self.parent_comment.id
			}		

		self.response_2 = self.client.post(
			reverse('comments'),
			self.nested_comment_data,
			format="json")

	def test_api_can_create_a_comment(self):
		"""Test we can comment an album via API"""
		self.assertEqual(self.response_1.status_code, status.HTTP_201_CREATED)

	def test_api_can_create_a_nested_comment(self):
		"""Test we can answer a comment via API"""
		self.assertEqual(self.response_2.status_code, status.HTTP_201_CREATED)

	def test_api_can_get_a_comment(self):
		"""Test we can retrive comment detail"""
		response = self.client.get(
			reverse('comment_detail',
			kwargs={'pk': self.parent_comment.id}), format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertContains(response, self.parent_comment.id)

	def test_api_can_update_a_comment(self):
		"""Test the api can update a given comment."""
		change_comment = {'text': 'Something new'}
		response = self.client.patch(
			reverse('comment_detail', kwargs={'pk': self.parent_comment.id}),
			change_comment, format='json'
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_api_can_delete_a_comment(self):
		"""Test the api can delete a given comment"""
		response = self.client.delete(
			reverse('comment_detail', kwargs={'pk': self.parent_comment.id}),
			format='json',
			follow=True)
		
		self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)		

