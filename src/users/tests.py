from django.test import TestCase
from django.utils import timezone
from django.conf import settings
from .models import User, Order, OrderItem
from albums.models import Album
# Create your tests here.

class UserTestCase(TestCase):
	"""Model test case for user"""
	def setUp(self):
		self.email = 'foo@bar'
		self.first_name = 'foo'
		self.last_name = 'foo-foo-foo'
		self.middle_name = 'foo-foo'
		self.phone = '55555555'
		self.username = 'foo'
		self.password = 'bar'
		self.user = User(
			email = self.email,
			first_name = self.first_name,
			last_name = self.last_name,
			middle_name = self.middle_name,
			phone = self.phone,
			username = self.username,
			password = self.password
			)

	def test_model_can_create_user(self):
		"""Test can create a user."""		
		old_count = User.objects.count()
		self.user.save()
		new_count = User.objects.count()
		self.assertNotEqual(old_count, new_count)

class OderTestCase(TestCase):
	"""Model test case for user"""
	def setUp(self):
		self.user = User.objects.create(
			username='foo', 
			email='foo@bar', 
			password='bar'
			)
		self.total_payed = 0.0
		
		self.album = Album.objects.create(
				title =  "Super album",
				lauch_date = timezone.now(),			
			)		


		self.order = Order(
				user = self.user,
				total_payed = self.total_payed
			)

	def test_model_can_create_order(self):
		"""Test we can create an order"""
		old_count = Order.objects.count()
		self.order.save()
		new_count = Order.objects.count()
		self.assertNotEqual(old_count, new_count)

	def test_model_can_add_item_to_order(self):
		"""Test we can add items to orders"""
		self.order.save()
		self.item = OrderItem(
			order = self.order,
			album = self.album,
			quantity = 3,
			total = 45.00
			)
		old_count = OrderItem.objects.count()
		self.item.save()
		new_count = OrderItem.objects.count()
		self.assertNotEqual(old_count, new_count)		
		self.assertEqual(self.item.order.id, self.order.id)


