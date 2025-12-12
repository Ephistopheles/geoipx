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
class DBIPASNMetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class DBIPCityMetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class DBIPCountryMetadataModel(BaseProviderPropertiesModel):
    pass

@dataclass
class DBIPIPMetadataModel:
    city: DBIPCityMetadataModel = field(default_factory=DBIPCityMetadataModel)
    country: DBIPCountryMetadataModel = field(default_factory=DBIPCountryMetadataModel)

@dataclass
class DBIPMetadataModel:
    asn: DBIPASNMetadataModel = field(default_factory=DBIPASNMetadataModel)
    ip: DBIPIPMetadataModel = field(default_factory=DBIPIPMetadataModel)

    @classmethod
    def from_dict(cls, data: dict):
        asn_data = data.get("asn", {})
        ip_data = data.get("ip", {})

        return cls(
            asn=DBIPASNMetadataModel(**asn_data),
            ip=DBIPIPMetadataModel(
                city=DBIPCityMetadataModel(**ip_data.get("city", {})),
                country=DBIPCountryMetadataModel(**ip_data.get("country", {}))
            )
        )