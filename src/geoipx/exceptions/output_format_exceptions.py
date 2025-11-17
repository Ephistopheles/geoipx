from geoipx.exceptions.GeoIPXException import GeoIPXException
from rich.panel import Panel
from rich import print as rich_print

class OutputFormatError(GeoIPXException):
    """Raised when the requested output format is invalid or unsupported."""

    @classmethod
    def from_format(cls, format: str, reason: str):
        return cls(rich_print(Panel(f"{format} → {reason}", title="[bold red]GeoIPX Error", title_align="left", border_style="red")))

    @classmethod
    def from_invalid_directory(cls, message: str):
        return cls(rich_print(Panel(message, title="[bold red]GeoIPX Error", title_align="left", border_style="red")))
