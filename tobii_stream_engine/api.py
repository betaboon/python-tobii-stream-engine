import logging
from dataclasses import dataclass
from typing import Any

from _tobii_stream_engine_cffi import ffi as _ffi  # type: ignore
from _tobii_stream_engine_cffi import lib as _lib

from tobii_stream_engine.errors import raise_on_error

logger = logging.getLogger(__name__)


_log_level_map = {
    _lib.TOBII_LOG_LEVEL_ERROR: logging.ERROR,
    _lib.TOBII_LOG_LEVEL_WARN: logging.WARNING,
    _lib.TOBII_LOG_LEVEL_INFO: logging.INFO,
    _lib.TOBII_LOG_LEVEL_DEBUG: logging.DEBUG,
    _lib.TOBII_LOG_LEVEL_TRACE: logging.DEBUG,
}


@_ffi.callback("tobii_log_func_t")  # type: ignore
def _custom_logger(log_context: Any, level: int, text: _ffi.CData) -> None:
    log_level = _log_level_map[level]
    log_msg = _ffi.string(text).decode()
    logger.log(level=log_level, msg=log_msg)


class Api:
    def __init__(self, enable_library_logging: bool = False) -> None:
        self._api_ptr: _ffi.CDATA
        self._create(create_custom_logger=enable_library_logging)

    def __del__(self) -> None:
        self._destroy()

    def _create(self, create_custom_logger: bool) -> None:
        logger.debug("creating api")

        api_ptr = _ffi.new("tobii_api_t **")

        custom_log = _ffi.NULL
        if create_custom_logger:
            custom_log = _ffi.new("tobii_custom_log_t *")
            custom_log.log_context = _ffi.NULL
            custom_log.log_func = _custom_logger

        ret = _lib.tobii_api_create(
            api_ptr,
            _ffi.NULL,
            custom_log,
        )

        raise_on_error(ret)

        self._api_ptr = api_ptr[0]

    def _destroy(self) -> None:
        logger.debug("destroying api")

        ret = _lib.tobii_api_destroy(
            self._api_ptr,
        )

        raise_on_error(ret)

        self._api_ptr = None

    def get_system_clock(self) -> int:
        logger.debug("getting system-clock")

        timestamp_us = _ffi.new("int64_t *")

        ret = _lib.tobii_system_clock(
            self._api_ptr,
            timestamp_us,
        )

        raise_on_error(ret)

        return int(_ffi.cast("intptr_t", timestamp_us[0]))

    def enumerate_local_device_urls(self) -> list[str]:
        logger.debug("getting device-urls")

        device_urls = []

        # TODO migrate to def_external
        @_ffi.callback("tobii_device_url_receiver_t")  # type: ignore
        def url_receiver(url, user_data) -> None:
            device_url = _ffi.string(url).decode()
            device_urls.append(device_url)

        ret = _lib.tobii_enumerate_local_device_urls(
            self._api_ptr,
            url_receiver,
            _ffi.NULL,
        )

        raise_on_error(ret)

        return device_urls


@dataclass(frozen=True)
class ApiVersion:
    major: int
    minor: int
    revision: int
    build: int


def get_api_version() -> ApiVersion:
    logger.debug("getting api version")

    version = _ffi.new("tobii_version_t *")

    ret = _lib.tobii_get_api_version(
        version,
    )

    raise_on_error(ret)

    return ApiVersion(
        major=version.major,
        minor=version.minor,
        revision=version.revision,
        build=version.build,
    )
