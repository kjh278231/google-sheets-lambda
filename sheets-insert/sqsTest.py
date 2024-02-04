import boto3
from botocore.config import Config
from sqsUtil import *
import logging

logger = logging.getLogger(__name__)

def sendMessageHandler(event, context):
    try:
        my_config = Config(
            region_name = 'ap-northeast-2',
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        # 서비스 자원 가져오기
        sqs = boto3.resource('sqs',config=my_config)

        # 큐 가져오기. SQS.Queue 인스턴스가 반환됩니다.
        queue = sqs.get_queue_by_name(QueueName='SPREAD_INSERT_QUEUE')

        # queue 로 메시지 전송하기
        send_messages(queue,"This is test message")

    except Exception as inst:
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }

def receiveMessageHandler(event, context):
    try:
        my_config = Config(
            region_name = 'ap-northeast-2',
            signature_version = 'v4',
            retries = {
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
        # 서비스 자원 가져오기
        sqs = boto3.resource('sqs',config=my_config)

        # 큐 가져오기. SQS.Queue 인스턴스가 반환됩니다.
        queue = sqs.get_queue_by_name(QueueName='SPREAD_INSERT_QUEUE')

        # queue 로 메시지 전송하기
        meesage = receive_messages(queue,1,0)
        logger.info(meesage)
    except Exception as inst:
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }