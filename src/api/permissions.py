from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
	"""Override IsAdminOrReadOnly so  users retrieve data with safe methods but can't post, put or patch content"""
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		else:
			return request.user.is_staff

class IsAuthenticated(BasePermission):
	"""Override IsAuthenticated so users can retrive data with safe methods but can't post, put, or path content unless they
	are authentcated
	 """
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		else:
			return request.user and request.user.is_authenticated
