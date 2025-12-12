from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusProviderEnum

@dataclass
class BaseProviderPropertiesModel:
    last_update: Optional[datetime | None] = None
    status: GeoIPXMetadataStatusProviderEnum = GeoIPXMetadataStatusProviderEnum.NEVER_RUN
    last_error: Optional[str | None] = None
    rate_limit_remaining: Optional[int | None] = None
    rate_limit_reset_at: Optional[datetime | None] = None
    records_count: Optional[int | None] = None

@dataclass
class IPLocateASNMetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class IPLocateCountryMetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class IPLocateIPMetadataModel:
    country: IPLocateCountryMetadataModel = field(default_factory=IPLocateCountryMetadataModel)

@dataclass
class IPLocateMetadataModel:
    asn: IPLocateASNMetadataModel = field(default_factory=IPLocateASNMetadataModel)
    ip: IPLocateIPMetadataModel = field(default_factory=IPLocateIPMetadataModel)

    @classmethod
    def from_dict(cls, data: dict):
        asn_data = data.get("asn", {})
        ip_data = data.get("ip", {})
        return cls(
            asn=IPLocateASNMetadataModel(**asn_data),
            ip=IPLocateIPMetadataModel(
                country=IPLocateCountryMetadataModel(**ip_data.get("country", {}))
            )
        )