from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CertificationSerializer
from user_service import utils
from certification.models import Certification
from user.models import User
from certification import sms

@api_view(['POST', 'PATCH'])
def request_certification_number(request):
    data = {'message': ""}

    if request.method == 'POST':
        serializer = CertificationSerializer(data=request.data)

        if serializer.is_valid():
            if User.objects.filter(phone_number=serializer.validated_data['phone_number']).count(): 
                data['message'] = "이미 가입된 휴대폰 번호입니다."
                return Response(data, status.HTTP_200_OK)
            
            serializer.save()

            cert_number = Certification.objects.filter(phone_number=serializer.data['phone_number']).latest('created_at').number
            sms.publish_message(serializer.data['phone_number'].replace("-",""), cert_number)

            data['message'] = "인증 번호가 전송되었습니다. (제한 시간: 3분)"
            data['cert_id'] = serializer.data["id"]

            return Response(data, status=status.HTTP_201_CREATED)

    elif request.method == 'PATCH':
        serializer = CertificationSerializer(data=request.data) 
        
        if serializer.is_valid():
            certification = Certification.objects.filter(id=request.data['id'], phone_number=serializer.validated_data['phone_number'])

            if certification.count() > 0:
                if serializer.validated_data['number'] == certification.get().number and certification.get().ttl >= utils.create_timestamp_ttl(0):
                    certification.update(certified=True)
                    data['message'] = "인증 되었습니다."
                    data['cert_id'] = certification.get().id
                    data['phone_number'] = certification.get().phone_number
            else:
                data['message'] = "인증 번호가 올바르지 않습니다."

            return Response(data, status=status.HTTP_200_OK)
            
    
        
        
        
        
    
