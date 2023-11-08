# Copyright 2020 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import utils as view_utils


def instance_single(instance):
    return {"instance": view_utils._format_opt(instance)}


def instances_collection(instances):
    formatted_instances = [view_utils._format_opt(m)
                           for m in instances]
    return {'instances': formatted_instances}


def network_single(network):
    return {"network": view_utils._format_opt(network)}


def networks_collection(networks):
    formatted_networks = [view_utils._format_opt(m)
                          for m in networks]
    return {'networks': formatted_networks}


def storage_collection(storage):
    formatted_storages = view_utils._format_opt(storage)
    return {'storage': formatted_storages}
