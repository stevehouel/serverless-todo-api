from src.main import logger, get_resource

DEBUG_HEADER = 'debug-log-enabled'


class Request:

    def __init__(self, event, resource=None):
        self.event = event
        self.params = {}
        self.request_context = {}
        self.resource = resource or get_resource()

    def get_and_check_params(self, mandatory, optional):
        params = {}
        if self.event.get('pathParameters'):
            params.update(self.event.get('pathParameters', {}))
        if self.event.get('queryStringParameters'):
            params.update(self.event.get('queryStringParameters', {}))
        err, res = self.check_params(params, mandatory, optional)
        if err:
            logger.error(err)
            return err, False
        else:
            self.params.update(res)
            return None, True

    @staticmethod
    def operation_not_authorised():
        logger.info('Operation not authorised')
        err = ValueError('Operation not authorised')
        err.status_code = '401'
        return err, False

    @staticmethod
    def check_params(params, mandatory, optional):
        """
        Check request params
        :param params: Params to verify
        :param mandatory:
        :param optional:
        :return:
        """
        values = {}
        missing = []
        for param in mandatory:
            value = params.get(param)
            if not value or value == '':
                missing.append(param)
            else:
                values[param] = value
        for param in optional:
            value = params.get(param)
            if param in params:
                values[param] = value
        if missing:
            msg = 'Empty or missing mandatory parameter(s): %s' % ', '.join(missing)
            return ValueError(msg), None
        else:
            return None, values
