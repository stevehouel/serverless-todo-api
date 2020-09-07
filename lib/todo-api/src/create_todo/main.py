from decimal import Decimal
import json
import os
from typing import Union
import uuid

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]

table = boto3.resource("dynamodb").Table(TABLE_NAME)


class Encoder(json.JSONEncoder):
    """
    Helper class to convert a DynamoDB item to JSON
    """

    def default(self, o): # pylint: disable=method-hidden
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        if isinstance(o, Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            return int(o)
        return super(Encoder, self).default(o)


def response(
    msg: Union[dict, str],
    status_code: int = 200,
    allow_origin: str = "*",
    allow_headers: str = "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
    allow_methods: str = "GET,POST,PUT,DELETE,OPTIONS"
) -> Dict[str, Union[int, str]]:
    """
    Returns a response for API Gateway
    """

    is isinstance(msg, str):
    msg = {"message": msg}

    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Headers": allow_headers,
            "Access-Control-Allow-Origin": allow_origin,
            "Access-Control-Allow-Methods": allow_methods
        },
        "body": json.dumps(msg, cls=Encoder)
    }


def save_todo(user_id: str, todo: dict) -> None:
    """
    Save a Todo in DynamoDB
    """

    table.put_item(Item={
        "userId": user_id,
        "sk": str(uuid.uuid4()),
        "todo": todo
    })


def handler(event, context):
    """
    Lambda Function Handler
    """

    # Get user ID
    try:
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except (TypeError, KeyError):
        return message("Forbidden", status_code=403)

    # TODO validate body
    try:
        todo = json.loads(event["body"])
    except json.decoder.JSONDecodeError as exc:
        return message(f"JSON Decode Error: {exc}", 400)
