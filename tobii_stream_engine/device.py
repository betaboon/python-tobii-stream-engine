import enum
import logging
from dataclasses import dataclass
from typing import Protocol

from _tobii_stream_engine_cffi import ffi as _ffi  # type: ignore
from _tobii_stream_engine_cffi import lib as _lib

from tobii_stream_engine.api import Api
from tobii_stream_engine.capabilities import Capability
from tobii_stream_engine.errors import raise_on_error
from tobii_stream_engine.streams import Stream

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeviceInfo:
    serial_number: str
    model: str
    generation: str
    firmware_version: str


@dataclass(frozen=True)
class PositionXY:
    x: float
    y: float


@dataclass(frozen=True)
class PositionXYZ:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class GazePoint:
    validity: bool
    position_xy: PositionXY


@dataclass(frozen=True)
class GazeOrigin:
    left_validity: bool
    left_xyz: PositionXYZ
    right_validity: bool
    right_xyz: PositionXYZ


@dataclass(frozen=True)
class EyePosition:
    left_validity: bool
    left_xyz: PositionXYZ
    right_validity: bool
    right_xyz: PositionXYZ


class UserPresence(enum.Enum):
    UNKNOWN = enum.auto()
    AWAY = enum.auto()
    PRESENT = enum.auto()


class GazePointCallback(Protocol):
    def __call__(self, *, timestamp: int, gaze_point: GazePoint) -> None:
        ...


class GazeOriginCallback(Protocol):
    def __call__(self, *, timestamp: int, gaze_origin: GazeOrigin) -> None:
        ...


class EyePositionCallback(Protocol):
    def __call__(self, *, timestamp: int, eye_position: EyePosition) -> None:
        ...


class UserPresenceCallback(Protocol):
    def __call__(self, *, timestamp: int, user_presence: UserPresence) -> None:
        ...


@_ffi.def_extern()  # type: ignore
def gaze_point_callback(gaze_point, user_data) -> None:
    _timestamp_us = int(gaze_point.timestamp_us)
    _validity = gaze_point.validity == _lib.TOBII_VALIDITY_VALID
    _position_xy = PositionXY(
        x=float(gaze_point.position_xy[0]),
        y=float(gaze_point.position_xy[1]),
    )
    _gaze_point = GazePoint(
        validity=_validity,
        position_xy=_position_xy,
    )

    device: Device = _ffi.from_handle(user_data)
    device._on_gaze_point(
        timestamp=_timestamp_us,
        gaze_point=_gaze_point,
    )


@_ffi.def_extern()  # type: ignore
def gaze_origin_callback(gaze_origin, user_data) -> None:
    _timestamp_us = int(gaze_origin.timestamp_us)
    _left_validity = gaze_origin.left_validity == _lib.TOBII_VALIDITY_VALID
    _left_xyz = PositionXYZ(
        x=float(gaze_origin.left_xyz[0]),
        y=float(gaze_origin.left_xyz[1]),
        z=float(gaze_origin.left_xyz[2]),
    )
    _right_validity = gaze_origin.right_validity == _lib.TOBII_VALIDITY_VALID
    _right_xyz = PositionXYZ(
        x=float(gaze_origin.right_xyz[0]),
        y=float(gaze_origin.right_xyz[1]),
        z=float(gaze_origin.right_xyz[2]),
    )
    _gaze_origin = GazeOrigin(
        left_validity=_left_validity,
        left_xyz=_left_xyz,
        right_validity=_right_validity,
        right_xyz=_right_xyz,
    )

    device: Device = _ffi.from_handle(user_data)
    device._on_gaze_origin(
        timestamp=_timestamp_us,
        gaze_origin=_gaze_origin,
    )


@_ffi.def_extern()  # type: ignore
def eye_position_normalized_callback(eye_position, user_data) -> None:
    _timestamp_us = int(eye_position.timestamp_us)
    _left_validity = eye_position.left_validity == _lib.TOBII_VALIDITY_VALID
    _left_xyz = PositionXYZ(
        x=float(eye_position.left_xyz[0]),
        y=float(eye_position.left_xyz[1]),
        z=float(eye_position.left_xyz[2]),
    )
    _right_validity = eye_position.right_validity == _lib.TOBII_VALIDITY_VALID
    _right_xyz = PositionXYZ(
        x=float(eye_position.right_xyz[0]),
        y=float(eye_position.right_xyz[1]),
        z=float(eye_position.right_xyz[2]),
    )
    _eye_position = EyePosition(
        left_validity=_left_validity,
        left_xyz=_left_xyz,
        right_validity=_right_validity,
        right_xyz=_right_xyz,
    )

    device: Device = _ffi.from_handle(user_data)
    device._on_eye_position(
        timestamp=_timestamp_us,
        eye_position=_eye_position,
    )


