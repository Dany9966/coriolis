# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

from unittest import mock

from coriolis.api.v1.views import migration_view
from coriolis.api.v1.views import replica_tasks_execution_view as view
from coriolis.api.v1.views import utils as view_utils
from coriolis.tests import test_base


class MigrationViewTestCase(test_base.CoriolisBaseTestCase):
    """Test suite for the Coriolis api v1 views."""

    @mock.patch.object(view, 'format_replica_tasks_execution')
    @mock.patch.object(view_utils, '_format_opt')
    def test_format_migration(
        self,
        mock__format_opt,
        mock_format_replica_tasks_execution
    ):
        mock__format_opt.return_value = {
            "executions": [{'tasks': 'mock_id1'}],
            'tasks': 'mock_id2',
            'mock_key': 'mock_value'
        }
        mock_format_replica_tasks_execution.return_value = {
            'tasks': 'mock_id1'
        }

        expected_result = {
            'tasks': 'mock_id1',
            'mock_key': 'mock_value'
        }

        result = migration_view._format_migration("")

        self.assertEqual(
            expected_result,
            result
        )

    @mock.patch.object(view_utils, '_format_opt')
    def test_format_migration_no_tasks(
        self,
        mock__format_opt,
    ):
        mock__format_opt.return_value = {
            'mock_key': 'mock_value'
        }

        result = migration_view._format_migration("")

        self.assertEqual(
            mock__format_opt.return_value,
            result
        )

    @mock.patch.object(view_utils, '_format_opt')
    def test_format_migration_migration_dict_has_tasks(
        self,
        mock__format_opt,
    ):
        mock__format_opt.return_value = {
            'tasks': 'mock_id1',
            'mock_key': 'mock_value'
        }

        result = migration_view._format_migration("")

        self.assertEqual(
            mock__format_opt.return_value,
            result
        )
