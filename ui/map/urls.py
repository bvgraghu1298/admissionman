from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^map/index/',views.index,name='index'),
    url(r'^map/data/', views.data, name='data')
]
