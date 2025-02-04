"""The Bold Bluetooth integration."""
from __future__ import annotations

import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_DEVICE_INFO, DOMAIN, PLATFORMS
from .coordinator import BoldDataUpdateCoordinator
from .lib_files.bold_lock import BoldLock

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Bold BLE component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bold Bluetooth from a config entry."""
    assert entry.unique_id is not None
    hass.data.setdefault(DOMAIN, {})

    device_info = entry.data[CONF_DEVICE_INFO]
    address = entry.data[CONF_ADDRESS]

    ble_device = bluetooth.async_ble_device_from_address(
        hass, address.upper(), True
    )
    if not ble_device:
        raise ConfigEntryNotReady(
            f"Could not find Bold with address {address}"
        )

    lock = BoldLock(
        ble_device, device_info['device_id']
    )

    coordinator = hass.data[DOMAIN][entry.entry_id] = BoldDataUpdateCoordinator(
        hass,
        _LOGGER,
        ble_device,
        lock,
        entry.unique_id,
        str(entry.data.get(CONF_NAME, entry.title)),
        device_info['device_id']
    )

    entry.async_on_unload(coordinator.async_start())
    if not await coordinator.async_wait_ready():
        raise ConfigEntryNotReady(f"{address} is not advertising state")

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
