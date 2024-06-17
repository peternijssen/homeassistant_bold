from typing import TypedDict


class BoldBleDeviceInfo(TypedDict):
    protocol_version: int
    type: int
    model: int
    device_id: int
    is_installable: bool
    events_available: bool
    should_time_sync: bool
    is_in_dfu_mode: bool
