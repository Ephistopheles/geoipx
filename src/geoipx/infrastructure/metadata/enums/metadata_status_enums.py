from enum import Enum

class GeoIPXMetadataStatusGlobalEnum(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NEVER_RUN = "NEVER_RUN"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

class GeoIPXMetadataStatusProviderEnum(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NEVER_RUN = "NEVER_RUN"
    RATE_LIMITED = "RATE_LIMITED"
