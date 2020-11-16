# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.

DEFAULT_CORIOLIS_REGION_NAME = "Default Region"

EXECUTION_STATUS_UNEXECUTED = "UNEXECUTED"
EXECUTION_STATUS_RUNNING = "RUNNING"
EXECUTION_STATUS_COMPLETED = "COMPLETED"
EXECUTION_STATUS_ERROR = "ERROR"
EXECUTION_STATUS_DEADLOCKED = "DEADLOCKED"
EXECUTION_STATUS_CANCELED = "CANCELED"
EXECUTION_STATUS_CANCELLING = "CANCELLING"
EXECUTION_STATUS_CANCELED_FOR_DEBUGGING = "CANCELED_FOR_DEBUGGING"
EXECUTION_STATUS_AWAITING_MINION_ALLOCATIONS = "AWAITING_MINION_ALLOCATIONS"
EXECUTION_STATUS_ERROR_ALLOCATING_MINIONS = "ERROR_ALLOCATING_MINIONS"

ACTIVE_EXECUTION_STATUSES = [
    EXECUTION_STATUS_RUNNING,
    EXECUTION_STATUS_CANCELLING,
    EXECUTION_STATUS_AWAITING_MINION_ALLOCATIONS
]

FINALIZED_EXECUTION_STATUSES = [
    EXECUTION_STATUS_COMPLETED,
    EXECUTION_STATUS_CANCELED,
    EXECUTION_STATUS_ERROR,
    EXECUTION_STATUS_CANCELED_FOR_DEBUGGING,
    EXECUTION_STATUS_DEADLOCKED,
    EXECUTION_STATUS_ERROR_ALLOCATING_MINIONS
]

TASK_STATUS_SCHEDULED = "SCHEDULED"
TASK_STATUS_PENDING = "PENDING"
TASK_STATUS_STARTING = "STARTING"
TASK_STATUS_UNSCHEDULED = "UNSCHEDULED"
TASK_STATUS_RUNNING = "RUNNING"
TASK_STATUS_COMPLETED = "COMPLETED"
TASK_STATUS_ERROR = "ERROR"
TASK_STATUS_FORCE_CANCELED = "FORCE_CANCELED"
TASK_STATUS_FAILED_TO_CANCEL = "FAILED_TO_CANCEL"
TASK_STATUS_CANCELED = "CANCELED"
TASK_STATUS_CANCELED_AFTER_COMPLETION = "CANCELED_AFTER_COMPLETION"
TASK_STATUS_CANCELLING = "CANCELLING"
TASK_STATUS_CANCELLING_AFTER_COMPLETION = "CANCELLING_AFTER_COMPLETION"
TASK_STATUS_CANCELED_FOR_DEBUGGING = "CANCELED_FOR_DEBUGGING"
TASK_STATUS_CANCELED_FROM_DEADLOCK = "STRANDED_AFTER_DEADLOCK"
TASK_STATUS_ON_ERROR_ONLY = "EXECUTE_ON_ERROR_ONLY"
TASK_STATUS_FAILED_TO_SCHEDULE = "FAILED_TO_SCHEDULE"

ACTIVE_TASK_STATUSES = [
    TASK_STATUS_PENDING,
    TASK_STATUS_STARTING,
    TASK_STATUS_RUNNING,
    TASK_STATUS_CANCELLING,
    TASK_STATUS_CANCELLING_AFTER_COMPLETION
]

CANCELED_TASK_STATUSES = [
    TASK_STATUS_CANCELED,
    TASK_STATUS_UNSCHEDULED,
    TASK_STATUS_FORCE_CANCELED,
    TASK_STATUS_CANCELED_AFTER_COMPLETION,
    TASK_STATUS_CANCELED_FOR_DEBUGGING,
    TASK_STATUS_CANCELED_FROM_DEADLOCK,
    TASK_STATUS_FAILED_TO_SCHEDULE,
    TASK_STATUS_FAILED_TO_CANCEL
]

FINALIZED_TASK_STATUSES = [
    TASK_STATUS_COMPLETED,
    TASK_STATUS_ERROR,
    TASK_STATUS_UNSCHEDULED,
    TASK_STATUS_CANCELED,
    TASK_STATUS_FORCE_CANCELED,
    TASK_STATUS_CANCELED_FOR_DEBUGGING,
    TASK_STATUS_CANCELED_FROM_DEADLOCK,
    TASK_STATUS_CANCELED_AFTER_COMPLETION,
    TASK_STATUS_FAILED_TO_SCHEDULE,
    TASK_STATUS_FAILED_TO_CANCEL
]

