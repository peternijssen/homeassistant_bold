"""Support for Bold Bluetooth locks."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import BoldDataUpdateCoordinator
from .entity import BoldBleEntity
from .lib_files.bold_lock import BoldLock

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bold BLE lock platform."""
    coordinator: BoldDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([BoldBleLock(coordinator)])


class BoldBleLock(BoldBleEntity, LockEntity, CoordinatorEntity):
    """Bold BLE lock entity."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, coordinator: BoldDataUpdateCoordinator) -> None:
        """Initialize the lock entity."""
        super().__init__(coordinator)
        self._device: BoldLock = coordinator.device
        self._async_update_attrs()

    def _async_update_attrs(self) -> None:
        """Update the entity attributes."""
        #status = self._device.get_lock_status()
        #self._attr_is_locked = None << status
        #self._attr_is_locking = None << status
        #self._attr_is_unlocking = None << status

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the lock."""
        await self._device.unlock()
        self._async_update_attrs()
        self.async_write_ha_state()

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the lock."""
        await self._device.lock()
        self._async_update_attrs()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_update_listener)
        )

    async def async_update_listener(self) -> None:
        """Update the entity."""
        self._async_update_attrs()
        self.async_write_ha_state()
