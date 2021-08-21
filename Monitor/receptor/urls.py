from django.urls import path
from django.conf.urls import url
from .views import recive_data, show_data

app_name = "receptor"

urlpatterns = [
    url(r'^(?P<id>[a-zA-Z0-9]+)/$', recive_data, name="recive"),
    url(r'^$', show_data, name="list_pacients"),
]