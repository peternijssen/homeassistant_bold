"""Constants for the Bold Bluetooth integration."""
from homeassistant.const import Platform

DOMAIN = "bold_ble"
MANUFACTURER = "Bold"

CONF_DEVICE_INFO = "device_info"

PLATFORMS = [
    Platform.LOCK,
]
