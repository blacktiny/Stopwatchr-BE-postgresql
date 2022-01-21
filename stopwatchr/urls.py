from django.urls import path
from django.urls.conf import include
from stopwatchr import views 
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('devices', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users', views.users_list),
    path('api/users/<int:pk>', views.users_detail),
    path('api/login', views.user_login),
    path('api/stocks', views.stocks_list),
    path('api/alerts', views.alerts_list)
]
