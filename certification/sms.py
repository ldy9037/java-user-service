import boto3
import logging

#from user_service.settings import AWS_CONFIG
logger = logging.getLogger('pybo')

def publish_message(phone_number, cert_number):
    """
    client = boto3.client(
        "sns",
        aws_access_key_id=AWS_CONFIG['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=AWS_CONFIG['AWS_SECRET_ACCESS_KEY'],
        region_name=AWS_CONFIG['AWS_REGION']
    )

    phone_number = "+82" + phone_number
    message = "인증 번호는 ["+cert_number+"] 입니다. \n(제한 시간: 3분)"

    try:
        response = client.publish(
            PhoneNumber=phone_number, Message=message)
    except boto3.ClientError:
        logger.exception("메세지 전송에 실패하였습니다. 받는사람 : %s", phone_number)
        raise
    else:
        return response
    """