# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import endpoint_options_view
from coriolis.tests import test_base


class EndpointOptionsViewTestCase(test_base.CoriolisApiViewsTestCase):

    def test_source_options_collection(self):
        fun = getattr(endpoint_options_view, 'source_options_collection')
        self._collection_view_test(fun, "source_options")
