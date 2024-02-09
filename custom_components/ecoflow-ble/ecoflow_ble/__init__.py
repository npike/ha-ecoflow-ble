"""Parser for Ecoflow BLE advertisements.

"""
from __future__ import annotations

from sensor_state_data import (
    DeviceClass,
    DeviceKey,
    SensorDescription,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from .parser import EcoflowBluetoothDeviceData

__version__ = "0.0.1"

__all__ = [
    "EcoflowBluetoothDeviceData",
    "SensorDescription",
    "SensorDeviceInfo",
    "DeviceClass",
    "DeviceKey",
    "SensorUpdate",
    "SensorDeviceInfo",
    "SensorValue",
    "Units",
]