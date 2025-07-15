from geoip import get_ip_info, IPType, InvalidIPError
import pytest

def test_get_ip_info():

    with pytest.raises(InvalidIPError):
        get_ip_info("256.256.256.256")

    assert get_ip_info("192.168.0.0") == IPType.LOCAL_IP
    assert get_ip_info("192.168.127.127") == IPType.LOCAL_IP
    assert get_ip_info("192.168.255.255") == IPType.LOCAL_IP

    assert get_ip_info("127.0.0.0") == IPType.RESERVED_IP
    assert get_ip_info("127.127.127.127") == IPType.RESERVED_IP
    assert get_ip_info("127.255.255.255") == IPType.RESERVED_IP

    info = get_ip_info("8.8.8.8")
    assert isinstance(info, dict)
    assert info["countryCode"] == "US"
