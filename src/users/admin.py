from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.utils.translation import gettext, gettext_lazy as _

class UserAdmin(UserAdmin):
	list_display = ('first_name', 'last_name', 'email')
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone','facebook_id','profile_image','gender')}),
		(_('Permissions'), {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		(_('Important dates'), {'fields': ('last_login',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2'),
		}),
	)

	read_only_fields = ['facebook_id']

class OrderItemInline(admin.StackedInline):
	model = OrderItem
	extra = 0
	max_num = 100
	fields = ('album','quantity','total')
	readonly_fields = ('total',)
	
	def total(self,obj):
		album_price = Album.objects.get(pk = obj.album.id).price
		total = obj.quantity * album_price
		return total	
	
	total.short_description = "Total quantity paid per album"

class OrderAdmin(admin.ModelAdmin):
	fields = ('user','created_at','updated_at','status','total_payed')
	list_display = ('user','created_at', 'status', 'total_payed')
	readonly_fields = ('created_at','updated_at','user','total_payed')
	list_filter = ('user','status')
	search_fields = ('status','user')
	inlines = [OrderItemInline]

admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)	