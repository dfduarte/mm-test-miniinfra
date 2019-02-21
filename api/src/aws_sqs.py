import boto3
import json
import time
from aws_connectors import aws_connectors

def aws_sqs_create_message(suggestion):

    sqs, _ = aws_connectors()

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName='maxmilhas')

    # Create a new message
    response = queue.send_message(MessageBody=suggestion, 
                                  MessageAttributes={
                                        'Suggestion': {
                                           'StringValue': 'Suggestion',
                                           'DataType': 'String'
                                        }
                                        })

    # Returns body and ID confirming the creation
    print(response.get('MessageId'))
    print(response.get('MD5OfMessageBody'))

