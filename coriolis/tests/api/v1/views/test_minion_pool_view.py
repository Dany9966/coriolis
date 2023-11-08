# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

from unittest import mock

from coriolis.api.v1.views import minion_pool_view as view
from coriolis.api.v1.views import utils as view_utils
from coriolis.tests import test_base


class MinionPoolViewTestCase(test_base.CoriolisBaseTestCase):
    """Test suite for the Coriolis api v1 views."""

    @mock.patch.object(view_utils, '_format_opt')
    def test_format_minion_pool(
        self,
        mock__format_opt,
    ):
        mock_minion_pool_dict = {
            'minion_machines': [{
                'connection_info': {
                    'pkey': 'mock_key',
                    'password': 'mock_key',
                    'certificates': {'key': 'mock_key'}
                },
                'backup_writer_connection_info': {
                    'connection_details': {
                        'pkey': 'mock_key',
                        'password': 'mock_key',
                        'certificates': {'key': 'mock_key'}
                    },
                }
            }],
        }
        expected_result = {
            'minion_machines': [{
                'connection_info': {
                    'pkey': '***',
                    'password': '***',
                    'certificates': {'key': '***'}
                },
                'backup_writer_connection_info': {
                    'connection_details': {
                        'pkey': '***',
                        'password': '***',
                        'certificates': {'key': '***'}
                    },
                }
            }],
        }
        mock__format_opt.return_value = mock_minion_pool_dict

        result = view._format_minion_pool("")
        self.assertEqual(
            expected_result,
            result
        )
