# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import utils as view_utils


def _format_endpoint(endpoint, keys=None):
    endpoint_dict = view_utils._format_opt(endpoint)
    mapped_regions = endpoint_dict.get('mapped_regions', [])
    endpoint_dict['mapped_regions'] = [
        reg['id'] for reg in mapped_regions]

    return endpoint_dict


def single(endpoint):
    return {"endpoint": _format_endpoint(endpoint)}


def collection(endpoints):
    formatted_endpoints = [_format_endpoint(m)
                           for m in endpoints]
    return {'endpoints': formatted_endpoints}
