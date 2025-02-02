"""Config flow for Bold BLE integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_entry_oauth2_flow

from .const import CONF_DEVICE_INFO, DOMAIN
from .lib_files.ble import BoldBleConnection

_LOGGER = logging.getLogger(__name__)


class OAuth2FlowHandler(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    """Config flow to handle Bold BLE OAuth2 authentication."""

    VERSION = 1
    DOMAIN = DOMAIN

    reauth_entry: config_entries.ConfigEntry | None = None

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_step_reauth(self, user_input=None):
        """Perform reauth upon an API authentication error."""
        self.reauth_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Dialog that informs the user that reauth is required."""
        if user_input is None:
            return self.async_show_form(
                step_id="reauth_confirm"
            )
        return await self.async_step_user()

    async def async_oauth_create_entry(self, data: dict[str, Any]) -> FlowResult:
        """Create an entry for Bold BLE."""
        _LOGGER.debug("Creating entry with data: %s", data)

        # Get discovered BLE devices
        discovery_info = await self.hass.async_add_executor_job(
            bluetooth.async_discovered_service_info, self.hass
        )
        _LOGGER.error("Found BLE devices: %s", discovery_info)

        # Filter for Bold devices
        # TODO: Can we use the data from the manifest.json file?
        bold_devices = [
            device
            for device in discovery_info
            if device.manufacturer_id == 1627
            and device.service_uuids
            and "0000fd30-0000-1000-8000-00805f9b34fb" in device.service_uuids
        ]
        _LOGGER.debug("Found Bold BLE devices: %s", bold_devices)

        if not bold_devices:
            return self.async_abort(reason="no_devices_found")

        # if len(bold_devices) == 1:
        #     device = bold_devices[0]
        #
        #     # Retrieve device info
        #     connection = BoldBleConnection()
        #     device_info = connection.get_device_info(device)
        #
        #     return self.async_create_entry(
        #         title=device.name or device.address,
        #         data={
        #             **data,
        #             CONF_NAME: device.name,
        #             CONF_ADDRESS: device.address,
        #             CONF_DEVICE_INFO: device_info,
        #         },
        #     )

        # Show selection form
        return self.async_show_form(
            step_id="select_device",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_ADDRESS): vol.In(
                        {
                            device.address: f"{device.name} ({device.address})"
                            for device in bold_devices
                        }
                    ),
                }
            ),
        )

    async def async_step_select_device(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle device selection."""
        if user_input is None:
            return self.async_abort(reason="no_devices_found")

        address = user_input[CONF_ADDRESS]
        device = next(
            device
            for device in bluetooth.async_discovered_service_info(self.hass)
            if device.address == address
        )

        # Retrieve device info
        connection = BoldBleConnection()
        device_info = connection.get_device_info(device)

        if device_info['is_installable'] is True:
            return self.async_abort(reason="device_is_installable")

        if device_info['is_in_dfu_mode'] is True:
            return self.async_abort(reason="device_is_in_dfu_mode")

        await self.async_set_unique_id(
            device.address, raise_on_progress=False
        )
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=device_info['device_id'],
            data={
                CONF_DEVICE_INFO: device_info,
                CONF_ADDRESS: address,
            },
        )