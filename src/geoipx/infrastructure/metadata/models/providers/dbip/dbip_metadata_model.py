from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusProviderEnum

@dataclass
class BaseProviderPropertiesModel:
    status: GeoIPXMetadataStatusProviderEnum = GeoIPXMetadataStatusProviderEnum.NEVER_RUN
    last_update: Optional[datetime | None] = None
    last_error: Optional[str | None] = None
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

        return cls(**data)

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
            asn=DBIPASNMetadataModel.from_dict(asn_data),
            ip=DBIPIPMetadataModel(
                city=DBIPCityMetadataModel.from_dict(ip_data.get("city", {})),
                country=DBIPCountryMetadataModel.from_dict(ip_data.get("country", {}))
            )
        )