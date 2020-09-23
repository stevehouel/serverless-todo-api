from functools import wraps
from src.main import logger, get_resource
from src.core.request import Request
from src.core.response import response


def api_endpoint():
    """Decorate a lambda function endpoint with user access checking"""
    def decorator(func):
        @wraps(func)
        def decorated(event, context):
            try:
                resource = get_resource()
                req = Request(event=event, resource=resource)
                # Assign request to context
                context.request = req
                # Call method and manage session in case of error
                err, res = func(event, context, resource)
            except Exception as e:
                logger.error(e)
                err, res = e, None
                err.status_code = '500'

            return response(err, res)
        return decorated
    return decorator
