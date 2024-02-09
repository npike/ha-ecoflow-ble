"""Parser for Ecoflow BLE advertisements.

"""
from __future__ import annotations

import logging
import struct
import binascii
from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorLibrary
_LOGGER = logging.getLogger(__name__)

class EcoflowBluetoothDeviceData(BluetoothData):
    """Data for Ecoflow BLE sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing Ecoflow BLE service_info data: %s", service_info.name)
        manufacturer_data = service_info.manufacturer_data
        _LOGGER.debug("Parsing Ecoflow BLE manufacturer_data data: %s", manufacturer_data)
        address = service_info.address
        _LOGGER.debug("Ecoflow Address: " + str(address))
        
        
        for mfr_id, mfr_data in manufacturer_data.items():
            _LOGGER.debug("mfr_id: " + str(mfr_id))
            _LOGGER.debug("mfr_data: " + str(mfr_data))
            
            if mfr_id == 46517:
                _LOGGER.debug("")
                _LOGGER.debug("Parsing Ecoflow BLE mfr data: %s", str(mfr_data))
                hex_representation = binascii.hexlify(mfr_data).decode('utf-8')
                _LOGGER.debug(f"hex {hex_representation}")
                serial = hex_representation[2:34]
                serial = binascii.unhexlify(serial).decode('utf-8')
                _LOGGER.debug(f"serial {serial}")

                battery_raw = hex_representation[34:36]
                battery = int(battery_raw, 16)
                _LOGGER.debug(f"battery {battery}")
                
                if serial:

                    # map device serial to product model
                    model = service_info.name
                    if serial.startswith("R60"):
                        model = "River 2"

                    self.set_device_manufacturer("Ecoflow")
                    self.set_device_name(f"{serial}")
                    self.set_device_type(model)
                    
                    self.update_predefined_sensor(SensorLibrary.BATTERY__PERCENTAGE, battery)