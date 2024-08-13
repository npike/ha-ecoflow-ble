"""Constants"""

from bleak.exc import BleakError
# Component constants

DOMAIN = "ecoflow_ble"
PLATFORM = "sensor"

BLEAK_EXCEPTIONS = (AttributeError, BleakError, TimeoutError)
