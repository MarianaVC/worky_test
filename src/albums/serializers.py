from rest_framework import serializers
from .models import *
from users.serializers import *
from rest_framework.validators import UniqueTogetherValidator


def required(value):
	if value is None:
		raise serializers.ValidationError('This field is required')	

class ArtistSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""
	
	class Meta:
		"""Map serializer's fields with model fields"""
		model = Artist
		fields = ('artistic_name','slug','profile_picture')
		read_only_fields = ['slug']

class CommentSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""
	class Meta:
		"""Map serializer's fields with model fields"""
		model = Comment
		partial = True
		fields = ('author','text','id','album')
		read_only_fields = ('author','id')

class GenreSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""
	class Meta:
		"""Map serializer's fields with model fields"""
		model = Genre
		fields = ('name', 'slug')
		read_only_fields = ['slug']
	
	def get_fields(self):
		fields = super(GenreSerializer, self).get_fields()
		fields['parent'] = GenreSerializer()
		return fields

class AlbumListSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""
	genre = GenreSerializer(many=True, read_only = True)
	artist = ArtistSerializer(many=True, read_only = True)
	comments = CommentSerializer(many=True, read_only = True)
	score = serializers.CharField()

	class Meta:
		"""Map serializer's fields with model fields"""
		partial = True
		fields = ('title','slug','lauch_date','artist','genre','cover','quantity','price', 'comments', 'score')
		model = Album
		read_only_fields = ('author','slug','score')


class MinAlbumSerializer(serializers.ModelSerializer):
	"""Min Serializer to map model to JSON format"""
	
	class Meta:
		"""Map serializer's fields with model fields"""
		partial = True
		fields = ('title','slug','cover','quantity','price','total_sales')
		model = Album
		read_only_fields = ('created_at','updated_at','author','slug')

class ScoreSerializer(serializers.ModelSerializer):
	"""Serializer to map model to JSON format"""

	author = MinUserSerializer(read_only = True)

	class Meta:
		"""Map serializer's fields with model fields"""
		fields = ('album','author','created_at','score')
		model = Score
		read_only_fields = ('created_at','updated_at')
		extra_kwargs = {'album_id': {'required':True}, 'score':{'required':True}} 
	

class ItemSerializer(serializers.ModelSerializer):
	"""Order Item serializer to map model to json"""
	album = MinAlbumSerializer(read_only = True)
	total = serializers.CharField()

	class Meta:
		"""Order Serializer to map model to JSON format"""
		model = OrderItem
		partial = True
		fields = ('order','album','quantity','total')
		read_only_fields = ('order','total')


	
