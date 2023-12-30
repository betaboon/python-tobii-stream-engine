from tobii_stream_engine import Api, Device, GazePoint, Stream


def on_gaze_point(timestamp: int, gaze_point: GazePoint) -> None:
    print(f"{gaze_point=}")


def main() -> None:
    api = Api()

    device_urls = api.enumerate_local_device_urls()

    if not len(device_urls):
        print("no device found")
        return

    device = Device(api=api, url=device_urls[0])

    if not device.is_supported_stream(Stream.GAZE_POINT):
        print("gaze-point not supported")
        return

    device.subscribe_gaze_point(callback=on_gaze_point)
    device.run()


if __name__ == "__main__":
    main()
