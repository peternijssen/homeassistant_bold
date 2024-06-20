"""Support for Bold Bluetooth locks."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import BoldDataUpdateCoordinator
from .entity import BoldBleEntity
from .lib_files.bold_lock import BoldLock

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up locks."""
    coordinator: BoldDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BoldBleLock(coordinator)])


class BoldBleLock(BoldBleEntity, LockEntity):
    """A bold ble lock."""

    _attr_translation_key = "lock"
    _attr_name = None
    _device: BoldLock

    def __init__(self, coordinator: BoldDataUpdateCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._async_update_attrs()

    def _async_update_attrs(self) -> None:
        """Update the entity attributes."""
        #status = self._device.get_lock_status()
        #self._attr_is_locked = None << status
        #self._attr_is_locking = None << status
        #self._attr_is_unlocking = None << status

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the lock."""
        self._last_run_success = await self._device.unlock()
        self.async_write_ha_state()

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the lock."""
        self._last_run_success = await self._device.lock()
        self.async_write_ha_state()
