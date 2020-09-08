# flake8: noqa
import sys
import os
import boto3

from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Logger

# Global variables
region = os.environ.get('AWS_REGION')
resource = None
tracer = None
logger = None
initialized = False

def build_dynamodb_resource():
  global resource
  logger.debug("Building DynamoDB resource")
  if os.getenv("AWS_SAM_LOCAL") == 'true':
    logger.info('Using local endpoint to access DynamoDB service')
    resource = boto3.resource('dynamodb', region_name='localhost', endpoint_url="http://localhost:8000/")
  else:
    resource = boto3.resource('dynamodb', region_name=region)


def get_resource():
  return resource


def init():
  global initialized
  global tracer
  global logger
  try:
    if initialized:
      return
    else:
      initialized = True
      build_dynamodb_resource()
      tracer = Tracer()
      logger = Logger()

  except Exception as e:
    logger.error("An error occurred during initialization phase", e)
    sys.exit()