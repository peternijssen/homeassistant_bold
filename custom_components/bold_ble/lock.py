"""Support for Bold Bluetooth locks."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import BoldBleEntity

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up locks."""
    async_add_entities([BoldBleLock(entry.lock)])


class BoldBleLock(BoldBleEntity, LockEntity):
    """A bold ble lock."""

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the lock."""
        #await self._device.unlock()

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the lock."""
        #await self._device.lock()
