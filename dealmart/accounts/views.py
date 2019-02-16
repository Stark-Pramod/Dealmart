from .serializers import *
from .permissions import *
from django.db.models import Q
from .backends import EmailOrUsername
from rest_framework.response import Response
from django.contrib.auth import get_user_model
User=get_user_model()
import django_filters.rest_framework
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status,filters
from rest_framework import generics,viewsets,mixins
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.core.mail import send_mail
from dealmart.settings import EMAIL_HOST_USER
from random import *
from rest_framework import permissions
from .models import OTP
from django.contrib.auth import login,logout
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import action

# Create your views here.

class SignUp(APIView):
    """
    List all user, or create a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = User.objects.create_user(username=username,email=email,password=password)
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver=user)
        data.save()
        user.is_active = False
        user.save()
        subject = 'Activate Your Dealmart Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
         })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': username+',Please confirm your email to complete registration.',
                                'user_id': user.id })


class Activate(APIView):
    """
    Activate verifies the stored otp and the otp entered by user.
    """
    permission_classes = (permissions.AllowAny,IsNotActive)
    serializer_class = OTPSerializer

    def post(self,request,user_id,*args,**kwargs):
        code = OTPSerializer(data=request.data)
        code.is_valid(raise_exception=True)
        code = code.validated_data['otp']
        try:
            otp = OTP.objects.get(receiver=user_id)
        except(TypeError, ValueError, OverflowError, OTP.DoesNotExist):
                otp = None
        try:
            receiver = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            receiver = None
        if otp is None or receiver is None:
            return Response({'error':'you are not a valid user'},status=status.HTTP_400_BAD_REQUEST)

        elif timezone.now() - otp.sent_on >= timedelta(days=0,hours=0,minutes=2,seconds=0):
            otp.delete()
            return Response({'detail':'OTP expired!',
                                 'user_id':user_id})

        if otp.otp == code:
            receiver.is_active = True
            receiver.save()
            buyer = Role.objects.get(role='Buyer')
            receiver.roles.add(buyer)
            # Cart.objects.create(user=receiver)
            # login(request, receiver)
            otp.delete()
            return Response({'message': 'Thank you for Email Verification you are successfully logged in'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid OTP',},status = status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class ResendOtp(generics.CreateAPIView):
    """
    views for resend the otp.
    """
    serializer_class = OTPSerializer
    permission_classes = (permissions.AllowAny,IsNotActive)

    def get(self,request,user_id,*args,**kwargs):
        try:
            user = User.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None:
            return Response({'error':'Not a valid user!'})
        otp = OTP.objects.filter(receiver=user)
        if otp:
            otp.delete()
        otp = randint(100000, 1000000)
        data = OTP.objects.create(otp=otp,receiver= user)
        data.save()
        subject = 'Activate Your Dealmart Account'
        message = render_to_string('account_activate.html', {
            'user': user,
            'OTP': otp,
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        return Response({'details': user.username +',Please confirm your email to complete registration.',
                         'user_id': user_id },
                        status=status.HTTP_201_CREATED)

class Login(APIView):
    """
    the user can login either with email or username. EmailOrUsername is the function for it.
    """

    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self,request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uname_or_em = serializer.validated_data['uname_or_em']
        password = serializer.validated_data['password']
        user = EmailOrUsername(self,uname_or_em = uname_or_em,password=password)

        if user == 2:
            return Response({'error':'Invalid Username or Email!!'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        elif user == 3:
            return Response({'error':'Incorrect Password'},
                                status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            if user.is_active:
                login(request, user)
                return Response({'detail':'successfully Logged in!','user_id': user.id,
                                 'username':user.username},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error':'Please! varify Your Email First','user_id':user.id},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)


class Logout(APIView):
    """
    logout view.Only authenticated user can access this url(by default)

    """
    def get(self,request,*args,**kwargs):
        logout(request)
        return Response({'message':'successfully logged out'},
                        status=status.HTTP_200_OK)


class RoleView(generics.ListCreateAPIView):
    """
    view to create the different Role.
    """
    permission_classes = (permissions.IsAuthenticated,IsAdmin)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            role = serializer.validated_data['role']
            serializer.save(role=role)
            return Response({'details':'role created'})
        return Response({'error':'some error occured'})



class DeliveryAddressView(viewsets.ModelViewSet):
    """
    DeliveryAddress view for storing delivery address of buyer.
    """
    serializer_class = DeliveryAddressSerializer
    queryset = DeliveryAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsBuyer)
    lookup_url_kwarg = 'ad_id'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        add = DeliveryAddress.objects.filter(user=request.user)
        serializer = DeliveryAddressSerializer(data=add,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class PickupAddressView(viewsets.ModelViewSet):
    """
    PickupAddress view for storing pickup address of seller.
    """
    serializer_class = PickupAddressSerializer
    queryset = PickupAddress.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner, IsSeller)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        add = PickupAddress.objects.filter(user=request.user)
        serializer = PickupAddressSerializer(data=add,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class SellerDetailsView(viewsets.ModelViewSet):
    """
      seller detail view for storing bank details and tax related info of seller.
    """
    serializer_class = SellerDetailsSerializer
    queryset = SellerDetails.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def perform_create(self, serializer):
        if SellerDetails.objects.filter(user=self.request.user):
            raise ValidationError("you are not allowed to add more than one detail set")
        user = self.request.user
        seller = Role.objects.get(role='Seller')
        user.roles.add(seller)
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        add = SellerDetails.objects.filter(user=request.user)
        serializer = SellerDetailsSerializer(data=add,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,DjangoFilterBackend)
    search_fields = ('name','category__category','subcategory__subcategory','subsubcategory__subsubcategory')
    filter_fields = ('category__category', 'subcategory__subcategory','subsubcategory__subsubcategory')


    def get_serializer_class(self):
        if self.action == 'submit_feedback':
            return FeedbackSerializer
        elif self.action == 'submit_rating':
            return RatingSerializer
        elif self.action == 'list':
            return ListProductSerializer
        else:
            return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['GET'],detail=True)
    def feedback(self,*args,**kwargs):
        product = self.kwargs['pk']
        feedback_list = Feedback.objects.filter(product=product)
        serializer = FeedbackSerializer(data=feedback_list,many=True)
        serializer.is_valid()
        return Response(serializer.data)

    @action(methods=['POST'],detail=True)
    def submit_feedback(self,*args,**kwargs):
        product = self.kwargs['pk']
        feedback = FeedbackSerializer(data=self.request.data)
        feedback.is_valid()
        feedback.save(user=self.request.user,product_id=product)
        return Response(feedback.data)

    @action(methods=['get'],detail=True)
    def rating(self,*args,**kwargs):
        product_id = self.kwargs['pk']
        all_rating = Rating.objects.all()
        total_rating = all_rating.count()
        avg_rating = 0
        rating_count = 0
        for rate in all_rating:
            rating_count += rate.star
        avg_rating = rating_count/(total_rating+1)
        if not self.request.user.is_anonymous:
            try:
                rated = Rating.objects.get(user=self.request.user,product=product_id)
            except (Rating.DoesNotExist):
                rated =None
            if rated is None:
                return Response({'status':False,'avg_rating':avg_rating})
            return Response({'status':True,'avg_rating':avg_rating})
        else:
            return Response({'avg_rating':avg_rating})

    @action(methods=['POST'],detail=True)
    def submit_rating(self,request,*args,**kwargs):
        product_id = self.kwargs['pk']
        product = Product.objects.get(id=product_id)
        try:
            rated = Rating.objects.get(user=self.request.user,product=product)
        except (Rating.DoesNotExist):
            rated =None
        if rated is None:
            rating = RatingSerializer(data=request.data)
            if rating.is_valid(raise_exception=True):
                rating.save(user=request.user,product=product)
                return Response("rated")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryView(generics.ListAPIView):
    serializer_class = ListHomeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = SubSubCategory.objects.all()

    # def get(self, request, *args, **kwargs):
    #     subsub = SubSubCategory.objects.all()
    #     subsubcat = SubCategorySerializer(data=subsub,many=True)
    #     subsubcat.is_valid()
    #     for subsubcategory in subsubcat.data:
    #         category = subsubcategory['category']
    #         sub2cat = subsubcategory['id']
    #         subsubcategory['category'] = Category.objects.get(id=category).category
    #         subsubcategory['id'] = SubSubCategory.objects.get(id=sub2cat).subsubcategory
    #     return Response(subsubcat.data)

class SubcategoryView(generics.CreateAPIView):
    serializer_class = ListSubcategorySerializer
    permission_classes = (permissions.AllowAny,)
    # queryset = Subcategory.objects.all()

    def get_serializer_context(self):
        category = self.kwargs['category']
        return {'category':category}


class SubSubcategoryView(generics.CreateAPIView):
    serializer_class = ListSubSubCategorySerializer
    permission_classes = (permissions.AllowAny,)
    # queryset = SubSubCategory.objects.all()

    def get_serializer_context(self):
        subcategory = self.kwargs['subcategory']
        category = self.kwargs['category']
        return {'subcategory':subcategory,'category':category}


class CartView(generics.ListAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def list(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        product_list = Product.objects.filter(cart=cart)
        serializer = ProductSerializer(data=product_list,many=True)
        serializer.is_valid()
        return Response(serializer.data)


class AddOrRemoveToCartView(APIView):

    def get(self,request,*args,**kwargs):
        id = self.kwargs['product_id']
        cart = Cart.objects.get(user=request.user)
        try:
            product_in_cart = Product.objects.get(Q(cart=cart)&Q(id=id))
        except Product.DoesNotExist:
            product_in_cart = None
        if product_in_cart is None:
            try:
                product_selected = Product.objects.get(id=id)
            except Product.DoesNotExist:
                product_selected = None
            if product_selected is not None:
                cart.product.add(product_selected)
                return Response({'message':'Added to cart'})
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                product_selected = Product.objects.get(id=id)
            except Product.DoesNotExist:
                product_selected = None
            if product_selected is not None:
                cart.product.remove(product_selected)
                return Response({'message':'Removed from cart'})
            return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def list(self, request, *args, **kwargs):
        order = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(data=order,many=True)
        serializer.is_valid()
        return Response(serializer.data)

    def perform_create(self, serializer):
        product = self.kwargs['product_id']
        prod = Product.objects.get(id=product)
        serializer.save(user=self.request.user,product=prod)

    def update(self, request, *args, **kwargs):
        pass


class PaymentView(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


