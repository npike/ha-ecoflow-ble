from .models import DeviceInfo
import logging
import binascii

_LOGGER = logging.getLogger(__name__)


def parse_manufacturer_data(data: bytes) -> DeviceInfo:
    hex_representation = binascii.hexlify(data).decode("utf-8")
    serial = hex_representation[2:34]
    serial = binascii.unhexlify(serial).decode("utf-8")
    # _LOGGER.debug(f"serial {serial}")

    battery_raw = hex_representation[34:36]
    battery = int(battery_raw, 16)

    model = "Unknown"
    if serial:
        # map device serial to product model
        if serial.startswith("R60"):
            model = "River 2"
        elif serial.startswith("R65"):
            model = "River 3"
        elif serial.startswith("R33"):
            model = "Delta 2"

    return DeviceInfo(name=serial, serial=serial, model=model, battery=battery)
