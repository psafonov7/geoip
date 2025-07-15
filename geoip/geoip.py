from enum import Enum
from urllib.request import urlopen
import re
import ipaddress
import json

BASE_URL = "http://ip-api.com/json"
UTF8 = "utf-8"
IP_RE = r"(?:^|\b(?<!\.))(?:1?\d?\d|2[0-4]\d|25[0-5])(?:\.(?:1?\d?\d|2[0-4]\d|25[0-5])){3}(?=$|[^\w.])"
LOCAL_SUBNETS = ["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]
RESERVED_SUBNETS = ["127.0.0.0/8", "169.254.0.0/16", "192.0.2.0/24"]

class IPType(Enum):
    LOCAL_IP = 1
    RESERVED_IP = 2

class InvalidIPError(Exception):
    """
    Invalid IP Exception
    """
    def __init__(self, ip: str):
        message = f"IP {ip} is invalid."
        super().__init__(message)

def get_ip_info(ip: str, fields: (list[str] | None) = None) -> dict[str, str] | IPType:
    if not _is_valid_ip(ip):
        raise InvalidIPError(ip)
    if _is_local_ip(ip):
        return IPType.LOCAL_IP
    if _is_reserved_ip(ip):
        return IPType.RESERVED_IP
    
    url = _compose_url(ip, fields)
    response = urlopen(url)
    data = response.read().decode(UTF8)
    return json.loads(data)

def _compose_url(ip: str, fields: (list[str] | None) = None) -> str:
    url = BASE_URL + f"/{ip}"
    if fields is not None:
        separator = ","
        joined_fields = separator.join(fields)
        url += f"?fields={joined_fields}"
    return url

def _is_valid_ip(ip: str) -> bool:
    is_match = re.match(IP_RE, ip)
    return is_match is not None

def _is_local_ip(ip: str) -> bool:
    for subnet in LOCAL_SUBNETS:
        if _is_ip_in_range(ip, subnet):
            return True
    return False

def _is_reserved_ip(ip: str) -> bool:
    for subnet in RESERVED_SUBNETS:
        if _is_ip_in_range(ip, subnet):
            return True
    return False

def _is_ip_in_range(ip: str, network_range: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip)
        network = ipaddress.ip_network(network_range)
        return ip_obj in network
    except ValueError:
        return False
