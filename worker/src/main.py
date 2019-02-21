import boto3
import time
import logging
from pymongo import MongoClient
from aws_connectors import aws_connectors


def save_document_in_collection(suggestion):
    
    client = MongoClient('localhost', 27017)
    db = client.suggestions
    sug = db.sug

    suggestion_doc = {'suggestions': suggestion}
    sug.insert_one(suggestion_doc).inserted_id

if __name__ == '__main__':

    sqs, sqs_client = aws_connectors()
    queue = sqs.get_queue_by_name(QueueName='maxmilhas')
    
    suggestions = sqs_client.receive_message(MaxNumberOfMessages=10,
                                            WaitTimeSeconds=1,
                                            MessageAttributeNames=['All'],
                                            QueueUrl=queue.url)

    if 'Messages' in suggestions:
        for suggestion in suggestions['Messages']:
            save_document_in_collection(suggestion['Body'])
            sqs_client.delete_message(QueueUrl=queue.url, ReceiptHandle=suggestion['ReceiptHandle'])
            print('Received and deleted message: %s' % suggestion)


    
