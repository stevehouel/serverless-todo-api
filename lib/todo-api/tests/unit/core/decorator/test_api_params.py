import unittest
import mock

from src.core.decorator.api_params import api_params


class TestApiRequired(unittest.TestCase):

    def test_api_params(self):
        mock_check_required = mock.Mock(return_value=(None, True))

        # Init Context & Request mock
        context = mock.MagicMock()
        context.request = mock.MagicMock()
        context.request.get_and_check_params = mock_check_required

        def dummy_func(event, context, resource):
            pass

        dummy_func(None, None, None)
        mock_check_required.assert_not_called()

        wrapped_dummy_func = api_params([], [])(dummy_func)
        wrapped_dummy_func({}, context, None)
        mock_check_required.assert_called_once()
