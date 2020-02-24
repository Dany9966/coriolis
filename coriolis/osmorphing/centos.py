# Copyright 2020 Cloudbase Solutions Srl
# All Rights Reserved.

import re

from coriolis.osmorphing import redhat


class BaseCentOsMorphingTools(redhat.BaseRedHatMorphingTools):
    def _check_os(self):
        centos_release_path = "etc/centos-release"
        if self._test_path(centos_release_path):
            release_info = self._read_file(
                centos_release_path).decode().splitlines()
            if release_info:
                m = re.match(r"^(.*) release ([0-9].*) \((.*)\).*$",
                             release_info[0].strip())
                if m:
                    distro, version, _ = m.groups()
                    return (distro, version)