TASK_TYPE_DEPLOY_MIGRATION_SOURCE_RESOURCES = (
    "DEPLOY_MIGRATION_SOURCE_RESOURCES")
TASK_TYPE_DEPLOY_MIGRATION_TARGET_RESOURCES = (
    "DEPLOY_MIGRATION_TARGET_RESOURCES")
TASK_TYPE_DELETE_MIGRATION_SOURCE_RESOURCES = (
    "DELETE_MIGRATION_SOURCE_RESOURCES")
TASK_TYPE_DELETE_MIGRATION_TARGET_RESOURCES = (
    "DELETE_MIGRATION_TARGET_RESOURCES")
TASK_TYPE_DEPLOY_INSTANCE_RESOURCES = "DEPLOY_INSTANCE_RESOURCES"
TASK_TYPE_FINALIZE_INSTANCE_DEPLOYMENT = "FINALIZE_INSTANCE_DEPLOYMENT"
TASK_TYPE_CLEANUP_FAILED_INSTANCE_DEPLOYMENT = (
    "CLEANUP_FAILED_INSTANCE_DEPLOYMENT")
TASK_TYPE_CLEANUP_INSTANCE_SOURCE_STORAGE = (
    "CLEANUP_INSTANCE_SOURCE_STORAGE")
TASK_TYPE_CLEANUP_INSTANCE_TARGET_STORAGE = (
    "CLEANUP_INSTANCE_TARGET_STORAGE")

TASK_TYPE_CREATE_INSTANCE_DISKS = "CREATE_INSTANCE_DISKS"

TASK_TYPE_DEPLOY_OS_MORPHING_RESOURCES = "DEPLOY_OS_MORPHING_RESOURCES"
TASK_TYPE_OS_MORPHING = "OS_MORPHING"
TASK_TYPE_DELETE_OS_MORPHING_RESOURCES = "DELETE_OS_MORPHING_RESOURCES"

TASK_TYPE_GET_INSTANCE_INFO = "GET_INSTANCE_INFO"
TASK_TYPE_DEPLOY_REPLICA_DISKS = "DEPLOY_REPLICA_DISKS"
TASK_TYPE_DELETE_REPLICA_SOURCE_DISK_SNAPSHOTS = (
    "DELETE_REPLICA_SOURCE_DISK_SNAPSHOTS")
TASK_TYPE_DELETE_REPLICA_DISKS = "DELETE_REPLICA_DISKS"
TASK_TYPE_REPLICATE_DISKS = "REPLICATE_DISKS"
TASK_TYPE_DEPLOY_REPLICA_SOURCE_RESOURCES = "DEPLOY_REPLICA_SOURCE_RESOURCES"
TASK_TYPE_DELETE_REPLICA_SOURCE_RESOURCES = "DELETE_REPLICA_SOURCE_RESOURCES"
TASK_TYPE_DEPLOY_REPLICA_TARGET_RESOURCES = "DEPLOY_REPLICA_TARGET_RESOURCES"
TASK_TYPE_DELETE_REPLICA_TARGET_RESOURCES = "DELETE_REPLICA_TARGET_RESOURCES"
TASK_TYPE_SHUTDOWN_INSTANCE = "SHUTDOWN_INSTANCE"
TASK_TYPE_DEPLOY_REPLICA_INSTANCE_RESOURCES = (
    "DEPLOY_REPLICA_INSTANCE_RESOURCES")
TASK_TYPE_FINALIZE_REPLICA_INSTANCE_DEPLOYMENT = (
    "FINALIZE_REPLICA_INSTANCE_DEPLOYMENT")
TASK_TYPE_CLEANUP_FAILED_REPLICA_INSTANCE_DEPLOYMENT = (
    "CLEANUP_FAILED_REPLICA_INSTANCE_DEPLOYMENT")
TASK_TYPE_CREATE_REPLICA_DISK_SNAPSHOTS = "CREATE_REPLICA_DISK_SNAPSHOTS"
TASK_TYPE_DELETE_REPLICA_TARGET_DISK_SNAPSHOTS = (
    "DELETE_REPLICA_TARGET_DISK_SNAPSHOTS")
