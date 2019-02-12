from django.shortcuts import render
from rest_framework import generics
from albums.serializers import *
from albums.models import *
from users.models import *
from users.serializers import *
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly, IsAuthenticated
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.views.defaults import bad_request
from rest_framework import status
from django.core import serializers
import json

@api_view(['GET'])
def api_root(request, format=None):
	"""Worky API root"""
	return Response({
		'comments/': reverse('comments', request=request, format=format),
		'albums/': reverse('albums', request=request, format=format),
		'scores/': reverse('scores', request=request, format=format),
		'comments/{{pk}}': reverse('comment_detail', request=request, format=format,kwargs={'pk': 1}),
		'users/': reverse('users', request=request, format=format),
		'api/token/':reverse('token_obtain_pair', request=request, format=format),
		'api/token/refresh/': reverse('token_refresh', request=request, format=format),
	})

#=====Comments=====#

class CommentCreateView(generics.ListCreateAPIView):
	"""Define list and post behavior of our rest api, only allow authenticated users"""
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = (IsAuthenticated,)	
	
	def handle_exception(self, exc):
		"""
		Handle any exception that occurs, by returning an appropriate
		response,or re-raising the error.
		"""
		return Response({'error':'bad request'}, status= status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		"""Save the post data when creating a new comment."""
		serializer.save(author=self.request.user)


#=====Albums=====#
class AlbumListView(generics.ListCreateAPIView):
	"""List All albums by genre with comments and score"""
	serializer_class = AlbumListSerializer
	genre = GenreSerializer(read_only=True)
	comments = CommentSerializer(read_only = True)
	permission_classes = (IsAdminOrReadOnly, )

	def get_queryset(self):
		"""
		Optionally restricts the return albums by genre,
		by filtering against a `genre` query parameter in the URL.
		"""
		queryset = Album.objects.all()
		genre = self.request.query_params.get('genre', None)
		if genre is not None:
			genre_id = Genre.objects.get(name=genre).id
			queryset = queryset.filter(genre=genre_id)
		return queryset
	
	def perform_create(self, serializer):
		"""Save the post data when creating a new comment. Only staff menbers can add albums"""
		serializer.save()

class AlbumDetailView(generics.RetrieveAPIView):	
	"""Total sales per album"""
	serializer_class = MinAlbumSerializer
	#permission_classes = (IsAdminOrReadOnly, )	
	def get_queryset(self):
		queryset = Album.objects.all()
		pk = self.kwargs['pk']
		queryset =  Album.objects.filter(pk = pk)
		return queryset

class CommentDetailsView(generics.RetrieveUpdateDestroyAPIView):
	"""Handles the http GET, PUT and DELETE requests for comments"""

	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

#=====User=====#

class UserListView(generics.ListAPIView):
	"""Define create user behavior of api, users can only be created by staff"""	
	queryset = User.objects.all()
	serializer_class = UserSerializer
	#permission_classes = (IsAdminOrReadOnly, )

	#def perform_create(self, serializer):
		#"""Save the post data when creating a new user."""
		#serializer.save()	
		
#=====Scores=====#

class ScoreCreateListView(generics.ListCreateAPIView):
	queryset = Score.objects.all()
	serializer_class = ScoreSerializer
	permission_classes = (IsAuthenticated,)	

	def handle_exception(self, exc):
		"""
		Handle any exception that occurs, by returning an appropriate
		response,or re-raising the error.
		"""
		return Response({'error':'bad request'}, status= status.HTTP_400_BAD_REQUEST)

	def perform_create(self, serializer):
		"""Save the post data when creating a new user."""
		serializer.save(author=self.request.user)

#=====Orders=====#
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order(request):
	"""Post an order only for authenticated users"""
	serialized = OrderItemSerializer(data=request.data, many = True)
	if serialized.is_valid():
		order = Order.objects.create(
			user = request.user
			)
		
		serialized.save(order=order)
		order = Order.objects.get(id=order.id) # retrive object again so we can have total_payed updated
		serialized_order = json.loads(serializers.serialize('json', [ order, ]))[0]["fields"]
		return Response(serialized_order, status=status.HTTP_201_CREATED)
	return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersListView(generics.ListAPIView):
	"""Define list behavior for model Orders"""
	pass	

class AlbumOrdersListView(generics.ListAPIView):
	"""Define lis behavior for model Orders filtering by album"""
	serializer_class = ItemSerializer
	queryset = OrderItem.objects.all()
	def get_queryset(self):
		album = self.kwargs['pk']
		queryset =  OrderItem.objects.filter(album_id = album)
		return queryset

