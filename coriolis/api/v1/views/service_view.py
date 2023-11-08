# Copyright 2020 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import utils as view_utils


def _format_service(service, keys=None):
    service_dict = view_utils._format_opt(service)

    mapped_regions = service_dict.get('mapped_regions', [])
    service_dict['mapped_regions'] = [
        mapping['id'] for mapping in mapped_regions]

    return service_dict


def single(service):
    return {"service": _format_service(service)}


def collection(services):
    formatted_services = [
        _format_service(r) for r in services]
    return {'services': formatted_services}
