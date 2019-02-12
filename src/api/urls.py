# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_simplejwt import views as jwt_views


urlpatterns = {
    url(r'^$', api_root),
    url(r'api/token/$', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'api/token/refresh/$', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
	url(r'^users/$', UserListView.as_view(), name="users"),
	url(r'^comments/$', CommentCreateView.as_view(), name="comments"),
	url(r'^orders/albums/(?P<pk>[0-9]+)/$', AlbumOrdersListView.as_view(), name="album_orders"),
	url(r'^sales/albums/(?P<pk>[0-9]+)/$', AlbumDetailView.as_view(), name="album_detail"),		
	url(r'^orders/$', order, name="orders"),
	url(r'^albums/$', AlbumListView.as_view(), name="albums"),
	url(r'^scores/$', ScoreCreateListView.as_view(), name="scores"),
	url(r'^comments/(?P<pk>[0-9]+)/$', CommentDetailsView.as_view(), name="comment_detail"),
}

urlpatterns = format_suffix_patterns(urlpatterns)