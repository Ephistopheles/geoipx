from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from geoipx.infrastructure.metadata.enums.geoipx_metadata_status_enums import GeoIPXMetadataStatusProviderEnum

@dataclass
class DBIPMetadataModel:

    last_update: Optional[datetime | None] = None
    status: GeoIPXMetadataStatusProviderEnum = GeoIPXMetadataStatusProviderEnum.NEVER_RUN
    last_error: Optional[str | None] = None
    rate_limit_remaining: Optional[int | None] = None
    rate_limit_reset_at: Optional[datetime | None] = None
    records_count: Optional[int | None] = None