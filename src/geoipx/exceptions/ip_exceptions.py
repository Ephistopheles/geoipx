from geoipx.exceptions.GeoIPXException import GeoIPXException
from rich.panel import Panel
from rich import print as rich_print

class InvalidIPError(GeoIPXException):
    """Raised when the IP format is invalid or unsupported."""

    def __init__(self, ip: str, reason: str):
        super().__init__(rich_print(Panel(f"{ip} → {reason}", title="[bold red]GeoIPX Error", title_align="left", border_style="red")))