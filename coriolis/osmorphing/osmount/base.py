# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
# pylint: disable=anomalous-backslash-in-string

import abc
import base64
import os
import re

from oslo_log import log as logging
import paramiko
from six import with_metaclass

from coriolis import exception
from coriolis import utils

LOG = logging.getLogger(__name__)


class BaseOSMountTools(object, with_metaclass(abc.ABCMeta)):

    def __init__(self, connection_info, event_manager, ignore_devices):
        self._event_manager = event_manager
        self._ignore_devices = ignore_devices
        self._environment = {}
        self._connection_info = connection_info
        self._connect()

    @abc.abstractmethod
    def _connect(self):
        pass

    @abc.abstractmethod
    def get_connection(self):
        pass

    @abc.abstractmethod
    def check_os(self):
        pass

    def setup(self):
        pass

    @abc.abstractmethod
    def mount_os(self):
        pass

    @abc.abstractmethod
    def dismount_os(self, root_dir):
        pass

    def set_proxy(self, proxy_settings):
        pass

    def get_environment(self):
        return self._environment


class BaseSSHOSMountTools(BaseOSMountTools):
    @utils.retry_on_error(max_attempts=5, sleep_seconds=3)
    def _connect(self):
        connection_info = self._connection_info

        ip = connection_info["ip"]
        port = connection_info.get("port", 22)
        username = connection_info["username"]
        pkey = connection_info.get("pkey")
        password = connection_info.get("password")

        LOG.info("Waiting for connectivity on host: %(ip)s:%(port)s",
                 {"ip": ip, "port": port})
        utils.wait_for_port_connectivity(ip, port)

        self._event_manager.progress_update(
            "Connecting to SSH host: %(ip)s:%(port)s" %
            {"ip": ip, "port": port})
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=port, username=username, pkey=pkey,
                    password=password)
        self._ssh = ssh

    def setup(self):
        if self._allow_ssh_env_vars():
            self._ssh.close()
            self._connect()

    def _allow_ssh_env_vars(self):
        pass

    def _exec_cmd(self, cmd):
        return utils.exec_ssh_cmd(self._ssh, cmd, self._environment)

    def get_connection(self):
        return self._ssh


