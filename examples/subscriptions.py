import logging

from tobii_stream_engine import (
    Api,
    Device,
    EyePosition,
    GazeOrigin,
    GazePoint,
    Stream,
    UserPresence,
    get_api_version,
)


def on_gaze_point(timestamp: int, gaze_point: GazePoint) -> None:
    print(f"{gaze_point=}")


def on_gaze_origin(timestamp: int, gaze_origin: GazeOrigin) -> None:
    print(f"{gaze_origin=}")


def on_eye_position(timestamp: int, eye_position: EyePosition) -> None:
    print(f"{eye_position=}")


def on_user_presence(timestamp: int, user_presence: UserPresence) -> None:
    print(f"{user_presence=}")


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    version = get_api_version()
    print(f"{version=}")

    api = Api()

    system_clock = api.get_system_clock()
    print(f"{system_clock=}")

    device_urls = api.enumerate_local_device_urls()
    print(f"{device_urls=}")

    if not len(device_urls):
        print("no devices found.")
        return

    device = Device(api=api, url=device_urls[0])

    device_info = device.get_device_info()
    print(f"{device_info=}")

    supported_capabilities = device.get_supported_capabilities()
    print(f"{supported_capabilities=}")

    supported_streams = device.get_supported_streams()
    print(f"{supported_streams=}")

    if Stream.GAZE_POINT in supported_streams:
        device.subscribe_gaze_point(callback=on_gaze_point)

    if Stream.GAZE_ORIGIN in supported_streams:
        device.subscribe_gaze_origin(callback=on_gaze_origin)

    if Stream.EYE_POSITION_NORMALIZED in supported_streams:
        device.subscribe_eye_position(callback=on_eye_position)

    if Stream.USER_PRESENCE in supported_streams:
        device.subscribe_user_presence(callback=on_user_presence)

    device.run()


if __name__ == "__main__":
    main()
