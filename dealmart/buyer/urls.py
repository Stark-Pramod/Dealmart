from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.SignUp.as_view(), name='signup'),
    url(r'^activate/$', views.Activate.as_view(), name='activate'),
    ]