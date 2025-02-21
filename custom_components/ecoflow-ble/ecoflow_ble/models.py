from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeviceInfo:
    name: str
    serial: str
    model: str | None = "Unknown"
    battery: int | None = None
