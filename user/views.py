from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User

@api_view(['GET','POST'])
def list_insert_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
    return Response(serializer.data)

@api_view(['GET'])
def count_users(request, value):
    data = {'message': ""}

    if request.method == 'GET':
        count = User.objects.filter(email=value).count()
        data['email'] = count
            
        count = User.objects.filter(phone_number=value).count()
        data['phone_number'] = count

        return Response(data, status.HTTP_200_OK)

