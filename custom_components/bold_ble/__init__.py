"""The Bold Bluetooth integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS
from homeassistant.core import HomeAssistant

from .const import CONF_DEVICE_INFO, PLATFORMS
from .lib_files.objects import BoldLock

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bold Bluetooth from a config entry."""
    device_info = entry.data[CONF_DEVICE_INFO]
    address = entry.data[CONF_ADDRESS]

    lock = BoldLock(
        device_info['device_id'], address
    )

    entry.lock = lock

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)