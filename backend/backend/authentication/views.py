from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, UserSerializer

# Register View (User Registration)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user and return the user data and token.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Custom Auth Token (Login)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login a user by providing credentials and return a token.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# User Details View (Authenticated User)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    """
    Get the details of the currently authenticated user.
    """
    user = request.user
    return Response(UserSerializer(user).data)

# User Details View (Authenticated User)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    Delete the currently authenticated user.
    """
    user = request.user
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Logout View (Logout by Deleting Token)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Log out the user by deleting their auth token.
    """
    request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# Get User by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    """
    Get the details of a user by their ID.
    """
    try:
        user = User.objects.get(pk=id)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# Get User by Username
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    """
    Get the details of a user by their username.
    """
    try:
        user = User.objects.get(username=username)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# Update User Details
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Update the details of the currently authenticated user.
    """
    user = request.user
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        updated_user = serializer.save()
        return Response(UserSerializer(updated_user).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
