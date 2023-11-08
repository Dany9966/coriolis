# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import replica_tasks_execution_view as view
from coriolis.api.v1.views import utils as view_utils


def _format_replica(replica, keys=None):
    replica_dict = view_utils._format_opt(replica)

    executions = replica_dict.get('executions', [])
    replica_dict['executions'] = [
        view.format_replica_tasks_execution(ex)
        for ex in executions]

    return replica_dict


def single(replica):
    return {"replica": _format_replica(replica)}


def collection(replicas):
    formatted_replicas = [_format_replica(m)
                          for m in replicas]
    return {'replicas': formatted_replicas}
