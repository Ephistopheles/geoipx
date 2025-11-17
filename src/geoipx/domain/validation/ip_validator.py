from ipaddress import ip_address
from geoipx.exceptions.ip_exceptions import InvalidIPError

def validate_ip(ip: str) -> str:
    """Validate if an IP is valid and public. Returns the normalized IP."""
    try:
        parsed_ip = ip_address(ip)
    except ValueError:
        raise InvalidIPError(ip, "Invalid IP format")

    if parsed_ip.is_private:
        raise InvalidIPError(ip, "Private IPs are not allowed")

    if parsed_ip.is_loopback:
        raise InvalidIPError(ip, "Loopback IPs are not allowed")

    if parsed_ip.is_reserved:
        raise InvalidIPError(ip, "Reserved IPs cannot be used")

    return str(parsed_ip)
