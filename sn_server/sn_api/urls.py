from django.conf.urls import include, url
from rest_framework import routers

from .views import UserViewset, GroupViewset, UserProfile, \
    GroupManagement, GroupMembership, UserFriendship

api_router = routers.SimpleRouter()

api_router.register(r'allusers', UserViewset, basename='allusers')
api_router.register(r'allgroups', GroupViewset, basename='allgroups')

urlpatterns = [
    url(r'', include(api_router.urls)),
    url(r'auth/registration/', include('rest_auth.registration.urls')),
    url(r'auth/', include('rest_auth.urls')),
    url(
        r'group/(?P<group_id>\d)/membership', 
        GroupMembership.as_view()
    ),
    url(r'group/(?:/(?P<group_id>\d)/)?', GroupManagement.as_view()),
    url(
        r'user/(?P<friend>\d)/friendship/', 
        UserFriendship.as_view()
    ),
    url(r'user/(?P<user_id>\d)/', UserProfile.as_view()),
]