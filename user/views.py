from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import Profile
from user.serializers import ProfileSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        user = Profile.objects.filter(email=email).first()
        print(email, password)
        if user is not None and check_password(password, user.password):
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def signup_for_client(request):

    email = request.data['email']
    if Profile.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Create a new Profile instance
        user_password_hashed = make_password(password)
        user = Profile(
            username=username,
            email=email,
            is_active="Active",
            password=user_password_hashed,
        )
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signup_for_operator(request):

    email = request.data['email']
    if Profile.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        is_staff = request.data.get('is_staff')
        password = request.data.get('password')
        print(is_staff)
        # Create a new Profile instance
        user_password_hashed = make_password(password)
        user = Profile(
            username=username,
            email=email,
            is_active="Active",
            is_staff=is_staff,
            password=user_password_hashed,
        )
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
