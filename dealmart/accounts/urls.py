from django.conf.urls import url
from . import views
from django.conf import settings
from rest_framework.routers import DefaultRouter
from django.urls import include
from django.conf.urls.static import static

from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register(r'daddress', views.DeliveryAddressView)
router.register(r'paddress',views.PickupAddressView)
router.register(r'sdetail',views.SellerDetailsView)
router.register(r'product',views.ProductView)
router.register(r'order',views.OrderView)
# router.register(r'order/(?P<product_id>[0-9]+)',views.OrderView)
router.register(r'payment',views.PaymentView)
# router.register(r'feedback',views.FeedbackView)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/role/$',views.RoleView.as_view()),
    url(r'^api/signup/$', views.SignUp.as_view()),
    url(r'^api/activate/(?P<user_id>[0-9]+)/$', views.Activate.as_view(), name='activate'),
    url(r'^api/resendotp/(?P<user_id>[0-9]+)/$',views.ResendOtp.as_view(), name='resend-otp'),
    url(r'^api/login/$',views.Login.as_view(), name='login'),
    url(r'^api/logout/$',views.Logout.as_view(), name='logout'),
    url(r'^api/cart/$',views.CartView.as_view()),
    url(r'^api/cart/(?P<product_id>[0-9]+)/$',views.AddOrRemoveToCartView.as_view()),
    url(r'^api/category/$',views.CategoryView.as_view()),
    # url(r'^api/rating/(?P<product_id>[0-9]+)/$',views.RatingView.as_view()),
    url(r'^api/(?P<category>[0-9 a-z A-Z]+)/$',views.SubcategoryView.as_view()),
    url(r'^api/(?P<category>[0-9 a-z A-Z]+)/(?P<subcategory>[0-9 a-z A-Z]+)/$',views.SubSubcategoryView.as_view()),
    url(r'^docs/', include_docs_urls(title='My API title'))
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)