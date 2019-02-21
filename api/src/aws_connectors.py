from boto3 import (Session,
                    resource,
                    client)
import os

def aws_connectors():

    session = Session(region_name=os.environ.get('AWS_DEFAULT_REGION'),
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    sqs = session.resource('sqs')
    sqs_client = session.client('sqs')

    return sqs, sqs_client
