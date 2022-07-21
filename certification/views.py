from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CertificationSerializer
from user_service import utils
from certification.models import Certification
from user.models import User
from certification import sms

# 함수 형식 view로 POST, PATCH 동작 구현 
# PATCH의 경우 인증체크
# class 기반 view로 viewset을 사용해 깔끔하게 코드 구현 가능했을 것 같음.(perform_create, perform_update) 
# serializer의 is_valid는 실패시 error속성을 사용할 수 있음. 해당 속성에는 유요하지 않은 필드에 대한 오류를 나열함. 이 속성을 사용해서 Response를 전달했으면 깔끔했겠음. 
# 응답 데이터에 serializer를 활용하지 않았음. return data 구조도 개선 필요
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
            
    
        
        
        
        
    
