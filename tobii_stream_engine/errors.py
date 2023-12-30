from _tobii_stream_engine_cffi import ffi as _ffi  # type: ignore
from _tobii_stream_engine_cffi import lib as _lib  # type: ignore


class TobiiError(Exception):
    ...


class TobiiInternalError(TobiiError):
    ...


class TobiiInsufficientLicenseError(TobiiError):
    ...


class TobiiNotSupportedError(TobiiError):
    ...


class TobiiNotAvailableError(TobiiError):
    ...


class TobiiConnectionFailedError(TobiiError):
    ...


class TobiiTimedOutError(TobiiError):
    ...


class TobiiAllocationFailedError(TobiiError):
    ...


class TobiiInvalidParameterError(TobiiError):
    ...


class TobiiCalibrationAlreadyStartedError(TobiiError):
    ...


class TobiiCalibrationNotStartedError(TobiiError):
    ...


class TobiiAlreadySubscribedError(TobiiError):
    ...


class TobiiNotSubscribedError(TobiiError):
    ...


class TobiiOperationFailedError(TobiiError):
    ...


class TobiiConflictingApiInstancesError(TobiiError):
    ...


class TobiiCalibrationBusyError(TobiiError):
    ...


class TobiiCallbackInProgressError(TobiiError):
    ...


class TobiiTooManySubscribersError(TobiiError):
    ...


class TobiiConnectionFailedDriverError(TobiiError):
    ...


_exception_map = {
    _lib.TOBII_ERROR_INTERNAL: TobiiInternalError,
    _lib.TOBII_ERROR_INSUFFICIENT_LICENSE: TobiiInsufficientLicenseError,
    _lib.TOBII_ERROR_NOT_SUPPORTED: TobiiNotSupportedError,
    _lib.TOBII_ERROR_NOT_AVAILABLE: TobiiNotAvailableError,
    _lib.TOBII_ERROR_CONNECTION_FAILED: TobiiConnectionFailedError,
    _lib.TOBII_ERROR_TIMED_OUT: TobiiTimedOutError,
    _lib.TOBII_ERROR_ALLOCATION_FAILED: TobiiAllocationFailedError,
    _lib.TOBII_ERROR_INVALID_PARAMETER: TobiiInvalidParameterError,
    _lib.TOBII_ERROR_CALIBRATION_ALREADY_STARTED: TobiiCalibrationAlreadyStartedError,
    _lib.TOBII_ERROR_CALIBRATION_NOT_STARTED: TobiiCalibrationNotStartedError,
    _lib.TOBII_ERROR_ALREADY_SUBSCRIBED: TobiiAlreadySubscribedError,
    _lib.TOBII_ERROR_NOT_SUBSCRIBED: TobiiNotSupportedError,
    _lib.TOBII_ERROR_OPERATION_FAILED: TobiiOperationFailedError,
    _lib.TOBII_ERROR_CONFLICTING_API_INSTANCES: TobiiConflictingApiInstancesError,
    _lib.TOBII_ERROR_CALIBRATION_BUSY: TobiiCalibrationBusyError,
    _lib.TOBII_ERROR_CALLBACK_IN_PROGRESS: TobiiCallbackInProgressError,
    _lib.TOBII_ERROR_TOO_MANY_SUBSCRIBERS: TobiiTooManySubscribersError,
    _lib.TOBII_ERROR_CONNECTION_FAILED_DRIVER: TobiiConnectionFailedDriverError,
}


def raise_on_error(return_value: int) -> None:
    if return_value == _lib.TOBII_ERROR_NO_ERROR:
        return

    exception_class = _exception_map.get(return_value, TobiiError)
    error_message = _lib.tobii_error_message(return_value)
    error_message = _ffi.string(error_message).decode()
    raise exception_class(error_message)