TASK_TYPE_RESTORE_REPLICA_DISK_SNAPSHOTS = "RESTORE_REPLICA_DISK_SNAPSHOTS"
TASK_TYPE_GET_OPTIMAL_FLAVOR = "GET_OPTIMAL_FLAVOR"
TASK_TYPE_VALIDATE_MIGRATION_SOURCE_INPUTS = (
    "VALIDATE_MIGRATION_SOURCE_INPUTS")
TASK_TYPE_VALIDATE_MIGRATION_DESTINATION_INPUTS = (
    "VALIDATE_MIGRATION_DESTINATION_INPUTS")
TASK_TYPE_VALIDATE_REPLICA_SOURCE_INPUTS = "VALIDATE_REPLICA_SOURCE_INPUTS"
TASK_TYPE_VALIDATE_REPLICA_DESTINATION_INPUTS = (
    "VALIDATE_REPLICA_DESTINATION_INPUTS")
TASK_TYPE_VALIDATE_REPLICA_DEPLOYMENT_INPUTS = (
    "VALIDATE_REPLICA_DEPLOYMENT_INPUTS")
TASK_TYPE_UPDATE_SOURCE_REPLICA = "UPDATE_SOURCE_REPLICA"
TASK_TYPE_UPDATE_DESTINATION_REPLICA = "UPDATE_DESTINATION_REPLICA"

TASK_TYPE_VALIDATE_SOURCE_MINION_POOL_OPTIONS = (
    "VALIDATE_SOURCE_MINION_POOL_ENVIRONMENT_OPTIONS")
TASK_TYPE_VALIDATE_DESTINATION_MINION_POOL_OPTIONS = (
    "VALIDATE_DESTINATION_MINION_POOL_ENVIRONMENT_OPTIONS")
TASK_TYPE_CREATE_SOURCE_MINION_MACHINE = "CREATE_SOURCE_MINION_MACHINE"
TASK_TYPE_CREATE_DESTINATION_MINION_MACHINE = (
    "CREATE_DESTINATION_MINION_MACHINE")
TASK_TYPE_DELETE_SOURCE_MINION_MACHINE = "DELETE_SOURCE_MINION_MACHINE"
TASK_TYPE_DELETE_DESTINATION_MINION_MACHINE = (
    "DELETE_DESTINATION_MINION_MACHINE")
TASK_TYPE_SET_UP_SOURCE_POOL_SHARED_RESOURCES = (
    "SET_UP_SOURCE_POOL_SHARED_RESOURCES")
TASK_TYPE_SET_UP_DESTINATION_POOL_SHARED_RESOURCES = (
    "SET_UP_DESTINATION_POOL_SHARED_RESOURCES")
TASK_TYPE_TEAR_DOWN_SOURCE_POOL_SHARED_RESOURCES = (
    "TEAR_DOWN_SOURCE_POOL_SHARED_RESOURCES")
TASK_TYPE_TEAR_DOWN_DESTINATION_POOL_SHARED_RESOURCES = (
    "TEAR_DOWN_DESTINATION_POOL_SHARED_RESOURCES")
TASK_TYPE_ATTACH_VOLUMES_TO_SOURCE_MINION = "ATTACH_VOLUMES_TO_SOURCE_MINION"
TASK_TYPE_DETACH_VOLUMES_FROM_SOURCE_MINION = (
    "DETACH_VOLUMES_FROM_SOURCE_MINION")
TASK_TYPE_ATTACH_VOLUMES_TO_DESTINATION_MINION = (
    "ATTACH_VOLUMES_TO_DESTINATION_MINION")
TASK_TYPE_DETACH_VOLUMES_FROM_DESTINATION_MINION = (
    "DETACH_VOLUMES_FROM_DESTINATION_MINION")
TASK_TYPE_ATTACH_VOLUMES_TO_OSMORPHING_MINION = (
    "ATTACH_VOLUMES_TO_OSMORPHING_MINION")
TASK_TYPE_DETACH_VOLUMES_FROM_OSMORPHING_MINION = (
    "DETACH_VOLUMES_FROM_OSMORPHING_MINION")
TASK_TYPE_VALIDATE_SOURCE_MINION_POOL_COMPATIBILITY = (
    "VALIDATE_SOURCE_MINION_POOL_COMPATIBILITY")
TASK_TYPE_VALIDATE_DESTINATION_MINION_POOL_COMPATIBILITY = (
    "VALIDATE_DESTINATION_MINION_POOL_COMPATIBILITY")
