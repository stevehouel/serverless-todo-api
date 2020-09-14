from functools import wraps
from src.main import logger


def api_params(required, optional=[]):
    """Extract values from request context and fail if missing"""
    def decorator(func):
        @wraps(func)
        def decorated(event, context, resource):
            req = context.request
            err, ok = req.get_and_check_params(required, optional)
            if not ok:
                return err, None
            else:
                logger.debug('Injecting params to request: {}'.format(req.params))
                return func(event, context, resource, **req.params)
        return decorated
    return decorator
