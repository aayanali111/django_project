from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UsersInfo
from .serializers import UsersInfoSerializer

@api_view(['GET'])
def get_users(request):
    users = UsersInfo.objects.all()
    serializer = UsersInfoSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def register_user(request):
    serializer = UsersInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # password will be hashed here
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_user(request):
    user_id = request.data.get("id")
    try:
        user = UsersInfo.objects.get(id=user_id)
    except UsersInfo.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsersInfoSerializer(user, data=request.data, partial=False)  # use partial=True if you want PATCH-like behaviour
    if serializer.is_valid():
        serializer.save()  # will hash password if present
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request):
    user_id = request.data.get("id")
    try:
        user = UsersInfo.objects.get(id=user_id)
    except UsersInfo.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)