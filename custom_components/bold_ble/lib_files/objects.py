"""The Bold BLE integration models."""

from __future__ import annotations


class BoldLock:
    """The actual Bold lock."""

    def __init__(
        self,
        device_id: int | None = None,
        address: str | None = None,
    ) -> None:
        """Init of the lock."""
        self._device_id = device_id
        self._address = address

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
        return self._device_id

    @property
    def address(self) -> str:
        """Get the address of the lock."""
        return self._address

    @property
    def serial_number(self) -> str:
        """Get the serial number of the lock."""
        return self.device_id
