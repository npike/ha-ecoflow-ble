"""The led ble integration models."""
from __future__ import annotations

from dataclasses import dataclass

from .ecoflow_ble import EcoflowController

from .coordinator import EcoflowDataUpdateCoordinator


@dataclass
class EcoflowData:
    """Data for the Ecoflow integration."""

    title: str
    device: EcoflowController
    coordinator: EcoflowDataUpdateCoordinator
