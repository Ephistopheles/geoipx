from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusProviderEnum

@dataclass
class BaseProviderPropertiesModel:
    last_update: Optional[datetime | None] = None
    status: GeoIPXMetadataStatusProviderEnum = GeoIPXMetadataStatusProviderEnum.NEVER_RUN
    last_error: Optional[str | None] = None
    rate_limit_remaining: Optional[int | None] = 5
    rate_limit_reset_at: Optional[datetime | None] = None
    records_count: Optional[int | None] = None

    @classmethod
    def from_dict(cls, data: dict):
        if data.get("status"):
            try:
                data["status"] = GeoIPXMetadataStatusProviderEnum(data["status"])
            except ValueError:
                pass

        if data.get("last_update") and isinstance(data["last_update"], str):
            try:
                data["last_update"] = datetime.fromisoformat(data["last_update"])
            except ValueError:
                pass

        if data.get("rate_limit_reset_at") and isinstance(data["rate_limit_reset_at"], str):
            try:
                data["rate_limit_reset_at"] = datetime.fromisoformat(data["rate_limit_reset_at"])
            except ValueError:
                pass

        return cls(**data)

@dataclass
class IP2LocationIPv4MetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class IP2LocationIPv6MetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class IP2LocationIPMetadataModel:
    v4: IP2LocationIPv4MetadataModel = field(default_factory=IP2LocationIPv4MetadataModel)
    v6: IP2LocationIPv6MetadataModel = field(default_factory=IP2LocationIPv6MetadataModel)

@dataclass
class IP2LocationMetadataModel:
    ip: IP2LocationIPMetadataModel = field(default_factory=IP2LocationIPMetadataModel)

    def iter_tasks(self):
        yield self.ip.v4
        yield self.ip.v6

    @classmethod
    def from_dict(cls, data: dict):
        ip_data = data.get("ip", {})
        return cls(
            ip=IP2LocationIPMetadataModel(
                v4=IP2LocationIPv4MetadataModel.from_dict(ip_data.get("v4", {})),
                v6=IP2LocationIPv6MetadataModel.from_dict(ip_data.get("v6", {}))
            )
        )