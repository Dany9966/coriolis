# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

from unittest import mock

from coriolis.api.v1.views import endpoint_view
from coriolis.api.v1.views import utils as view_utils
from coriolis.tests import test_base


class EndpointViewTestCase(test_base.CoriolisBaseTestCase):
    """Test suite for the Coriolis api v1 views."""

    @mock.patch.object(view_utils, '_format_opt')
    def test_format_endpoint(self, mock__format_opt):
            mock__format_opt.return_value = {
                "mapped_regions": [{'id': 'mock_id1'}, {'id': 'mock_id2'}],
                "mock_key": "mock_value"
            }

            expected_result = {
                'mapped_regions': ['mock_id1', 'mock_id2'],
                'mock_key': 'mock_value'
            }

            result = endpoint_view._format_endpoint("")

            self.assertEqual(
                expected_result,
                result
            )

    @mock.patch.object(view_utils, '_format_opt')
    def test_format_endpoint_no_keys(self, mock__format_opt):
            mock__format_opt.return_value = {
                "mapped_regions": [{'id': 'mock_id1'}, {'id': 'mock_id2'}],
            }

            expected_result = {
                'mapped_regions': ['mock_id1', 'mock_id2'],
            }

            result = endpoint_view._format_endpoint("")

            self.assertEqual(
                expected_result,
                result
            )