TASK_TYPE_VALIDATE_OSMORPHING_MINION_POOL_COMPATIBILITY = (
    "VALIDATE_OSMORPHING_MINION_POOL_COMPATIBILITY")
TASK_TYPE_RELEASE_SOURCE_MINION = "RELEASE_SOURCE_MINION"
TASK_TYPE_RELEASE_DESTINATION_MINION = "RELEASE_DESTINATION_MINION"
TASK_TYPE_RELEASE_OSMORPHING_MINION = "RELEASE_OSMORPHING_MINION"
TASK_TYPE_COLLECT_OSMORPHING_INFO = "COLLECT_OS_MORPHING_INFO"
TASK_TYPE_HEALTHCHECK_SOURCE_MINION = "HEALTHCHECK_SOURCE_MINION"
TASK_TYPE_HEALTHCHECK_DESTINATION_MINION = "HEALTHCHECK_DESTINATION_MINION"

MINION_POOL_OPERATIONS_TASKS = [
    TASK_TYPE_VALIDATE_SOURCE_MINION_POOL_OPTIONS,
    TASK_TYPE_VALIDATE_DESTINATION_MINION_POOL_OPTIONS,
    TASK_TYPE_SET_UP_SOURCE_POOL_SHARED_RESOURCES,
    TASK_TYPE_SET_UP_DESTINATION_POOL_SHARED_RESOURCES,
    TASK_TYPE_CREATE_SOURCE_MINION_MACHINE,
    TASK_TYPE_CREATE_DESTINATION_MINION_MACHINE,
    TASK_TYPE_TEAR_DOWN_SOURCE_POOL_SHARED_RESOURCES,
    TASK_TYPE_TEAR_DOWN_DESTINATION_POOL_SHARED_RESOURCES,
    TASK_TYPE_HEALTHCHECK_SOURCE_MINION,
    TASK_TYPE_HEALTHCHECK_DESTINATION_MINION
]

TASK_PLATFORM_SOURCE = "source"
TASK_PLATFORM_DESTINATION = "destination"
TASK_PLATFORM_BILATERAL = "bilateral"

PROVIDER_PLATFORM_SOURCE = "source"
PROVIDER_PLATFORM_DESTINATION = "destination"

PROVIDER_TYPE_IMPORT = 1
PROVIDER_TYPE_EXPORT = 2
PROVIDER_TYPE_REPLICA_IMPORT = 4
PROVIDER_TYPE_REPLICA_EXPORT = 8
PROVIDER_TYPE_ENDPOINT = 16
PROVIDER_TYPE_ENDPOINT_INSTANCES = 32
PROVIDER_TYPE_OS_MORPHING = 64
PROVIDER_TYPE_ENDPOINT_NETWORKS = 128
PROVIDER_TYPE_INSTANCE_FLAVOR = 256
PROVIDER_TYPE_DESTINATION_ENDPOINT_OPTIONS = 512
PROVIDER_TYPE_SETUP_LIBS = 1024
PROVIDER_TYPE_VALIDATE_MIGRATION_EXPORT = 2048
PROVIDER_TYPE_VALIDATE_REPLICA_EXPORT = 4096
PROVIDER_TYPE_VALIDATE_MIGRATION_IMPORT = 8192
PROVIDER_TYPE_VALIDATE_REPLICA_IMPORT = 16384
PROVIDER_TYPE_ENDPOINT_STORAGE = 32768
PROVIDER_TYPE_SOURCE_REPLICA_UPDATE = 65536
PROVIDER_TYPE_SOURCE_ENDPOINT_OPTIONS = 131072
PROVIDER_TYPE_DESTINATION_REPLICA_UPDATE = 262144
PROVIDER_TYPE_SOURCE_MINION_POOL = 524288
PROVIDER_TYPE_DESTINATION_MINION_POOL = 1048576

DISK_FORMAT_VMDK = 'vmdk'
DISK_FORMAT_RAW = 'raw'
DISK_FORMAT_QCOW = "qcow"
DISK_FORMAT_QCOW2 = 'qcow2'
DISK_FORMAT_VHD = 'vhd'
DISK_FORMAT_VHDX = 'vhdx'

DISK_ALLOCATION_TYPE_STATIC = "static"
DISK_ALLOCATION_TYPE_DYNAMIC = "dynamic"

