from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register('user',  UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls), name='index'),
]
