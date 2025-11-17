class GeoIPXException(Exception):
    """Base exception for all GeoIPX related errors."""

    prefix = "[GeoIPX Error]"
    
    def __str__(self):
        return f"{self.prefix} {self.message}"
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)