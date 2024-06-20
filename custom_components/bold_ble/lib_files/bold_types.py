
from typing import Literal, TypedDict
from dataclasses import dataclass
from typing import Any

from bleak.backends.device import BLEDevice


@dataclass
class BoldBleDeviceInfo(TypedDict):
    """Bold device info."""

    protocol_version: int
    type: int
    model: int
    device_id: int
    is_installable: bool
    events_available: bool
    should_time_sync: bool
    is_in_dfu_mode: bool

@dataclass
class BoldAdvertisement:
    """Bold advertisement."""

    address: str
    data: dict[str, Any]
    device: BLEDevice
    rssi: int
    active: bool = False

BoldBlePacketTypes = {
    "ResultSuccess": 0x00,
    "StartHandshake": 0xa0,
    "HandshakeResponse": 0xa1,
    "HandshakeClientResponse": 0xa2,
    "HandshakeFinishedResponse": 0xa3,
    "Command": 0xa4,
    "CommandAck": 0xa5,
    "LocalCommand": 0xa6,
    "LocalCommandResponse": 0xa7,
    "DeliverMessages": 0xb0,
    "DialogServer": 0xc0,
    "DialogDevice": 0xc1,
    "Event": 0xd0,
    "EventAck": 0xd1,
    "EventAckResponse": 0xd2,
    "ClientBlocked": 0xfd,
    "HandshakeExpired": 0xfe,
    "EncryptionError": 0xff,
}

BoldBlePacketType = Literal[
    0x00, 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5,
    0xa6, 0xa7, 0xb0, 0xc0, 0xc1, 0xd0, 0xd1,
    0xd2, 0xfd, 0xfe, 0xff
]
