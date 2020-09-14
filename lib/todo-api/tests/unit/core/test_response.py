import unittest
import json

from src.core.response import response


class TestResponse(unittest.TestCase):

    def test_response_200(self):

        return_200 = {
            'statusCode': '200',
            'body': '{\n  "id": 1234\n}',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

        self.assertEqual(return_200, response(None, {'id': 1234}))

    def test_response_error_default(self):

        return_400 = {
            'statusCode': '400',
            'body': json.dumps({'message': str('Error')}, indent=2),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

        self.assertEqual(return_400, response(ValueError('Error')))
        self.assertEqual(return_400, response(ValueError('Error'), {'id': 1234}))

    def test_response_error_custom(self):

        return_404 = {
            'statusCode': '404',
            'body': json.dumps({'message': str('Not found')}, indent=2),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

        error404 = ValueError('Not found')
        error404.status_code = '404'
        self.assertEqual(return_404, response(error404))
