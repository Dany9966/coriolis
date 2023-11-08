# Copyright 2022 Cloudbase Solutions Srl
# All Rights Reserved.

import itertools


def _format_opt(option, keys=None):
    def transform(key, value):
        if keys and key not in keys:
            return
        yield (key, value)

    return dict(itertools.chain.from_iterable(
        transform(k, v) for k, v in option.items()))
