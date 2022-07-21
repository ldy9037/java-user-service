from email import message
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer
from .models import User
from certification.models import Certification
from argon2 import PasswordHasher
from user_service.validators import validate_password, validate_phone_number

# 회원 관련 View 
# 이쪽 로직들도 대부분은 Viewset으로 대체 가능할 것 같음. 

# 회원가입 View 
@api_view(['POST'])
def insert_users(request):
    data = {'message': ''}
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        # 휴대폰 인증을 했는지, 요청 데이터들이 유효한지, password를 받았는지
        # 휴대폰 인증 여부의 경우 custom permission으로 만들어서 permission_classes로 지정했으면 깔끔했을 것 같음.
        # password는 굳이 request로 받을 것이 아니고 serializer로 받았어도 좋았겠음. save를 override해서 암호화 로직 넣으면 깔끔함.
        # 어차피 로그인의 경우 별도의 backend에서 진행되기 때문에 너무 view에서 password로 무언가를 하려하지 않아도 괜찮음.
        # 또한 valid의 경우 errors 속성을 사용해서 message를 구성하면 좋았겠음.
        if serializer.is_valid() and request.data['cert_id'] and request.data['plain_password']:
            certification = Certification.objects.filter(id=request.data['cert_id'], phone_number=request.data['phone_number'], certified=True)
            validate_password(request.data['plain_password'])

            if certification.count():
                password = PasswordHasher().hash(request.data['plain_password'])
                serializer.save()
                User.objects.filter(id=serializer.data["id"]).update(password=password)
                data['message'] = "회원가입 되었습니다."
                data['user'] = serializer.data
                return Response(data, status=status.HTTP_201_CREATED)    
            else:    
                data['message'] = '휴대폰 번호 인증을 진행해주세요.'
                return Response(data, status=status.HTTP_200_OK)
        else:
            data['message'] = "입력 정보가 유효하지 않습니다."
            return Response(data, status=status.HTTP_400_BAD_REQUEST)        
    
# 중복체크를 위한 더 좋은 방법은 없을까?
@api_view(['GET'])
def count_users(request, value):
    data = {'message': ""}

    if request.method == 'GET':
        count = User.objects.filter(email=value).count()
        data['email'] = count
            
        count = User.objects.filter(phone_number=value).count()
        data['phone_number'] = count

        return Response(data, status.HTTP_200_OK)

# 본인의 개인정보를 가져오는 view
# 이것도 본인임을 확인하는 custom permission을 생성해서 permission_classes로 지정했으면 좋았겠음.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    data = {'message': ""}

    if request.method == 'GET':
        serializer = UserSerializer(User.objects.filter(id=id).get())

        data['user'] = serializer.data
    
        return Response(data, status.HTTP_200_OK)

# 비밀번호 찾기(비밀번호 변경)
# 휴대폰 번호 인증 permission 적용했으면 좋았겠음.
# 비밀번호 변경도 회원가입과 마찬가지로 serializer를 사용해 로직을 간소화할 수 있을 것 같음.
@api_view(['PATCH'])
def find_password(request):
    data = {'message': ""}

    if request.method == 'PATCH':
        
        if request.data['cert_id'] and request.data['plain_password'] and request.data['phone_number']:
            validate_password(request.data['plain_password'])
            validate_phone_number(request.data['phone_number'])

            certification = Certification.objects.filter(id=request.data['cert_id'], phone_number=request.data['phone_number'], certified=True)    

            if certification.count():
                password = PasswordHasher().hash(request.data['plain_password'])
                User.objects.filter(phone_number=request.data['phone_number']).update(password=password)
                
                data['message'] = "정상적으로 변경되었습니다."
                return Response(data, status.HTTP_200_OK)  
            else:
                data['message'] = '휴대폰 번호 인증을 진행해주세요.'
                return Response(data, status=status.HTTP_200_OK)
        else:
            data['message'] = '정확한 정보를 입력해주세요.'
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   
