from  rest_framework import views,filters,permissions,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from  .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends =[DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['role']
    search_fields = ['username','phone_number','tenant_id']


    def perform_create(self.serializer):
        user = serializer.save()
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_decode(force_bytes(user.pk))
        reset_url = f"https://bellissimo/reset-password{uid}/{token}/"
        send_mail(
            subject="Your Bellissimo Account Has Been Created",
            message=(
                f"Dear{user.username},\n\n"
                f"Your Bellissimo account has been created as a {user.role}.\n"
                f"Please set your password to activate your account by visiting:\n{reset_url}\n\n"
                f"if you did not expect this email,please contact vincenttommikorir@gmail.com"
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return user
    
    @action(detail=False, methods=['get'],permission_classes=[permission_classes.IsAuthenticated])