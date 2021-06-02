from django.conf.urls import url 
from stopwatchr import views 
 
urlpatterns = [ 
    url(r'^api/users$', views.users_list),
    url(r'^api/users/(?P<pk>[0-9]+)$', views.users_detail),
    url(r'^api/login$', views.user_login),
    url(r'^api/stocks$', views.stocks_list),
    url(r'^api/stocks/(?P<pk>[0-9]+)$', views.stocks_detail),
]
