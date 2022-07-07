from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', views.list_insert_users, name='list_insert_users'),
]
