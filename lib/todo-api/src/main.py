import os

import boto3
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger

# Global variables
region = os.environ.get('AWS_REGION')
table_name = os.environ.get('TABLE_NAME')
resource = boto3.resource('dynamodb', region_name=region)
tracer = Tracer()
logger = Logger()


def get_resource():
    return resource