@_ffi.def_extern()  # type: ignore
def user_presence_callback(status, timestamp_us, user_data) -> None:
    _timestamp_us = int(timestamp_us)
    _user_presence = UserPresence.UNKNOWN
    if status == _lib.TOBII_USER_PRESENCE_STATUS_AWAY:
        _user_presence = UserPresence.AWAY
    elif status == _lib.TOBII_USER_PRESENCE_STATUS_PRESENT:
        _user_presence = UserPresence.PRESENT

    device: Device = _ffi.from_handle(user_data)
    device._on_user_presence(
        timestamp=_timestamp_us,
        user_presence=_user_presence,
    )


class Device:
    def __init__(self, api: Api, url: str) -> None:
        self._api = api
        self._url = url
        self._gaze_point_callback: GazePointCallback | None = None
        self._gaze_origin_callback: GazeOriginCallback | None = None
        self._eye_position_callback: EyePositionCallback | None = None
        self._user_presence_callback: UserPresenceCallback | None = None

        self._handle = _ffi.new_handle(self)
        self._device_ptr: _ffi.CDATA
        self._device_ptr_ptr: _ffi.CDATA

        self._create()

    def __del__(self) -> None:
        self.unsubscribe_gaze_point()
        self.unsubscribe_eye_position()
        self.unsubscribe_user_presence()
        self._destroy()

    def _create(self) -> None:
        logger.debug(f"{self._url}: creating device")

        device_ptr = _ffi.new("tobii_device_t **")

        ret = _lib.tobii_device_create(
            self._api._api_ptr,
            self._url.encode(),
            _lib.TOBII_FIELD_OF_USE_INTERACTIVE,
            device_ptr,
        )

        raise_on_error(ret)

        self._device_ptr = device_ptr[0]
        self._device_ptr_ptr = device_ptr

    def _destroy(self) -> None:
        logger.debug(f"{self._url}: destroying device")

        ret = _lib.tobii_device_destroy(
            self._device_ptr,
        )

        raise_on_error(ret)

        self._device_ptr = None

    def get_device_info(self) -> DeviceInfo:
        logger.debug(f"{self._url}: getting device info")

        device_info = _ffi.new("tobii_device_info_t *")

        ret = _lib.tobii_get_device_info(
            self._device_ptr,
            device_info,
        )

        raise_on_error(ret)

        serial_number = _ffi.string(device_info.serial_number).decode()
        model = _ffi.string(device_info.model).decode()
        generation = _ffi.string(device_info.generation).decode()
        firmware_version = _ffi.string(device_info.firmware_version).decode()

        return DeviceInfo(
            serial_number=serial_number,
            model=model,
            generation=generation,
            firmware_version=firmware_version,
        )

    def is_supported_capability(self, capability: Capability) -> bool:
        logger.debug(f"{self._url}: checking supported capability '{capability.name}'")

        supported = _ffi.new("tobii_supported_t *")

        ret = _lib.tobii_capability_supported(
            self._device_ptr,
            capability,
            supported,
        )

        raise_on_error(ret)

        is_supported: bool = supported[0] == _lib.TOBII_SUPPORTED

        return is_supported

    def get_supported_capabilities(self) -> list[Capability]:
        logger.debug(f"{self._url}: getting supported capabilities")

        supported_capabilities = []

        for capability in Capability:
            if self.is_supported_capability(capability):
                supported_capabilities.append(capability)

        return supported_capabilities

    def is_supported_stream(self, stream: Stream) -> bool:
        logger.debug(f"{self._url}: checking supported stream '{stream.name}'")

        supported = _ffi.new("tobii_supported_t *")

        ret = _lib.tobii_stream_supported(
            self._device_ptr,
            stream,
            supported,
        )

        raise_on_error(ret)

        is_supported: bool = supported[0] == _lib.TOBII_SUPPORTED

        return is_supported

    def get_supported_streams(self) -> list[Stream]:
        logger.debug(f"{self._url}: getting supported streams")

        supported_streams = []

        for stream in Stream:
            if self.is_supported_stream(stream):
                supported_streams.append(stream)

        return supported_streams

    def get_output_frequency(self) -> float:
        logger.debug(f"{self._url}: getting output frequency")

        output_frequency = _ffi.new("float *")

        ret = _lib.tobii_get_output_frequency(
            self._device_ptr,
            output_frequency,
        )

        raise_on_error(ret)

        return float(output_frequency[0])

    def set_output_frequency(self, output_frequency: float) -> None:
        logger.debug(f"{self._url}: setting output frequency")

        ret = _lib.tobii_set_output_frequency(
            self._device_ptr,
            output_frequency,
        )

        raise_on_error(ret)

    def enumerate_output_frequencies(self) -> list[float]:
        logger.debug(f"{self._url}: getting output frequencies")

        output_frequencies = []

        @_ffi.callback("tobii_output_frequency_receiver_t")  # type: ignore
        def output_frequency_receiver(output_frequency, user_data) -> None:
            output_frequencies.append(float(output_frequency))

        ret = _lib.tobii_enumerate_output_frequencies(
            self._device_ptr,
            output_frequency_receiver,
            _ffi.NULL,
        )

        raise_on_error(ret)

        return output_frequencies

    def subscribe_gaze_point(self, callback: GazePointCallback) -> None:
        logger.debug(f"{self._url}: subscribing to gaze-point")

        ret = _lib.tobii_gaze_point_subscribe(
            self._device_ptr,
            _lib.gaze_point_callback,
            self._handle,
        )

        raise_on_error(ret)

        self._gaze_point_callback = callback

    def unsubscribe_gaze_point(self) -> None:
        if self._gaze_point_callback is None:
            return

        logger.debug(f"{self._url}: unsubscribing from gaze-point")

        ret = _lib.tobii_gaze_point_unsubscribe(
            self._device_ptr,
        )

        raise_on_error(ret)

        self._gaze_point_callback = None

    def _on_gaze_point(self, timestamp: int, gaze_point: GazePoint) -> None:
        if self._gaze_point_callback is None:
            return

        self._gaze_point_callback(
            timestamp=timestamp,
            gaze_point=gaze_point,
        )

    def subscribe_gaze_origin(self, callback: GazeOriginCallback) -> None:
        logger.debug(f"{self._url}: subscribing to gaze-origin")

        ret = _lib.tobii_gaze_origin_subscribe(
            self._device_ptr,
            _lib.gaze_origin_callback,
            self._handle,
        )

        raise_on_error(ret)

        self._gaze_origin_callback = callback

    def unsubscribe_gaze_origin(self) -> None:
        if self._gaze_origin_callback is None:
            return

        logger.debug(f"{self._url}: unsubscribing from gaze-origin")

        ret = _lib.tobii_gaze_origin_unsubscribe(
            self._device_ptr,
        )

        raise_on_error(ret)

        self._gaze_origin_callback = None

    def _on_gaze_origin(self, timestamp: int, gaze_origin: GazeOrigin) -> None:
        if self._gaze_origin_callback is None:
            return

        self._gaze_origin_callback(
            timestamp=timestamp,
            gaze_origin=gaze_origin,
        )

    def subscribe_eye_position(self, callback: EyePositionCallback) -> None:
        logger.debug(f"{self._url}: subscribing to eye-position")

        ret = _lib.tobii_eye_position_normalized_subscribe(
            self._device_ptr,
            _lib.eye_position_normalized_callback,
            self._handle,
        )

        raise_on_error(ret)

        self._eye_position_callback = callback

    def unsubscribe_eye_position(self) -> None:
        if self._eye_position_callback is None:
            return

        logger.debug(f"{self._url}: unsubscribing from eye-position")

        ret = _lib.tobii_eye_position_normalized_unsubscribe(
            self._device_ptr,
        )

        raise_on_error(ret)

        self._eye_position_callback = None

    def _on_eye_position(self, timestamp: int, eye_position: EyePosition) -> None:
        if self._eye_position_callback is None:
            return

        self._eye_position_callback(
            timestamp=timestamp,
            eye_position=eye_position,
        )

    def subscribe_user_presence(self, callback: UserPresenceCallback) -> None:
        logger.debug(f"{self._url}: subscribing to user-presence")

        ret = _lib.tobii_user_presence_subscribe(
            self._device_ptr,
            _lib.user_presence_callback,
            self._handle,
        )

        raise_on_error(ret)

        self._user_presence_callback = callback

    def unsubscribe_user_presence(self) -> None:
        if self._user_presence_callback is None:
            return

        logger.debug(f"{self._url}: unsubscribing from user-presence")

        ret = _lib.tobii_user_presence_unsubscribe(
            self._device_ptr,
        )

        raise_on_error(ret)

        self._user_presence_callback = None

    def _on_user_presence(self, timestamp: int, user_presence: UserPresence) -> None:
        if self._user_presence_callback is None:
            return

        self._user_presence_callback(
            timestamp=timestamp,
            user_presence=user_presence,
        )

    def run(self) -> None:
        logger.debug(f"{self._url}: starting loop")

        while True:
            ret = _lib.tobii_wait_for_callbacks(1, self._device_ptr_ptr)
            if ret == _lib.TOBII_ERROR_TIMED_OUT:
                continue

            ret = _lib.tobii_device_process_callbacks(self._device_ptr)
