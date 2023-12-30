cffi_modules = [
    "tobii_stream_engine/builder/build.py:ffibuilder",
]


def pdm_build_update_setup_kwargs(context, setup_kwargs):  # type: ignore
    setup_kwargs.update(cffi_modules=cffi_modules)
