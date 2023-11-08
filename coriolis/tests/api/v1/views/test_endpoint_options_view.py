# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import endpoint_options_view
from coriolis.tests import test_base


class EndpointOptionsViewTestCase(test_base.CoriolisBaseTestCase):
    """Test suite for the Coriolis api v1 views."""

    def test_source_options_collection(self):
        mock_option1 = {
            "mock_key1": "mock_value1"
        }
        mock_option2 = {}
        mock_source_options = [mock_option1, mock_option2]

        expected_result = {'source_options': mock_source_options}

        result = endpoint_options_view.source_options_collection(
            mock_source_options)

        self.assertEqual(
            expected_result,
            result
        )

    def test_source_options_collection_no_options(self):
        mock_source_options = []

        expected_result = {'source_options': mock_source_options}

        result = endpoint_options_view.source_options_collection(
            mock_source_options)

        self.assertEqual(
            expected_result,
            result
        )
