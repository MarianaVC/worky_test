from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""
	
	class Meta:
		"""Map serializer's fields with model fields"""
		model = User
		partial = True
		fields = '__all__'		
		read_only_fields = ('updated_at','facebook_id')

class MinUserSerializer(serializers.ModelSerializer):
	"""Minified User Serializer to map model to JSON format"""
	
	class Meta:
		"""Map serializer's fields with model fields"""
		model = User
		partial = True
		fields = ('email','first_name','last_name','phone','username','profile_image')		

class OrderItemSerializer(serializers.ModelSerializer):
	"""Order Serializer to map model to JSON format"""
	def validate(self, data):
		"""
		Check quantity is > 0
		"""
		if data['quantity'] <= 0 :
			raise serializers.ValidationError("Quantity must be greater than 0")
		return data

	class Meta:
		"""Order Serializer to map model to JSON format"""
		model = OrderItem
		partial = True
		fields = ('order','album','quantity','total')
		read_only_fields = ('order','total')

class OrderSerializer(serializers.ModelSerializer):
	"""Order Serializer to map model to JSON format"""
	
	class Meta:

		"""Order Serializer to map model to JSON format"""
		model = Order
		partial = True
		fields = ('user','created_at','updated_at','status','total_payed')
		read_only_fields = ('created_at','user','updated','total_payed','status')