class BaseLinuxOSMountTools(BaseSSHOSMountTools):
    def _get_pvs(self):
        out = self._exec_cmd("sudo pvdisplay -c").decode().split("\n")
        pvs = {}
        for line in out:
            if line == "":
                continue
            line = line.strip().split(":")
            if pvs.get(line[1]) is None:
                pvs[line[1]] = [line[0], ]
            else:
                pvs[line[1]].append(line[0])
        return pvs

    def _get_vgnames(self):
        vg_names = []
        vgscan_out_lines = self._exec_cmd(
            "sudo vgscan").decode().split('\n')[1:-1]
        for vgscan_out_line in vgscan_out_lines:
            m = re.match(
                r'\s*Found volume group "(.*)" using metadata type lvm2',
                vgscan_out_line)
            if m:
                vg_names.append(m.groups()[0])
        return vg_names

    def _get_lv_paths(self):
        """ Returns list with paths of available LVM volumes. """
        lvm_paths = []
        out = self._exec_cmd("sudo lvdisplay -c").decode().strip()
        if out:
            LOG.debug("Decoded `lvdisplay` output data: %s", out)
            out_lines = out.split('\n')
            for line in out_lines:
                lvm_vol = line.strip().split(':')
                if lvm_vol:
                    lvm_paths.append(lvm_vol[0])

        LOG.debug("Found LVM device paths: %s", lvm_paths)
        return lvm_paths

    def _check_mount_fstab_partitions(
            self, os_root_dir, skip_mounts=["/", "/boot"],
            skip_filesystems=["swap"], mountable_lvm_devs=None):
        """ Reads the contents of /etc/fstab from the VM's root directory and
        tries to mount all clearly identified (by UUID or path) filesystems.
        Returns the list of the new directories which were mounted.
        param: skip_mounts: list(str()): list of directories (inside the
        chroot) to not try to mount.
        param: skip_filesystems: list(str()): list of filesystem types to skip
        mounting entirely
        param: mountable_lvm_devs: list(str()): list of LVM device paths which
        exist and are mountable should they appear in /etc/fstab
        """
        new_mountpoints = []
        etc_fstab_path = os.path.join(os_root_dir, "etc/fstab")
        if not utils.test_ssh_path(self._ssh, etc_fstab_path):
            LOG.warn(
                "etc/fstab file not found in '%s'. Cannot mount non-root dirs",
                os_root_dir)
            return []

        etc_fstab_raw = utils.read_ssh_file(self._ssh, etc_fstab_path)
        etc_fstab = etc_fstab_raw.decode('utf-8')

        LOG.debug(
            "Mounting non-root partitions from fstab file: %s" % (
                base64.b64encode(etc_fstab_raw)))

        # dictionary of the form {"mountpoint":
        #   {"device": "<dev>", "filesystem": "<fs>", "options": "<opts>"}}
        mounts = {}
        # fstab entry format:
        # <device> <mountpoint> <filesystem> <options> <dump> <fsck>
        fstab_entry_regex = (
            "^(\s*([^#\s]+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d)\s+(\d)\s*)$")
        for line in etc_fstab.splitlines():
            match = re.match(fstab_entry_regex, line)

            if not match:
                LOG.warn(
                    "Skipping unparseable /etc/fstab line: '%s'", line)
                continue

            device = match.group(2)
            mountpoint = match.group(3)
            if mountpoint in mounts:
                raise exception.CoriolisException(
                    "Mountpoint '%s' appears to be mounted twice in "
                    "'/etc/fstab'" % mountpoint)

            mounts[mountpoint] = {
                "device": device,
                "filesystem": match.group(4),
                "options": match.group(5)}

        # regexes for supported fstab device references:
        uuid_char_regex = "[0-9a-fA-F]"
        fs_uuid_regex = (
            "%(char)s{8}-%(char)s{4}-%(char)s{4}-"
            "%(char)s{4}-%(char)s{12}") % {"char": uuid_char_regex}
        fs_uuid_entry_regex = "^(UUID=%s)$" % fs_uuid_regex
        by_uuid_entry_regex = "^(/dev/disk/by-uuid/%s)$" % fs_uuid_regex
        if not mountable_lvm_devs:
            mountable_lvm_devs = []
        device_paths = self._get_device_file_paths(mountable_lvm_devs)
        for (mountpoint, details) in mounts.items():
            device = details['device']
            if (re.match(fs_uuid_entry_regex, device) is None and
                    re.match(by_uuid_entry_regex, device) is None):
                device_file_path = self._get_symlink_target(device)
                if device not in mountable_lvm_devs and (
                        device_file_path not in device_paths):
                    LOG.warn(
                        "Found fstab entry for dir %s which references device "
                        "%s. Only LVM volumes or devices referenced by UUID=* "
                        "or /dev/disk/by-uuid/* notation are supported. "
                        "Devicemapper paths for LVM volumes are also "
                        "supported. Skipping mounting directory." % (
                            mountpoint, device))
                    continue
            if mountpoint in skip_mounts:
                LOG.debug(
                    "Skipping undesired mount: %s: %s", mountpoint, details)
                continue
            if details["filesystem"] in skip_filesystems:
                LOG.debug(
                    "Skipping mounting undesired FS for device %s: %s",
                    device, details)
                continue

            LOG.debug("Attempting to mount fstab device: %s: %s",
                      device, details)
            # NOTE: `mountpoint` should always be an absolute path:
            chroot_mountpoint = "%s%s" % (os_root_dir, mountpoint)
            mountcmd = "sudo mount -t %s -o %s %s '%s'" % (
                details["filesystem"], details["options"],
                device, chroot_mountpoint)
            try:
                self._exec_cmd(mountcmd)
                new_mountpoints.append(chroot_mountpoint)
            except Exception:
                LOG.warn(
                    "Failed to run fstab filesystem mount command: '%s'. "
                    "Skipping mount. Error details: %s",
                    mountcmd, utils.get_exception_details())

        if new_mountpoints:
            LOG.info(
                "The following new /etc/fstab entries were successfully "
                "mounted: %s", new_mountpoints)

        return new_mountpoints

    def _get_symlink_target(self, symlink):
        target = None
        try:
            target = self._exec_cmd('readlink -en %s' % symlink).decode()
        except Exception:
            LOG.warn('Target not found for symlink: %s' % symlink)

        return target

    def _get_device_file_paths(self, symlink_list):
        """ Reads a list of symlink paths, such as `/dev/GROUP/VOLUME0` or
        `/dev/mapper/GROUP-VOLUME0` and returns a list of respective links'
        target device file paths, such as `/dev/dm0`
        """
        dev_file_paths = []
        for link in symlink_list:
            dev_file = self._get_symlink_target(link)
            if not dev_file:
                dev_file = link
            dev_file_paths.append(dev_file)
        return dev_file_paths

    def _get_mounted_devices(self):
        mounts = self._exec_cmd(
            "cat /proc/mounts").decode().split('\n')[:-1]
        ret = []
        for line in mounts:
            colls = line.split()
            if colls[0].startswith("/dev"):
                ret.append(colls[0])
        LOG.debug("Currently mounted devices: %s", ret)
        return ret

    def _get_mount_destinations(self):
        mounts = self._exec_cmd(
            "cat /proc/mounts").decode().split('\n')[:-1]
        ret = set()
        for line in mounts:
            colls = line.split()
            ret.add(colls[1])
        return ret

    def _get_volume_block_devices(self):
        # NOTE: depending on the version of the worker OS, scanning for just
        # the device NAME may lead to LVM volumes getting displayed as:
        # "<VG-name>-<LV-name> (dm-N)",
        #   where 'ln -s /dev/dm-N /dev/<VG-name>/<LV-name>'
        # Querying for the kernel device name (KNAME) should ensure we get the
        # device names we desire both for physical and logical volumes.
        volume_devs = self._exec_cmd(
            "lsblk -lnao KNAME").decode().split('\n')[:-1]
        LOG.debug("All block devices: %s", str(volume_devs))

        volume_devs = ["/dev/%s" % d for d in volume_devs if
                       not re.match(r"^.*\d+$", d)]

        LOG.debug("Ignoring block devices: %s", self._ignore_devices)
        volume_devs = [d for d in volume_devs if d
                       not in self._ignore_devices]

        LOG.info("Volume block devices: %s", volume_devs)
        return volume_devs

    def _find_dev_with_contents(self, devices, all_files=None,
                                one_of_files=None):
        if all_files and one_of_files:
            raise exception.CoriolisException(
                "all_files and one_of_files are mutually exclusive")
        dev_name = None
        for dev_path in devices:
            dirs = None
            tmp_dir = self._exec_cmd('mktemp -d').decode().split('\n')[0]
            try:
                self._exec_cmd('sudo mount %s %s' % (dev_path, tmp_dir))
                # NOTE: it's possible that the device was mounted successfully
                # but an I/O error occurs later along the line:
                dirs = self._exec_cmd('ls %s' % tmp_dir).decode().split('\n')
            except Exception:
                self._event_manager.progress_update(
                    "Failed to mount and scan device '%s'" % dev_path)
                LOG.warn(
                    "Failed to mount and scan device '%s':\n%s",
                    dev_path, utils.get_exception_details())
                utils.ignore_exceptions(self._exec_cmd)(
                    "sudo umount %s" % tmp_dir
                )
                utils.ignore_exceptions(self._exec_cmd)(
                    "sudo rmdir %s" % tmp_dir
                )
                continue

            LOG.debug("Contents of device %s:\n%s", dev_path, dirs)

            if all_files and dirs:
                common = [i if i in dirs else None for i in all_files]
                if not all(common):
                    self._exec_cmd('sudo umount %s' % tmp_dir)
                    continue

                dev_name = dev_path
                self._exec_cmd('sudo umount %s' % tmp_dir)
            elif one_of_files and dirs:
                common = [i for i in one_of_files if i in dirs]
                if len(common) > 0:
                    dev_name = dev_path
                    self._exec_cmd('sudo umount %s' % tmp_dir)
                    break
            else:
                self._exec_cmd('sudo umount %s' % tmp_dir)
                continue

        return dev_name

    def _find_and_mount_root(self, devices):
        files = ["etc", "bin", "sbin", "boot"]
        os_root_dir = None
        os_root_device = self._find_dev_with_contents(
            devices, all_files=files)

        if os_root_device is None:
            raise exception.OperatingSystemNotFound(
                "root partition not found")

        try:
            tmp_dir = self._exec_cmd('mktemp -d').decode().split('\n')[0]
            self._exec_cmd('sudo mount %s %s' % (os_root_device, tmp_dir))
            os_root_dir = tmp_dir
        except Exception:
            self._event_manager.progress_update(
                "Failed to mount root device '%s'" % os_root_device)
            LOG.warn(
                "Failed to mount root device '%s':\n%s",
                os_root_device, utils.get_exception_details())
            utils.ignore_exceptions(self._exec_cmd)(
                "sudo umount %s" % tmp_dir
            )
            utils.ignore_exceptions(self._exec_cmd)(
                "sudo rmdir %s" % tmp_dir
            )
            raise

        for directory in ['proc', 'sys', 'dev', 'run']:
            mount_dir = os.path.join(os_root_dir, directory)
            if not utils.test_ssh_path(self._ssh, mount_dir):
                LOG.info(
                    "No '%s' directory in mounted OS. Skipping mount.",
                    directory)
                continue
            self._exec_cmd(
                'sudo mount -o bind /%(dir)s/ %(mount_dir)s' %
                {'dir': directory, 'mount_dir': mount_dir})

        if os_root_device in devices:
            devices.remove(os_root_device)

        return os_root_dir, os_root_device

    def mount_os(self):
        dev_paths = []
        mounted_devs = self._get_mounted_devices()

        volume_devs = self._get_volume_block_devices()
        for volume_dev in volume_devs:
            self._exec_cmd("sudo partx -v -a %s || true" % volume_dev)
            devs = self._exec_cmd(
                "sudo ls -l %s*" % volume_dev).decode().split('\n')[:-1]
            dev_paths += [d.split()[-1] for d in devs
                          if re.match(r"^.*\d+$", d)]

        pvs = self._get_pvs()
        for vg_name in self._get_vgnames():
            found = False
            for pv in pvs[vg_name]:
                if pv in dev_paths:
                    found = True
                    break
            if not found:
                continue
            self._exec_cmd("sudo vgchange -ay %s" % vg_name)
            lvm_dev_paths = self._exec_cmd(
                "sudo ls /dev/%s/*" % vg_name).decode().split('\n')[:-1]
            dev_paths += lvm_dev_paths

        valid_filesystems = ['ext2', 'ext3', 'ext4', 'xfs', 'btrfs']

        dev_paths_to_mount = []
        for dev_path in dev_paths:
            if dev_path in mounted_devs:
                # this device is already mounted. Skip it, as it most likely
                # means this device belongs to the worker VM.
                continue
            fs_type = self._exec_cmd(
                "sudo blkid -o value -s TYPE %s || true" %
                dev_path).decode().split('\n')[0]
            if fs_type in valid_filesystems:
                if fs_type == "xfs":
                    utils.run_xfs_repair(self._ssh, dev_path)
                else:
                    utils.check_fs(self._ssh, fs_type, dev_path)
                dev_paths_to_mount.append(dev_path)

        os_root_dir, os_root_device = self._find_and_mount_root(
            dev_paths_to_mount)

        grub_dirs = ["grub", "grub2"]
        os_boot_device = self._find_dev_with_contents(
            dev_paths_to_mount, one_of_files=grub_dirs)

        if os_boot_device:
            LOG.debug("Mounting boot device '%s'", os_boot_device)
            self._exec_cmd(
                'sudo mount %s "%s/boot"' % (
                    os_boot_device, os_root_dir))

        lvm_devs = list(set(self._get_lv_paths()) - set(mounted_devs))
        self._check_mount_fstab_partitions(
            os_root_dir, mountable_lvm_devs=lvm_devs)

        return os_root_dir, os_root_device

    def dismount_os(self, root_dir):
        mounted_fs = self._get_mount_destinations()
        # Sort all mounted filesystems by length. This will ensure that
        # the first in the list is a subfolder of the next in the list,
        # and we unmount them in the proper order
        mounted_fs = list(reversed(sorted(mounted_fs)))
        for d in mounted_fs:
            if d.startswith(root_dir):
                # mounted filesystem is a subfolder of our root_dir
                self._exec_cmd('sudo umount %s' % d)

    def set_proxy(self, proxy_settings):
        url = proxy_settings.get('url')
        if not url:
            return

        username = proxy_settings.get('username')
        if username:
            password = proxy_settings.get('password', '')
            url = utils.get_url_with_credentials(url, username, password)

        LOG.debug("Proxy URL: %s", url)
        for var in ['http_proxy', 'https_proxy', 'ftp_proxy']:
            self._environment[var] = url
            # Some commands look for the uppercase var name
            self._environment[var.upper()] = url

        no_proxy = proxy_settings.get('no_proxy')
        if no_proxy:
            LOG.debug("Proxy exclusions: %s", no_proxy)
            self._environment["no_proxy"] = '.'.join(no_proxy)
