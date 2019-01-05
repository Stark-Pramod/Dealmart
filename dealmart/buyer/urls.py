from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.SignUp.as_view(), name='signup'),
    url(r'^activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'login/$',views.Login.as_view(), name='login'),
    url(r'logout/$',views.Logout.as_view(), name='logout'),
    url(r'address/$',views.AddressView.as_view(),name='address'),
    url(r'address/(?P<ad_id>[0-9]+)/$',views.AddressUpdate.as_view(), name='address_update')
    ]