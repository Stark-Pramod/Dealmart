from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.SignUp.as_view({'post':'post','get':'list'}),name='signup'),
    ]