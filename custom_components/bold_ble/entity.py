"""The bold_ble integration entities."""

from __future__ import annotations

from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, MANUFACTURER
from .lib_files.objects import BoldLock


class BoldBleEntity(Entity):
    """Defines a Bold Ble entity."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, lock: BoldLock) -> None:
        """Initialize the entity."""
        self._device = lock
        self._attr_available = False
        self._attr_unique_id = lock.unique_id
        self._attr_device_info = DeviceInfo(
            name=lock.name,
            manufacturer=MANUFACTURER,
            connections={(dr.CONNECTION_BLUETOOTH, lock.address)},
            identifiers={(DOMAIN, lock.unique_id)},
            serial_number=lock.serial_number,
        )