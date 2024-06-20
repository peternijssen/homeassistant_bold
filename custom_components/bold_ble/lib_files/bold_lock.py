"""The Bold BLE integration models."""

from __future__ import annotations

from bleak.backends.device import BLEDevice


class BoldLock:
    """The actual Bold lock."""

    def __init__(
        self,
        device: BLEDevice,
        device_id: int | None = None,
    ) -> None:
        """Init of the lock."""
        self._device = device
        self._device_id = device_id
        self._address = device.address

    @property
    def unique_id(self) -> str | None:
        """Get the device id."""
        return f"bold_{self._device_id}"

    @property
    def device_id(self) -> str | None:
        """Get the device id."""
        return self._device_id

    @property
    def name(self) -> str:
        """Get the name of the lock."""
        return str(self._device_id)

    @property
    def address(self) -> str:
        """Get the address of the lock."""
        return self._address

    @property
    def serial_number(self) -> str:
        """Get the serial number of the lock."""
        return self.device_id
    

    def poll_needed(self, seconds_since_last_poll: int) -> bool:
        """Check if we need to poll."""
        return False
