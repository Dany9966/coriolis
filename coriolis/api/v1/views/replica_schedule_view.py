# Copyright 2017 Cloudbase Solutions Srl
# All Rights Reserved.

from coriolis.api.v1.views import utils as view_utils


def single(schedule):
    return {"schedule": view_utils._format_opt(schedule)}


def collection(schedules):
    formatted_schedules = [view_utils._format_opt(m)
                           for m in schedules]
    return {'schedules': formatted_schedules}
