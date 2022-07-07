from django.contrib import admin
from django.conf.urls import url,include
from rest_framework import routers
from user.views import UserViewSet

router = routers.DefaultRouter()
router.register('user',  UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
]
