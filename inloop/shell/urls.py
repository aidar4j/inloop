from django.conf.urls import url

from inloop.shell import views

app_name = "shell"
urlpatterns = [
    url(r'^$', views.shell_view, name='shell_view'),
]
