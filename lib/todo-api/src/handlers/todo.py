import json
import uuid

from datetime import date

from botocore.exceptions import ClientError

from src.core.decorator.api_endpoint import api_endpoint
from src.core.decorator.api_params import api_params
from src.main import logger, tracer, table_name

from src.schemas.todo_item import todo_item_schema, todo_items_schema


@tracer.capture_lambda_handler
@logger.inject_lambda_context
@api_endpoint()
def get_all_todos(event, context, resource):
    try:
        table = resource.Table(table_name)
        response = table.scan()
        return None, todo_items_schema.dump(response.get('Items', []))
    except (TypeError, ValueError) as err:
        return err, None
    except AssertionError as e:
        return ValueError(str(e)), None


@tracer.capture_lambda_handler
@logger.inject_lambda_context
@api_endpoint()
@api_params(required=['todoId'])
def get_todo(event, context, resource, todoId):
    try:
        table = resource.Table(table_name)
        result = table.get_item(Key={'todoId': todoId})
        if 'Item' not in result:
            return {
                       'statusCode': '404',
                       'message': 'Todo item {} not found'.format(todoId)
                   }, None
        return None, todo_item_schema.dump(result['Item'])

    except ClientError as e:
        return ValueError(str(e.response['Error']['Message'])), None
    except (TypeError, ValueError) as err:
        return err, None
    except (AssertionError, ClientError) as e:
        return ValueError(str(e)), None


@tracer.capture_lambda_handler
@logger.inject_lambda_context
@api_endpoint()
def create_todo(event, context, resource):
    try:
        # Get Table resource
        table = resource.Table(table_name)

        # Get body content
        body = event.get('body')
        body = json.loads(body)

        assert 'title' in body, 'Title field is required'
        todoId = str(uuid.uuid4())
        response = table.put_item(
            Item={
                'todoId': todoId,
                'title': body['title'],
                'content': body['content'],
                'updatedAt': date.today().strftime("%m/%d/%Y")
            }
        )
        return None, todoId
    except (TypeError, ValueError) as err:
        return err, None
    except AssertionError as e:
        return ValueError(str(e)), None


@tracer.capture_lambda_handler
@logger.inject_lambda_context
@api_endpoint()
@api_params(required=['todoId'])
def update_todo(event, context, resource, todoId):
    try:
        table = resource.Table(table_name)

        # Get body content
        body = event.get('body')
        body = json.loads(body)

        assert 'title' in body, 'Title field is required'

        results = table.update_item(
            Key={
                'todoId': todoId
            },
            UpdateExpression="set title=:t, content=:c, updatedAt=:d",
            ExpressionAttributeValues={
                ':t': body['title'],
                ':c': body['content'],
                ':d': date.today().strftime("%m/%d/%Y")
            },
            ReturnValues="ALL_NEW"
        )
        return None, todo_item_schema.dump(results['Attributes'])
    except (TypeError, ValueError) as err:
        return err, None
    except AssertionError as e:
        return ValueError(str(e)), None


@tracer.capture_lambda_handler
@logger.inject_lambda_context
@api_endpoint()
@api_params(required=['todoId'])
def delete_todo(event, context, resource, todoId):
    try:
        table = resource.Table(table_name)
        table.delete_item(
            Key={
                'todoId': todoId,
            }
        )
        return None, {
            "code": '200',
            "message": "Deleted"
        }
    except (TypeError, ValueError) as err:
        return err, None
    except AssertionError as e:
        return ValueError(str(e)), None
