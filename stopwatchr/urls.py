from django.urls import path
from stopwatchr import views 
 
urlpatterns = [
    path('api/users', views.users_list),
    path('api/users/<int:pk>', views.users_detail),
    path('api/login', views.user_login),
    path('api/stocks', views.stocks_list)
]
