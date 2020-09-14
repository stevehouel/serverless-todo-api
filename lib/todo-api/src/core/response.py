import json

from src.main import logger


def response(err, res=None, status='200'):
    if err:
        status = getattr(err, 'status_code', '400')
        logger.error("Client response code: %s", status)
        # build error content
        if status == '500':
            res = {'message': 'An internal server error occurred, please contact the support'}
        else:
            res = {'message': str(err)}

    return {
        'statusCode': status,
        'body': json.dumps(res, indent=2),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
