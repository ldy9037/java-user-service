from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CertificationSerializer
from user_service import utils

@api_view(['POST'])
def request_certification_number(request):
    if request.method == 'POST':
        serializer = CertificationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        
        message = {'message': "인증 번호가 전송되었습니다."}

        return Response(message, status=status.HTTP_201_CREATED)
    
