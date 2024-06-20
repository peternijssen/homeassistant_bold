"""Config flow for Bold Bluetooth integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_ADDRESS

from .const import CONF_DEVICE_INFO, DOMAIN
from .lib_files.ble import BoldBleConnection

_LOGGER = logging.getLogger(__name__)


class BoldConfigFlow(ConfigFlow, domain=DOMAIN):
    """Bold config flow."""

    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        self._discovery_info = discovery_info

        return await self.async_step_user()


    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self.context["active"] = True
            address = user_input[CONF_ADDRESS]
            discovery_info = self._discovered_devices[address]
            connection = BoldBleConnection()
            device_info = connection.get_device_info(discovery_info)

            if device_info['is_installable'] is True:
                return self.async_abort(reason="device_is_installable")

            if device_info['is_in_dfu_mode'] is True:
                return self.async_abort(reason="device_is_in_dfu_mode")

            await self.async_set_unique_id(
                discovery_info.address, raise_on_progress=False
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=device_info['device_id'],
                data={
                    CONF_DEVICE_INFO: device_info,
                    CONF_ADDRESS: address,
                },
            )

        if discovery := self._discovery_info:
            self._discovered_devices[discovery.address] = discovery
        else:
            current_addresses = self._async_current_ids()
            for discovery in async_discovered_service_info(self.hass):
                if (
                    discovery.address in current_addresses
                    or discovery.address in self._discovered_devices
                ):
                    continue
                self._discovered_devices[discovery.address] = discovery

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_ADDRESS): vol.In(
                    {
                        service_info.address: (
                            f"{service_info.name} ({service_info.address})"
                        )
                        for service_info in self._discovered_devices.values()
                    }
                )
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )