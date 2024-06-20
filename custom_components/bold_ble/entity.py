"""The bold_ble integration entities."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from homeassistant.components.bluetooth.passive_update_coordinator import PassiveBluetoothCoordinatorEntity
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo

from .const import MANUFACTURER
from .coordinator import BoldDataUpdateCoordinator


class BoldBleEntity(PassiveBluetoothCoordinatorEntity[BoldDataUpdateCoordinator]):
    """Defines a Bold Ble entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: BoldDataUpdateCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._device = coordinator.device
        self._last_run_success: bool | None = None
        self._address = coordinator.address
        self._attr_unique_id = coordinator.base_unique_id
        self._attr_device_info = DeviceInfo(
            name=coordinator.device_name,
            manufacturer=MANUFACTURER,
            connections={(dr.CONNECTION_BLUETOOTH, self._address)},
            serial_number=coordinator.serial_number,
        )

    @property
    def parsed_data(self) -> dict[str, Any]:
        """Return parsed device data for this entity."""
        print("entity.py: parsed_data")
        return self.coordinator.device.parsed_data

    @property
    def extra_state_attributes(self) -> Mapping[Any, Any]:
        """Return the state attributes."""
        return {"last_run_success": self._last_run_success}

    @callback
    def _async_update_attrs(self) -> None:
        """Update the entity attributes."""

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle data update."""
        self._async_update_attrs()
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""
        #self.async_on_remove(self._device.subscribe(self._handle_coordinator_update))
        return await super().async_added_to_hass()

    async def async_update(self) -> None:
        """Update the entity.

        Only used by the generic entity update service.
        """
        await self._device.update()