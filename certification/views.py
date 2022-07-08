from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CertificationSerializer
from user_service import utils
from certification.models import Certification
from user.models import User

@api_view(['POST'])
def request_certification_number(request):
    if request.method == 'POST':
        serializer = CertificationSerializer(data=request.data)
        data = {'message': ""}

        if serializer.is_valid():
            if User.objects.filter(phone_number=serializer.validated_data['phone_number']).count(): 
                data['message'] = "이미 가입된 휴대폰 번호입니다."
                return Response(data, status.HTTP_200_OK)
            
            serializer.save()


            cert_number = Certification.objects.filter(phone_number=serializer.data['phone_number']).latest('created_at').number


            data['message'] = "인증 번호가 전송되었습니다. (제한 시간: 3분)"
            return Response(data, status=status.HTTP_201_CREATED)
        
        
        
        
    
