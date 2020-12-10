# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.

import os
from io import StringIO

from oslo_log import log as logging
import yaml

from coriolis import exception
from coriolis import utils
from coriolis.osmorphing import base
from coriolis.osmorphing.osdetect import debian as debian_osdetect

LOG = logging.getLogger(__name__)

DEBIAN_DISTRO_IDENTIFIER = debian_osdetect.DEBIAN_DISTRO_IDENTIFIER

LO_NIC_TPL = """
auto lo
iface lo inet loopback
"""

INTERFACES_NIC_TPL = """
auto %(device_name)s
iface %(device_name)s inet dhcp
"""


class BaseDebianMorphingTools(base.BaseLinuxOSMorphingTools):

    @classmethod
    def check_os_supported(cls, detected_os_info):
        if detected_os_info['distribution_name'] != (
                DEBIAN_DISTRO_IDENTIFIER):
            return False
        return cls._version_supported_util(
            detected_os_info['release_version'], minimum=8)

    def disable_predictable_nic_names(self):
        grub_cfg = os.path.join(
            self._os_root_dir,
            "etc/default/grub")
        if self._test_path(grub_cfg) is False:
            return
        contents = self._read_file(grub_cfg).decode()
        cfg = utils.Grub2ConfigEditor(contents)
        cfg.append_to_option(
            "GRUB_CMDLINE_LINUX_DEFAULT",
            {"opt_type": "key_val", "opt_key": "net.ifnames", "opt_val": 0})
        cfg.append_to_option(
            "GRUB_CMDLINE_LINUX_DEFAULT",
            {"opt_type": "key_val", "opt_key": "biosdevname", "opt_val": 0})
        cfg.append_to_option(
            "GRUB_CMDLINE_LINUX",
            {"opt_type": "key_val", "opt_key": "net.ifnames", "opt_val": 0})
        cfg.append_to_option(
            "GRUB_CMDLINE_LINUX",
            {"opt_type": "key_val", "opt_key": "biosdevname", "opt_val": 0})
        self._write_file_sudo("etc/default/grub", cfg.dump())
        self._exec_cmd_chroot("/usr/sbin/update-grub")

    def _compose_interfaces_config(self, nics_info):
        fp = StringIO()
        fp.write(LO_NIC_TPL)
        fp.write("\n\n")
        for idx, _ in enumerate(nics_info):
            dev_name = "eth%d" % idx
            cfg = INTERFACES_NIC_TPL % {
                "device_name": dev_name,
            }
            fp.write(cfg)
            fp.write("\n\n")
        fp.seek(0)
        return fp.read()

    def _compose_netplan_cfg(self, nics_info):
        cfg = {
            "network": {
                "version": 2,
                "ethernets": {
                    "lo": {
                        "match": {
                            "name": "lo"
                        },
                        "addresses": ["127.0.0.1/8"]
                    }
                }
            }
        }
        for idx, _ in enumerate(nics_info):
            cfg["network"]["ethernets"]["eth%d" % idx] = {
                "dhcp4": True,
                "dhcp6": True,
            }
        return yaml.dump(cfg, default_flow_style=False)

    def _get_interfaces_info(self, interfaces_path, mac_addresses):
        interfaces = dict()
        paths = [interfaces_path]

        def _parse_iface_file(interface_file, mac_addresses):
            nonlocal interfaces
            nonlocal paths
            curr_iface = None
            curr_mac_address = None
            interfaces_contents = self._read_file(interface_file).decode()
            LOG.debug(
                "Fetched %s contents: %s", interface_file, interfaces_contents)
            for line in interfaces_contents.splitlines():
                if line.strip().startswith("iface"):
                    words = line.split()
                    if len(words) > 1:
                        curr_iface = words[1]
                elif line.strip().startswith("hwaddress ether"):
                    words = line.split()
                    if len(words) > 2:
                        if not curr_iface:
                            LOG.warn("Found MAC address %s does not belong to "
                                     "any interface stanza. Skipping.",
                                     words[2])
                            continue

                        curr_mac_address = words[2]
                        if curr_mac_address.lower() not in mac_addresses:
                            LOG.warn(
                                "Found MAC address %s for interface '%s' is "
                                "not one of the MAC addresses fetched by "
                                "Coriolis for this instance: %s",
                                curr_mac_address, curr_iface, mac_addresses)
                        interfaces[curr_iface] = curr_mac_address
                elif line.strip().startswith("source"):
                    words = line.split()
                    if len(words) > 1:
                        source_path = words[2]
                        paths += self._exec_cmd_chroot(
                            'ls -1 %s' % source_path).splitlines()

        while paths:
            _parse_iface_file(paths[0], mac_addresses)
            paths.pop(0)

        return interfaces

    def _get_netplan_info(self, netplan_base_path, mac_addresses):
        interfaces = dict()
        netplan_cfgs = [n for n in self._list_dir(netplan_base_path)
                        if n.endswith(".yaml") or n.endswith(".yml")]
        for cfg in netplan_cfgs:
            cfg_path = "%s/%s" % (netplan_base_path, cfg)
            try:
                contents = yaml.safe_load(self._read_file(cfg_path).decode())
                ifaces = contents.get('network', {}).get('ethernets', {})
                for iface, net_cfg in ifaces.items():
                    mac_address = net_cfg.get('match', {}).get('macaddress')
                    if mac_address:
                        if mac_address not in mac_addresses:
                            LOG.warn(
                                "Found MAC address %s for interface '%s' is "
                                "not one of the MAC addresses fetched by "
                                "Coriolis for this instance: %s",
                                mac_address, iface, mac_addresses)
                        interfaces[iface] = mac_address
            except yaml.YAMLError:
                LOG.warn(
                    "Could not parse netplan configuration '%s'. Invalid YAML "
                    "file: %s", cfg_path, utils.get_exception_details())

        return interfaces

    def set_net_config(self, nics_info, dhcp):
        ifaces_file = "/etc/network/interfaces"
        netplan_base = "etc/netplan"

        if not dhcp:
            mac_addresses = [nic.get('mac_address') for nic in nics_info]

            if self._test_path(ifaces_file):
                net_ifaces_info = self._get_interfaces_info(
                    ifaces_file, mac_addresses)
            elif self._test_path(netplan_base):
                net_ifaces_info = self._get_netplan_info(
                    netplan_base, mac_addresses)

            self._add_net_udev_rules(net_ifaces_info.items())
            return

        self.disable_predictable_nic_names()
        if self._test_path("/etc/network"):
            contents = self._compose_interfaces_config(nics_info)
            if self._test_path(ifaces_file):
                self._exec_cmd_chroot(
                    "cp %s %s.bak" % (ifaces_file, ifaces_file))
            self._write_file_sudo(ifaces_file, contents)

        if self._test_path(netplan_base):
            curr_files = self._list_dir(netplan_base)
            for cnf in curr_files:
                if cnf.endswith(".yaml") or cnf.endswith(".yml"):
                    pth = "%s/%s" % (netplan_base, cnf)
                    self._exec_cmd_chroot(
                        "mv %s %s.bak" % (pth, pth)
                    )
            new_cfg = self._compose_netplan_cfg(nics_info)
            cfg_name = "%s/coriolis_netplan.yaml" % netplan_base
            self._write_file_sudo(cfg_name, new_cfg)

    def pre_packages_install(self, package_names):
        super(BaseDebianMorphingTools, self).pre_packages_install(
            package_names)
        try:
            if package_names:
                self._event_manager.progress_update("Updating packages list")
                self._exec_cmd_chroot('apt-get clean')
                self._exec_cmd_chroot('apt-get update -y')
        except Exception as err:
            raise exception.PackageManagerOperationException(
                "Failed to refresh apt repositories. Please ensure that *all* "
                "of the apt repositories configured within the source machine "
                "exist, are properly configured, and are reachable from the "
                "virtual network on the target platform which the OSMorphing "
                "minion machine is running on. If there are repositories "
                "configured within the source machine which are local, "
                "private, or otherwise unreachable from the target platform, "
                "please either try disabling the repositories within the "
                "source machine, or try to set up a mirror of said "
                "repositories which will be reachable from the temporary "
                "OSMorphing minion machine on the target platform. Original "
                "error was: %s" % str(err)) from err

    def install_packages(self, package_names):
        try:
            apt_get_cmd = 'apt-get install %s -y' % " ".join(package_names)
            self._exec_cmd_chroot(apt_get_cmd)
        except Exception as err:
            raise exception.FailedPackageInstallationException(
                package_names=package_names, package_manager='apt',
                error=str(err)) from err

    def uninstall_packages(self, package_names):
        try:
            for package_name in package_names:
                apt_get_cmd = 'apt-get remove %s -y || true' % package_name
                self._exec_cmd_chroot(apt_get_cmd)
        except exception.CoriolisException as err:
            raise exception.FailedPackageUninstallationException(
                package_names=package_names, package_manager='apt',
                error=str(err)) from err
