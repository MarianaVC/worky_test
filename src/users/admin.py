from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
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

admin.site.register(User, UserAdmin)