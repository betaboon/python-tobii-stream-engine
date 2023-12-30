import os
from pathlib import Path

from cffi import FFI

MODULE_NAME = "_tobii_stream_engine_cffi"

INCLUDE_DIR = Path(__file__).parent / "include"
INCLUDE_FILES = [
    "typedefs.h",
    "tobii.h",
    "tobii_streams.h",
    "tobii_wearable.h",
    "tobii_licensing.h",
    "tobii_config.h",
    "tobii_advanced.h",
]

CDEF = """
    extern "Python" void gaze_point_callback( tobii_gaze_point_t*, void* );
    extern "Python" void gaze_origin_callback( tobii_gaze_origin_t*, void* );
    extern "Python" void eye_position_normalized_callback( tobii_eye_position_normalized_t*, void* );
    extern "Python" void user_presence_callback( tobii_user_presence_status_t, int64_t, void* );
    extern "Python" void notification_callback( tobii_notification_t*, void* );
"""

cdef = ""
source = ""

for include in INCLUDE_FILES:
    include_path = INCLUDE_DIR / include
    cdef += include_path.read_text() + "\n"
    source += f'#include "{include_path.name}"\n'

library_dirs = [
    "/lib",
    "/usr/local/lib",
    "/lib/tobii_research",
    "/usr/local/lib/tobii_research",
]
ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
library_dirs.extend(ld_library_path.split(":"))

ffibuilder = FFI()
ffibuilder.cdef(cdef + CDEF)
ffibuilder.set_source(
    module_name=MODULE_NAME,
    source=source,
    include_dirs=[
        str(INCLUDE_DIR.absolute()),
    ],
    libraries=["tobii_research"],
    library_dirs=library_dirs,
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
