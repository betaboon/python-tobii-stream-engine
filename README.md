# tobii-stream-engine

> [!IMPORTANT]
> This is an unofficial library!

## Introduction

The [Tobii Eye Tracker 5](https://gaming.tobii.com/product/eye-tracker-5/) is an affordable, consumer-grade eye tracker.

It is not officially supported on linux.

This library is a [cffi](https://cffi.readthedocs.io/en/stable/)-wrapper for the undocumented `tobii-stream-engine` contained in the official `Tobii Pro SDK`.

## Usage

```python
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
```

## Preconditions

### Tobii Pro SDK

Download and install the [Tobii Pro SDK C for Linux](https://connect.tobii.com/s/sdk-c-linux-form).

### tobiiusbservice

Download and install the `tobiiusbservice`.

It is not contained in this repository for licensing reasons.

Use the search-engine of your choice to locate it.

To install it:
```sh
sudo dpkg -i tobiiusbservice_l64U14_2.1.5-28fd4a.deb
```

It has been found that the directory `/var/run/tobiiusb` has to exist for it to start.
```sh
sudo mkdir -p /var/run/tobiiusb
```

To start it:
```sh
sudo tobiiusbserviced
```

To enable debug logging:
```
sudo sh -c "echo 4 | nc -U /var/run/tobii_log"
```

### Build dependencies

```sh
apt install build-essential python3.10-dev
```

## Installation

```sh
export LD_LIBRARY_PATH=/usr/local/lib/libtobii_research

pip install git+https://github.com/betaboon/python-tobii-stream-engine.git
```

## Examples

- [subscriptions](./examples/subscriptions.py)

## Background

`Tobii Pro SDK` provides `libtobii_research.so` whose interface is documented[^1].

As it turns out, this library contains all the exports that are present in `libtobii_stream_engine.so`, but they are undocumented.

Luckily documentation for `Tobii Stream Engine` is publicly available[^2].

For the CFFI wrapper we generate header-files from this documentation[^3].

[^1]: https://developer.tobiipro.com/c/c-sdk-reference-guide.html
[^2]: https://tobiitech.github.io/stream-engine-docs/
[^3]: [tobii_stream_engine/builder/build_header_files.py](https://github.com/betaboon/python-tobii-stream-engine/blob/main/tobii_stream_engine/builder/build_header_files.py)

## Prior work

- https://github.com/Eitol/tobii_eye_tracker_linux_installer
