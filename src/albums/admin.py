from django.contrib import admin
from .models import *
from .forms import AlbumForm
from django.db.models import Sum, Count, Avg

# Register your models here.

class ArtistAdmin(admin.ModelAdmin):
	fields = ('artistic_name','original_name','slug','profile_picture','image_tag','author','created_at','updated_at')
	readonly_fields = ('created_at','updated_at','author','slug','image_tag')
	list_display = ('artistic_name','slug','created_at')
	list_filter = ('created_at','author')
	search_fields = ['artistic_name']

	def save_model(self, request, obj, form, change):
		#Save author relation on first save
		if not obj.id:
			obj.author = request.user
			obj.save()
		else:
			obj.save()

class GenreAdmin(admin.ModelAdmin):
	fields = ('parent','main_genre','name','slug','description','author','created_at','updated_at')
	readonly_fields = ('author','created_at','updated_at','slug','main_genre')
	list_display = ('name','slug','created_at')
	list_filter = ('created_at','parent')
	search_fields = ['name']

	def save_model(self, request, obj, form, change):
		#Save author relation on first save
		if not obj.id:
			obj.author = request.user
			obj.save()
		else:
			obj.save()

class AlbumAdmin(admin.ModelAdmin):
	fields = ('title','slug','lauch_date','artist','genre','cover','image_tag','author','created_at','updated_at','quantity','price','total_sales')
	readonly_fields = ('slug', 'created_at','updated_at','author','image_tag')
	list_display = ('title','slug','lauch_date','image_tag','get_avarage')
	list_filter = ('artist','genre','author')
	search_fields = ('title','artist','genre')
	form = AlbumForm

	def save_model(self, request, obj, form, change):
		#Save author relation on first save
		if not obj.id:
			obj.author = request.user
			obj.save()
		else:
			obj.save()

	def get_avarage(self, obj):
		"""Get avarage on list view"""
		total = Score.objects.filter(album_id = obj.id).annotate(Count('album_id')).aggregate(Avg('score'))			
		return total
	
	get_avarage.short_description = "User's grades avarage"

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Album, AlbumAdmin)