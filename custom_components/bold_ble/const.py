"""Constants for the Bold Bluetooth integration."""
from homeassistant.const import Platform

DOMAIN = "bold_ble"
MANUFACTURER = "bold"

CONF_DEVICE_INFO = "device_info"

# Time in seconds to wait for device to be ready
DEVICE_STARTUP_TIMEOUT = 30

PLATFORMS = [
    Platform.LOCK,
]
