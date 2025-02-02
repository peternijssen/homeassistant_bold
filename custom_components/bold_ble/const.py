"""Constants for the Bold BLE integration."""
from homeassistant.const import Platform

DOMAIN = "bold_ble"
MANUFACTURER = "bold"

CONF_DEVICE_INFO = "device_info"

# OAuth2 settings
BOLD_AUTHORIZE_URL = "https://auth.boldsmartlock.com"
BOLD_TOKEN_URL = "https://api.boldsmartlock.com/v2/oauth/token"
BOLD_REDIRECT_URI = "boldsmartlock://auth"

# Time in seconds to wait for device to be ready
DEVICE_STARTUP_TIMEOUT = 30

PLATFORMS = [
    Platform.LOCK,
]
