from dataclasses import dataclass

@dataclass
class ProviderFetchResult:

    success: bool
    error_message: str | None
    records_count: int | None
