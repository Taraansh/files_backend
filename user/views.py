from django.http import JsonResponse
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from user.models import Profile, File
from user.serializers import ProfileSerializer, FileSerializer
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
import jwt
from django.conf import settings
from django.core.mail import send_mail


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
            is_active=True,
            password=user_password_hashed,
        )
        send_welcome_email(user.email, user.username)
        user.save()
        # Send a welcome email

        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def send_welcome_email(to_email, username):
    subject = 'Welcome to Your Website!'
    message = f"Dear {username},\n\nThank you for signing up on Your Website! We're excited to have you as a member of our community."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)


@api_view(["POST"])
def signup_for_operator(request):

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
            is_active=True,
            is_staff=True,
            password=user_password_hashed,
        )
        send_welcome_email(user.email, user.username)
        user.save()
        # Send a welcome email
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def post_file(request):
    decoded_payload = jwt.decode(request.data.get(
        'token'), settings.SECRET_KEY, algorithms=['HS256'])
    user = Profile.objects.get(email=decoded_payload.get('email'))
    serializer = ProfileSerializer(user, many=False)
    file = request.FILES.get('file')

    if serializer.data.get("is_staff"):
        file_data = {
            'user': user.id,
            'file': file
            # Add any other fields you want to save with the file
        }

        file_serializer = FileSerializer(data=file_data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(file_serializer.errors)
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'User is not authorized to upload'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_file(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    for item in serializer.data:
        item['file'] = f'http://127.0.0.1:8000{item["file"]}'
    return Response(serializer.data, status=status.HTTP_200_OK)
