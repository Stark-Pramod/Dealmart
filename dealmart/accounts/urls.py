from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import include
# from snippets import views
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'address', views.AddressView)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/buyer/signup/$', views.BuyerSignUp.as_view()),
    # url(r'api/seller/signup/$', views.SellerSignUp.as_view()),
    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^api/login/$',views.Login.as_view(), name='login'),
    url(r'^api/logout/$',views.Logout.as_view(), name='logout'),
    url(r'^api/docs/', include_docs_urls(title='My API title'))
    ]