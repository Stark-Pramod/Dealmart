from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'daddress', views.DeliveryAddressView)
router.register(r'paddress',views.PickupAddressView)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/signup/$', views.SignUp.as_view()),
    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^api/login/$',views.Login.as_view(), name='login'),
    url(r'^api/logout/$',views.Logout.as_view(), name='logout'),
    url(r'^api/docs/', include_docs_urls(title='My API title'))
    ]