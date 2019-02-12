from ajax_select import register, LookupChannel
from django.db.models import Q # for making more complex querys with Or statements
from .models import Artist,Genre, Album

@register('artist')
class ArtistLookup(LookupChannel):
	"""Search artist by artistc name or original name"""
	model = Artist
	min_length = 3
	min_length = 3
	def get_query(self, q, request):
		return self.model.objects.filter( Q(original_name__icontains=q) | Q(artistic_name__icontains=q))
	
	def format_item_display(self, item):
		return u"<span class='tag'>{0}</span>".format(item.artistic_name)

@register('genre')
class MusicalGenreLookup(LookupChannel):
	"""Search Musical genre by name"""
	model = Genre
	min_length = 3
	max_length = 3
	def get_query(self, q, request):
		return self.model.objects.filter( Q(name__icontains=q))
	def format_item_display(self, item):
		return u"<span class='tag'>{0}</span>".format(item.name)	

