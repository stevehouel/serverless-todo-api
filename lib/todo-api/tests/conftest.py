import os

from aws_xray_sdk import global_sdk_config

# Init Global vars
global_sdk_config.set_sdk_enabled(False)
region = os.environ.get('AWS_REGION')
