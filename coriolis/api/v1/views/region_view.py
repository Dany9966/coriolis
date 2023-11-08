# Copyright 2020 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import utils as view_utils


def _format_region(region, keys=None):
    region_dict = view_utils._format_opt(region)

    mapped_endpoints = region_dict.get('mapped_endpoints', [])
    region_dict['mapped_endpoints'] = [
        endp['id'] for endp in mapped_endpoints]

    mapped_services = region_dict.get('mapped_services', [])
    region_dict['mapped_services'] = [
        svc['id'] for svc in mapped_services]

    return region_dict


def single(region):
    return {"region": _format_region(region)}


def collection(regions):
    formatted_regions = [
        _format_region(r) for r in regions]
    return {'regions': formatted_regions}