FIRMWARE_TYPE_BIOS = 'BIOS'
FIRMWARE_TYPE_EFI = 'EFI'

HYPERVISOR_VMWARE = "vmware"
HYPERVISOR_HYPERV = "hyperv"
HYPERVISOR_QEMU = "qemu"
HYPERVISOR_KVM = "kvm"
HYPERVISOR_XENSERVER = "xenserver"

TASK_EVENT_INFO = "INFO"
TASK_EVENT_WARNING = "WARNING"
TASK_EVENT_ERROR = "ERROR"

MINION_POOL_EVENT_INFO = "INFO"
MINION_POOL_EVENT_WARNING = "WARNING"
MINION_POOL_EVENT_ERROR = "ERROR"

OS_TYPE_BSD = "bsd"
OS_TYPE_LINUX = "linux"
OS_TYPE_OS_X = "osx"
OS_TYPE_SOLARIS = "solaris"
OS_TYPE_WINDOWS = "windows"
OS_TYPE_OTHER = "other"
OS_TYPE_UNKNOWN = "unknown"

DEFAULT_OS_TYPE = OS_TYPE_LINUX

VALID_OS_TYPES = [
    OS_TYPE_BSD, OS_TYPE_LINUX, OS_TYPE_OS_X, OS_TYPE_SOLARIS, OS_TYPE_WINDOWS]

TMP_DIRS_KEY = "__tmp_dirs"

COMPRESSION_FORMAT_GZIP = "gzip"
COMPRESSION_FORMAT_ZLIB = "zlib"

VALID_COMPRESSION_FORMATS = [
    COMPRESSION_FORMAT_GZIP,
    COMPRESSION_FORMAT_ZLIB
]

EXECUTION_TYPE_REPLICA_EXECUTION = "replica_execution"
EXECUTION_TYPE_REPLICA_DISKS_DELETE = "replica_disks_delete"
EXECUTION_TYPE_REPLICA_DEPLOY = "replica_deploy"
EXECUTION_TYPE_MIGRATION = "migration"
EXECUTION_TYPE_REPLICA_UPDATE = "replica_update"
EXECUTION_TYPE_MINION_POOL_MAINTENANCE = "minion_pool_maintenance"
EXECUTION_TYPE_MINION_POOL_UPDATE = "minion_pool_update"
EXECUTION_TYPE_MINION_POOL_SET_UP_SHARED_RESOURCES = (
    "minion_pool_set_up_shared_resources")
EXECUTION_TYPE_MINION_POOL_TEAR_DOWN_SHARED_RESOURCES = (
    "minion_pool_tear_down_shared_resources")
EXECUTION_TYPE_MINION_POOL_ALLOCATE_MINIONS = "minion_pool_allocate_minions"
EXECUTION_TYPE_MINION_POOL_DEALLOCATE_MINIONS = (
    "minion_pool_deallocate_minions")

MINION_POOL_EXECUTION_TYPES = [
    EXECUTION_TYPE_MINION_POOL_MAINTENANCE,
    EXECUTION_TYPE_MINION_POOL_UPDATE,
    EXECUTION_TYPE_MINION_POOL_SET_UP_SHARED_RESOURCES,
    EXECUTION_TYPE_MINION_POOL_TEAR_DOWN_SHARED_RESOURCES,
    EXECUTION_TYPE_MINION_POOL_ALLOCATE_MINIONS,
    EXECUTION_TYPE_MINION_POOL_DEALLOCATE_MINIONS]

TASK_LOCK_NAME_FORMAT = "task-%s"
TASKFLOW_LOCK_NAME_FORMAT = "taskflow-%s"
EXECUTION_LOCK_NAME_FORMAT = "execution-%s"
ENDPOINT_LOCK_NAME_FORMAT = "endpoint-%s"
MIGRATION_LOCK_NAME_FORMAT = "migration-%s"
REPLICA_LOCK_NAME_FORMAT = "replica-%s"
SCHEDULE_LOCK_NAME_FORMAT = "schedule-%s"
REGION_LOCK_NAME_FORMAT = "region-%s"
SERVICE_LOCK_NAME_FORMAT = "service-%s"
MINION_POOL_LOCK_NAME_FORMAT = "minion-pool-%s"
MINION_MACHINE_LOCK_NAME_FORMAT = "minion-pool-%s-machine-%s"

