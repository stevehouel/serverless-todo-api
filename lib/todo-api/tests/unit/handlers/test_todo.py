import boto3
import json
import os
import src.handlers.todo as handlers

from datetime import date
from moto.dynamodb2 import mock_dynamodb2
from undecorated import undecorated


get_all_todos = undecorated(handlers.get_all_todos)
get_todo = undecorated(handlers.get_todo)
create_todo = undecorated(handlers.create_todo)
update_todo = undecorated(handlers.update_todo)
delete_todo = undecorated(handlers.delete_todo)

__DEFAULT_TODO_ID__ = '6fb261b1-7d6f-41c2-b168-236fb50d9cde'
__DEFAULT_DATE__ = date.today().strftime("%m/%d/%Y")


@mock_dynamodb2
def test_get_all_todos():
    resource = init_table()
    err, body = get_all_todos(event=None, context=None, resource=resource)
    assert not err
    assert body
    assert len(body) == 1
    assert body[0].get('title') == 'sampleTitle'
    assert body[0].get('content') == 'sampleContent'
    assert body[0].get('todoId') == __DEFAULT_TODO_ID__
    assert body[0].get('updatedAt')


@mock_dynamodb2
def test_get_todo():
    resource = init_table()
    err, body = get_todo(event=None, context=None, resource=resource, todoId=__DEFAULT_TODO_ID__)
    assert not err
    assert body
    assert body.get('title') == 'sampleTitle'
    assert body.get('content') == 'sampleContent'
    assert body.get('todoId') == __DEFAULT_TODO_ID__
    assert body.get('updatedAt')


@mock_dynamodb2
def test_get_todo_invalid_id():
    resource = init_table()
    err, body = get_todo(event=None, context=None, resource=resource, todoId='INVALID')
    assert err
    assert err['statusCode'] == '404'
    assert err['message'] == 'Todo item INVALID not found'
    assert not body


@mock_dynamodb2
def test_delete_todo():
    resource = init_table()
    err, body = delete_todo(event=None, context=None, resource=resource, todoId=__DEFAULT_TODO_ID__)
    assert not err
    assert body
    assert body['code'] == '200'
    assert body['message'] == 'Deleted'
    table = resource.Table(os.environ.get('TABLE_NAME'))
    response = table.get_item(
        Key={
            'todoId': __DEFAULT_TODO_ID__
        }
    )
    assert 'Item' not in response


@mock_dynamodb2
def test_delete_todo_invalid_id():
    resource = init_table()
    err, body = delete_todo(event=None, context=None, resource=resource, todoId='INVALID')
    assert not err
    assert body
    assert body['code'] == '200'
    assert body['message'] == 'Deleted'
    table = resource.Table(os.environ.get('TABLE_NAME'))
    response = table.get_item(
        Key={
            'todoId': __DEFAULT_TODO_ID__
        }
    )
    assert 'Item' in response


@mock_dynamodb2
def test_create_todo():
    resource = init_table()
    event = {
        'body': json.dumps({
            'title': 'createdTitle',
            'content': 'createdContent',
        })
    }
    err, body = create_todo(event=event, context=None, resource=resource)
    assert not err
    assert body
    table = resource.Table(os.environ.get('TABLE_NAME'))
    response = table.get_item(
        Key={
            'todoId': body
        }
    )
    assert 'Item' in response
    assert response['Item']['todoId'] == body
    assert response['Item']['title'] == 'createdTitle'
    assert response['Item']['content'] == 'createdContent'
    assert response['Item']['updatedAt']


@mock_dynamodb2
def test_update_todo():
    resource = init_table()
    event = {
        'body': json.dumps({
            'title': 'updatedTitle',
            'content': 'updatedContent',
            'todoId': __DEFAULT_TODO_ID__
        })
    }
    err, body = update_todo(event=event, context=None, resource=resource, todoId=__DEFAULT_TODO_ID__)
    assert not err
    assert body
    assert body['title'] == 'updatedTitle'
    assert body['content'] == 'updatedContent'
    assert body['updatedAt'] is not __DEFAULT_DATE__
    table = resource.Table(os.environ.get('TABLE_NAME'))
    response = table.get_item(
        Key={
            'todoId': __DEFAULT_TODO_ID__
        }
    )
    assert 'Item' in response
    assert response['Item']['title'] == 'updatedTitle'
    assert response['Item']['content'] == 'updatedContent'
    assert response['Item']['updatedAt'] == body['updatedAt']


def init_table():
    resource = boto3.resource('dynamodb', 'eu-west-1')
    table = resource.create_table(
        TableName=os.environ.get('TABLE_NAME'),
        KeySchema=[
            {
                'AttributeName': 'todoId',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'todoId',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.put_item(Item={
        'todoId': __DEFAULT_TODO_ID__,
        'title': 'sampleTitle',
        'content': 'sampleContent',
        'updatedAt': __DEFAULT_DATE__
    })

    table = resource.Table(os.environ.get('TABLE_NAME'))
    response = table.get_item(
        Key={
            'todoId': __DEFAULT_TODO_ID__
        }
    )
    if 'Item' in response:
        item = response['Item']

    assert 'todoId' in item
    return resource
