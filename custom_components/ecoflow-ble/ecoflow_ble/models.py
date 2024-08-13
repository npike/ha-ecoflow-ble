from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeviceInfo:
    name: str
    serial: str
    battery: int | None = None