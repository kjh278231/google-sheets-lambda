import boto3
from botocore.config import Config
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
        sts = boto3.client('sts', config=my_config)
        print(sts.get_caller_identity())
        # 서비스 자원 가져오기
        sqs = boto3.resource('sqs',config=my_config)

        # 큐 가져오기. SQS.Queue 인스턴스가 반환됩니다.
        queue = sqs.get_queue_by_name(QueueName='SPREAD_INSERT_QUEUE')

        # queue 로 메시지 전송하기
        send_messages(queue,[{
            "id":"1",
            "body":"This is test message",
            "attributes":{
                'Author': {
                    'StringValue': 'Daniel',
                    'DataType': 'String'
                }
            }}])

    except Exception as inst:
        logger.error(inst)
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }

def receiveMessageHandler(event, context):
    try:
        logger.info(event)
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

        # queue에서 메시지 가져오기
        meesage = receive_messages(queue,1,0)
        logger.info(meesage)
    except Exception as inst:
        logger.error(inst)
        return {
            "status": "FAIL",
            "value": "-",
            "message": "오류가 발생했습니다.."
        }
    
def send_messages(queue, messages):
    """
    Send a batch of messages in a single request to an SQS queue.
    This request may return overall success even when some messages were not sent.
    The caller must inspect the Successful and Failed lists in the response and
    resend any failed messages.

    :param queue: The queue to receive the messages.
    :param messages: The messages to send to the queue. These are simplified to
                     contain only the message body and attributes.
    :return: The response from SQS that contains the list of successful and failed
             messages.
    """
    try:
        entries = [
            {
                "Id": str(ind),
                "MessageBody": msg["body"],
                "MessageAttributes": msg["attributes"],
            }
            for ind, msg in enumerate(messages)
        ]
        response = queue.send_messages(Entries=entries)
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                logger.info(
                    "Message sent: %s: %s",
                    msg_meta["MessageId"],
                    messages[int(msg_meta["Id"])]["body"],
                )
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                logger.warning(
                    "Failed to send: %s: %s",
                    msg_meta["MessageId"],
                    messages[int(msg_meta["Id"])]["body"],
                )
    except Exception as error:
        logger.exception("Send messages failed to queue: %s", queue)
        raise error
    else:
        return response



def receive_messages(queue, max_number, wait_time):
    """
    Receive a batch of messages in a single request from an SQS queue.

    :param queue: The queue from which to receive messages.
    :param max_number: The maximum number of messages to receive. The actual number
                       of messages received might be less.
    :param wait_time: The maximum time to wait (in seconds) before returning. When
                      this number is greater than zero, long polling is used. This
                      can result in reduced costs and fewer false empty responses.
    :return: The list of Message objects received. These each contain the body
             of the message and metadata and custom attributes.
    """
    try:
        messages = queue.receive_messages(
            MessageAttributeNames=["All"],
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=wait_time,
        )
        for msg in messages:
            logger.info("Received message: %s: %s", msg.message_id, msg.body)
    except Exception as error:
        logger.exception("Couldn't receive messages from queue: %s", queue)
        raise error
    else:
        return messages



def delete_messages(queue, messages):
    """
    Delete a batch of messages from a queue in a single request.

    :param queue: The queue from which to delete the messages.
    :param messages: The list of messages to delete.
    :return: The response from SQS that contains the list of successful and failed
             message deletions.
    """
    try:
        entries = [
            {"Id": str(ind), "ReceiptHandle": msg.receipt_handle}
            for ind, msg in enumerate(messages)
        ]
        response = queue.delete_messages(Entries=entries)
        if "Successful" in response:
            for msg_meta in response["Successful"]:
                logger.info("Deleted %s", messages[int(msg_meta["Id"])].receipt_handle)
        if "Failed" in response:
            for msg_meta in response["Failed"]:
                logger.warning(
                    "Could not delete %s", messages[int(msg_meta["Id"])].receipt_handle
                )
    except Exception:
        logger.exception("Couldn't delete messages from queue %s", queue)
    else:
        return response


