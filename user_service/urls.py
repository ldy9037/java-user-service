from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
import user.views
import certification.views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('user/', user.views.insert_users, name='insert-users'),
    path('count/<str:value>', user.views.count_users, name='count-users'),
    path('cert/', certification.views.request_certification_number, name='request-certification-number')
]
