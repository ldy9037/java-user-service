# ldy9037/assignment-python-service

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Django + rest_framework로 회원 서비스 구현 

##### 좋은 commit message 작성을 위한 참고자료

- [commit message 작성 규칙](https://meetup.toast.com/posts/106)
- [commit naming](https://blog.ull.im/engineering/2019/03/10/logs-on-git.html)
- [commit message style guide](https://udacity.github.io/git-styleguide/)


## Table of Contents

- [소개](#소개)
- [시작하기](#시작하기)
- [구현내용](#구현내용)
- [API명세](#API명세)
- [제작자](#제작자)

## 소개

 Django + rest_framework를 사용해서 REST API를 구현 하였습니다. 

 ##### 구현 기능
 - DevOps
 - 휴대폰 인증
 - 회원 가입
 - 로그인
 - 내 정보 보기
 - 비밀번호 찾기(변경)
 
 ##### 기술 스택
 - Python 3.8
 - Django 3.2.5
 - Mysql 5.7
 - Docker 20.10.14
 - docker-compose 1.29.2
 - Github Actions

 Task 관리는 Github의 issues를 사용했습니다.
 - [Github Issues](https://github.com/ldy9037/assignment-python-service/issues)
 
## 시작하기
docker, docker-compose를 설치해주세요.
- [Mac에서 설치](https://docs.docker.com/desktop/mac/install/)
- [Windows에서 설치](https://docs.docker.com/desktop/windows/install/) 

repository를 clone하고 repository root directory에 secret.json을 생성해줍니다.
```
$ cat <<EOF > `${pwd}`secrets.json
{
    "PYTHON_SECRET_KEY": "<PYTHON_SECRET_KEY>",
    
    "DB_USER": "root",
    "DB_PASSWORD": "<DB_PASSWORD>",
    "DB_HOST": "172.30.0.1",
    "DB_PORT": "3306"
}
EOF
```
| Key           |  Value   |
| ------------- | -------- |
| PYTHON_SECRET_KEY            | 메일로 전달해드린 값을 입력해주세요.  |
| DB_PASSWORD            | 원하시는 값을 입력해주세요.  |

secret 설정이 되었으니 docker container를 실행합니다.
```sh
$ docker-compose -f docker-compose-test.yml up -d
```

컨테이너가 실행되면 개발용 Mysql도 docker로 실행시켜 줍니다.
```sh
$ docker run --name mysql -d \
        -e MYSQL_ROOT_PASSWORD='<DB_PASSWORD>' \
        -e MYSQL_DATABASE=user_service \
		--mount type=bind,source=`pwd`/docker/mysql/default.cnf,target=/etc/mysql/conf.d/default.cnf \
		-p 3306:3306 \
		--network `echo ${PWD##*/}`_test_bridge \
        mysql:5.7 
```
DB_PASSWORD에는 위에서 secret에 입력했던 값을 똑같이 입력해주시면 됩니다.

이제 개발환경 세팅이 완료되었습니다. 
정상적으로 동작하는 테스트를 실행해줍니다.
```sh
$ API_CONTAINER_ID=`docker ps --filter name=user-api --format "{{.ID}}"`
$ docker exec --workdir /usr/src $API_CONTAINER_ID python manage.py test
```

실제 개발 전에는 migration을 해주어야합니다.
```sh
$ docker exec --workdir /usr/src $API_CONTAINER_ID python manage.py makemigrations
$ docker exec --workdir /usr/src $API_CONTAINER_ID python manage.py migrate
```

## 구현내용
구현 내용과 범위입니다.

### DevOps  

| 구현 기능 | 개발 환경 가상화  |
| --------| ---------------------------------------- |
| 구현 내용 | docker-compose를 사용해서 개발 환경을 가상화 하였습니다. 인터프린터 언어의 특성을 활용해서 소스코드가 존재하는 directory만 mount해 개발을 진행할 수 있도록 하였습니다. |
| 구현 효과 | 개발에 필요한 모든 환경은 Container에 자동으로 구성되고 실제 사용자는 Docker만 설치하면 바로 개발에 참여할 수 있습니다. Docker는 환경 일관성을 지켜주기 때문에 각 사용자별 환경 이슈를 해결 할 수 있으며, 운영환경과 동일한 Base Image에 동일한 구성을 사용하기 때문에 배포 시 생기는 이슈를 사전에 방지 할 수 있습니다. |

| 구현 기능 | CI (미완)  |
| --------| ---------------------------------------- |
| 구현 내용 | Github Actions를 사용해서 CI를 구성 예정입니다. 현재 빌드 전 Test 로직만 구현되어 있습니다. |
| 구현 효과 | 개발환경에서 작성한 코드가 빌드되기 전에 잘 동작하는 지 점검하고 사전에 에러를 방지할 수 있습니다. |

### 휴대폰 인증

| 구현 기능 | AWS SMS를 사용한 휴대폰 인증  |
| --------| ---------------------------------------- |
| 구현 내용 | 전체 로직은 [휴대폰 번호를 포함해서 인증 번호 전송을 요청 -> 휴대폰 번호 유효성 검증 + 이미 가입한 번호인지 체크 후 해당 번호로 인증번호 전송 -> 인증 번호와 체크 요청 -> 일치하면 인증 DB 상에 인증 성공 표시] 입니다. 인증을 완료하면 사용자는 회원 가입이나 비밀번호를 찾을 때 인증에 대한 id와 phone_number를 가지고 인증된 사용자인지 체크를 요청합니다. |
| 참고 사항 | AWS SMS는 국내 리전에 출시 되지 않아 메세지 전송 시 사용자 메세지에는 국제발신으로 표시됩니다. 또한 샌드박스(일종의 테스트 환경) 환경에서는 메세지 한도가 월 1달러이기 때문에 40~50 건 정도 전송하면 더 이상 메세지가 전송되지 않습니다. |

- 회원 가입

| 구현 기능 | 인증 체크 및 회원정보 저장 |
| --------| ---------------------------------------- |
| 구현 내용 | 전체 로직은 [휴대폰 번호와 인증 ID를 체크해 휴대폰 인증이 된 사람인지 체크 -> 인증이 된 사람이라면 회원정보 유효성 검증(중복 체크 포함) 후 DB에 저장] 입니다. 사용자 model은 BaseUser를 overriding 하였으며 개인 식별 정보로 email과 phone_number로 사용하였습니다. 비밀번호 암호화의 경우 기본 알고리즘이 아닌 [Argon2](https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#using-argon2-with-django)를 사용하였습니다. |

- 로그인

| 구현 기능 | 개인 식별 정보와 비밀번호를 사용해 Token 발급 |
| --------| ---------------------------------------- |
| 구현 내용 | 전체 로직은 rest_framework의 simple jwt를 사용했습니다. 대부분은 기본 설정을 그대로 사용하였지만 개인 식별정보가 email과 phone_number 두 가지이기 때문에 backend만 커스텀해서 사용하였습니다. token 발급시 포함되는 식별값은 email입니다. |

- 내 정보 보기

| 구현 기능 | Token 확인 후 개인정보 전달 |
| --------| ---------------------------------------- |
| 구현 내용 | 유일하게 권한이 필요한 API이기 때문에 Token check가 필요합니다. token check는 simple jwt에서 제공하는 permission_classes 사용했습니다.정보는 비밀번호와 같은 민감한 정보를 제외하고 반환합니다. |

- 비밀번호 찾기(변경)

| 구현 기능 | 휴대폰 번호 인증 후 비밀번호 변경 |
| --------| ---------------------------------------- |
| 구현 내용 | 휴대폰 번호를 인증했다면 회원가입과 유사한 과정을 통해 비밀번호를 변경 할 수 있습니다. 위에서 구현한 휴대폰 인증을 재사용했기 때문에 쉽게 구현하였습니다. |

### 기타
직접 작성한 대부분의 코드에 대해 테스트 코드가 작성되어 있습니다. 테스트 코드는 각 App directory의 tests/~ 에 존재합니다.

## API명세

### 휴대폰 인증
```sh
# 인증 번호 전송 요청
$ curl -d '{"phone_number":"010-5264-5565"}' \
-H "Content-Type: application/json" \
-X POST http://localhost:9000/api/cert/

{
    "message":"인증 번호가 전송되었습니다. (제한 시간: 3분)",
    "cert_id":2
}
```

```sh
# 인증 번호 체크
$ curl -d '{ "id": 5, "phone_number": "010-5264-5565", "number": "140393" }' \
-H "Content-Type: application/json" \
-X PATCH http://localhost:9000/api/cert/

{
    "message":"인증 되었습니다.",
    "cert_id":2,
    "phone_number":"010-5264-5565"
}
```

### 사용자
```sh
# 회원 가입
$ curl -d '{ "email": "ldy9037@naver.com", "name": "이동열", "nickname": "hani_6_6", "phone_number": "010-5264-5565", "plain_password": "!@#ldy12345", "cert_id": 5 }' \
-H "Content-Type: application/json" \
-X POST http://localhost:9000/api/user/

{
    'message': '회원가입 되었습니다.', 
    'user': {
        'id': 3, 
        'email': 'ldy9037@naver.com', 
        'name': '이동열', 
        'nickname': 'hani_6_6', 
        'phone_number': '010-5264-5565'
    }
}
```

```sh
# 중복 체크 (이메일 대신 휴대폰 번호도 가능 xxx-xxxx-xxxx)
$ curl -X GET "http://localhost:9000/api/count/ldy9037@naver.com"

{
    "message":"",
    "email":0,
    "phone_number":0
}
```

```sh
# 내 정보 가져오기 (사용자 ID)
curl -X GET "http://localhost:9000/api/user/1"

{
    'message': '', 
    'user': {
        'id': 1, 
        'email': 'ldy9037@naver.com', 
        'name': '이동열', 
        'nickname': 'hani_6_6', 
        'phone_number': '010-5264-5565'
    }
}
```

```sh
# 비밀번호 찾기 (변경)
$ curl -d '{ "phone_number": "010-5264-5565", "plain_password": "!@#ldy12345", "cert_id": "4" }' \
-H "Content-Type: application/json" \
-X PATCH http://localhost:9000/api/password/

{
    'message': '정삭적으로 변경되었습니다.'
}
```

```sh
# 로그인 (JWT)
$ curl -d '{ "email": "ldy9037@naver.com", "password": "12345678" }' \
-H "Content-Type: application/json" \
-X POST http://localhost:9000/api/token/

{
    'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni...', 
    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ...'
}
```

```sh
# 기간이 만료된 Access Token 재발급
$ curl -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni..."}' \
-H "Content-Type: application/json" \
-X POST http://localhost:9000/api/token/refresh/

{
    'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ...'
}
```

## 제작자
[ldy9037@naver.com]()
