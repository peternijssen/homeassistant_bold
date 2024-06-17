
from .bold_types import BoldBleDeviceInfo

SESAM_MANUFACTURER_ID = 0x065B

class BoldBleConnection:
    """Handles the connection."""

    def get_device_info(self, device) -> BoldBleDeviceInfo | None:
        """Retrieve device information."""
        data = device.manufacturer_data[SESAM_MANUFACTURER_ID]

        if len(data) != 12:
            return None

        flags = data[11]
        return {
            'protocol_version': data[0],
            'type': data[1],
            'model': data[2],
            'device_id': int.from_bytes(data[3:11], byteorder='little', signed=False),
            'is_installable': (flags & 1) > 0,
            'events_available': (flags & 2) > 0,
            'should_time_sync': (flags & 4) > 0,
            'is_in_dfu_mode': (flags & 8) > 0,
        }
