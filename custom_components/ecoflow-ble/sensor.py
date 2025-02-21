"""The ecoflow sensor platform."""

from __future__ import annotations
from typing import Any

from .ecoflow_ble import EcoflowController

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothCoordinatorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfPressure, UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN
from .coordinator import EcoflowDataUpdateCoordinator
from .models import EcoflowData


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up platform for ecoflow."""
    data: EcoflowData = hass.data[DOMAIN][entry.entry_id]
    entities = []
    entities.append(BatterySensor(data.coordinator, data.device, entry.title))

    async_add_entities(entities)


class EcoflowSensor(
    PassiveBluetoothCoordinatorEntity[EcoflowDataUpdateCoordinator], SensorEntity
):
    """Representation of Ecoflow sensor."""

    def __init__(
        self,
        coordinator: EcoflowDataUpdateCoordinator,
        device: EcoflowController,
        name: str,
    ) -> None:
        """Initialize an Ecoflow sensor."""
        super().__init__(coordinator)
        self._device = device
        self._name = name

        self._attr_device_info = DeviceInfo(
            name=device.name,
            model=device.model,
            serial_number=device.serial,
            manufacturer="Ecoflow",
            connections={(dr.CONNECTION_BLUETOOTH, device.address)},
        )
        self._async_update_attrs()

    @callback
    def _async_update_attrs(self) -> None:
        """Handle updating _attr values."""
        raise NotImplementedError("Not yet implemented.")

    @callback
    def _handle_coordinator_update(self, *args: Any) -> None:
        """Handle data update."""
        self._async_update_attrs()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        self.async_on_remove(
            self._device.register_callback(self._handle_coordinator_update)
        )
        return await super().async_added_to_hass()


class BatterySensor(EcoflowSensor):
    _attr_name = "Battery"
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def name(self) -> str:
        return f"{self._name} Battery"

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return f"{self._device.address}_battery"

    @callback
    def _async_update_attrs(self) -> None:
        """Handle updating _attr values."""
        self._attr_native_value = self._device.battery
