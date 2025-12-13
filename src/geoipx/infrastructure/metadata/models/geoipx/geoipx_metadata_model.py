import json
from enum import Enum
from datetime import datetime
from typing import Optional, Dict
from dataclasses import dataclass, field, asdict, is_dataclass
from geoipx.infrastructure.metadata.models.providers.dbip.dbip_metadata_model import DBIPMetadataModel
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusGlobalEnum
from geoipx.infrastructure.metadata.models.providers.iplocate.iplocate_metadata_model import IPLocateMetadataModel
from geoipx.infrastructure.metadata.models.providers.ip2location.ip2location_metadata_model import IP2LocationMetadataModel

@dataclass
class GeoIPXMetadataModel:

    schema_version: int = 1
    is_initialized: bool = False
    last_global_update: Optional[datetime | None] = None
    global_status: GeoIPXMetadataStatusGlobalEnum = GeoIPXMetadataStatusGlobalEnum.NEVER_RUN
    providers: Dict[str, object] = field(default_factory=lambda: {
        "dbip": DBIPMetadataModel(),
        "ip2location": IP2LocationMetadataModel(),
        "iplocate": IPLocateMetadataModel()
    })

    def to_json(self):
        return json.dumps(
            asdict(self),
            default=self._serialize_json,
            ensure_ascii=False,
            separators=(",", ":")
        )

    @staticmethod
    def to_model(json_str: str):
        raw = json.loads(json_str)

        if raw.get("last_global_update"):
            raw["last_global_update"] = datetime.fromisoformat(raw["last_global_update"])

        if raw.get("global_status"):
            raw["global_status"] = GeoIPXMetadataStatusGlobalEnum(raw["global_status"])

        provider_map = {
            "dbip": DBIPMetadataModel,
            "ip2location": IP2LocationMetadataModel,
            "iplocate": IPLocateMetadataModel,
        }

        providers_raw = raw.get("providers", {})
        providers = {}

        for key, model_class in provider_map.items():
            if hasattr(model_class, "from_dict"):
                providers[key] = model_class.from_dict(providers_raw.get(key, {}))
            else:
                providers[key] = model_class(**providers_raw.get(key, {}))

        raw["providers"] = providers

        return GeoIPXMetadataModel(**raw)

    def _serialize_json(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, datetime):
            return obj.isoformat()
        if is_dataclass(obj):
            return asdict(obj)
        return str(obj)
