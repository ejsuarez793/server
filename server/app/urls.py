# urls.py
from django.conf.urls import url
from app.views.viewsV import ClienteList, ClienteDetail


urlpatterns = [
    url(r'^clientes/$', ClienteList.as_view()),
    url(r'^clientes/(?P<pk>\d+)$', ClienteDetail.as_view()),
]