EXECUTION_TYPE_TO_ACTION_LOCK_NAME_FORMAT_MAP = {
    EXECUTION_TYPE_MIGRATION: MIGRATION_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_REPLICA_EXECUTION: REPLICA_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_REPLICA_DEPLOY: REPLICA_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_REPLICA_UPDATE: REPLICA_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_REPLICA_DISKS_DELETE: REPLICA_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_MINION_POOL_MAINTENANCE: MINION_POOL_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_MINION_POOL_UPDATE: MINION_POOL_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_MINION_POOL_SET_UP_SHARED_RESOURCES: (
        MINION_POOL_LOCK_NAME_FORMAT),
    EXECUTION_TYPE_MINION_POOL_TEAR_DOWN_SHARED_RESOURCES: (
        MINION_POOL_LOCK_NAME_FORMAT),
    EXECUTION_TYPE_MINION_POOL_ALLOCATE_MINIONS: MINION_POOL_LOCK_NAME_FORMAT,
    EXECUTION_TYPE_MINION_POOL_DEALLOCATE_MINIONS: MINION_POOL_LOCK_NAME_FORMAT
}

SERVICE_STATUS_UP = "UP"
SERVICE_STATUS_DOWN = "DOWN"
SERVICE_STATUS_UNKNOWN = "UNKNOWN"

SERVICE_MESSAGING_TOPIC_FORMAT = "%(main_topic)s.%(host)s"
CONDUCTOR_MAIN_MESSAGING_TOPIC = "coriolis_conductor"
WORKER_MAIN_MESSAGING_TOPIC = "coriolis_worker"
SCHEDULER_MAIN_MESSAGING_TOPIC = "coriolis_scheduler"
REPLICA_CRON_MAIN_MESSAGING_TOPIC = "coriolis_replica_cron_worker"
MINION_MANAGER_MAIN_MESSAGING_TOPIC = "coriolis_minion_manager"

MINION_POOL_MACHINE_RETENTION_STRATEGY_DELETE = "delete"
MINION_POOL_MACHINE_RETENTION_STRATEGY_POWEROFF = "poweroff"

MINION_POOL_STATUS_UNKNOWN = "UNKNOWN"
MINION_POOL_STATUS_ERROR = "ERROR"
MINION_POOL_STATUS_DEALLOCATED = "DEALLOCATED"
MINION_POOL_STATUS_VALIDATING_INPUTS = "VALIDATING_INPUTS"
MINION_POOL_STATUS_ALLOCATING_SHARED_RESOURCES = "ALLOCATING_SHARED_RESOURCES"
MINION_POOL_STATUS_ALLOCATING_MACHINES = "ALLOCATING_MACHINES"
MINION_POOL_STATUS_DEALLOCATING_MACHINES = "DEALLOCATING_MACHINES"
MINION_POOL_STATUS_DEALLOCATING_SHARED_RESOURCES = (
    "DEALLOCATING_SHARED_RESOURCES")
MINION_POOL_STATUS_ALLOCATED = "ALLOCATED"
MINION_POOL_STATUS_POOL_MAINTENANCE = "IN_MAINTENANCE"

ACTIVE_MINION_POOL_STATUSES = [
    MINION_POOL_STATUS_VALIDATING_INPUTS,
    MINION_POOL_STATUS_ALLOCATING_SHARED_RESOURCES,
    MINION_POOL_STATUS_ALLOCATING_MACHINES,
    MINION_POOL_STATUS_DEALLOCATING_MACHINES,
    MINION_POOL_STATUS_DEALLOCATING_SHARED_RESOURCES]

MINION_MACHINE_IDENTIFIER_FORMAT = "coriolis-pool-%(pool_id)s-minion-%(minion_id)s"
MINION_MACHINE_STATUS_UNKNOWN = "UNKNOWN"
MINION_MACHINE_STATUS_DEPLOYING = "DEPLOYING"
MINION_MACHINE_STATUS_ERROR = "ERROR"
MINION_MACHINE_STATUS_ERROR_DEPLOYING = "ERROR_DEPLOYING"
MINION_MACHINE_STATUS_RECONFIGURING = "RECONFIGURING"
MINION_MACHINE_STATUS_AVAILABLE = "AVAILABLE"
MINION_MACHINE_STATUS_ALLOCATED = "ALLOCATED"
MINION_MACHINE_STATUS_RESERVED = "RESERVED"
