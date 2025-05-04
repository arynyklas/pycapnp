import sys
import os

from setuptools.build_meta import *  # noqa: F401, F403
from setuptools.build_meta import build_wheel

backend_class = build_wheel.__self__.__class__


TRUTHY_VALUES = ('true', '1', 't')
FALSY_VALUES = ('false', '0', 'f')
VALID_VALUES = TRUTHY_VALUES + FALSY_VALUES


class _CustomBuildMetaBackend(backend_class):
    def run_setup(self, setup_script="setup.py"):
        force_bundler_libcapnp = os.environ.get("FORCE_BUNDLED_LIBCAPNP")
        force_system_libcapnp = os.environ.get("FORCE_SYSTEM_LIBCAPNP")

        if force_bundler_libcapnp is not None:
            if force_bundler_libcapnp not in VALID_VALUES:
                raise ValueError(f"FORCE_BUNDLED_LIBCAPNP must be one of {VALID_VALUES}, not {force_bundler_libcapnp!r}")

            force_bundler_libcapnp = force_bundler_libcapnp.lower() in TRUTHY_VALUES

        if force_system_libcapnp is not None:
            if force_system_libcapnp not in VALID_VALUES:
                raise ValueError(f"FORCE_SYSTEM_LIBCAPNP must be one of {VALID_VALUES}, not {force_system_libcapnp!r}")

            force_system_libcapnp = force_system_libcapnp.lower() in TRUTHY_VALUES

        if self.config_settings:
            flags = []
            if force_bundler_libcapnp or self.config_settings.get("force-bundled-libcapnp"):
                flags.append("--force-bundled-libcapnp")
            if force_system_libcapnp or self.config_settings.get("force-system-libcapnp"):
                flags.append("--force-system-libcapnp")
            if self.config_settings.get("libcapnp-url"):
                flags.append("--libcapnp-url")
                flags.append(self.config_settings["libcapnp-url"])
            if flags:
                sys.argv = sys.argv[:1] + ["build_ext"] + flags + sys.argv[1:]
        return super().run_setup(setup_script)

    def build_wheel(
        self, wheel_directory, config_settings=None, metadata_directory=None
    ):
        self.config_settings = config_settings
        return super().build_wheel(wheel_directory, config_settings, metadata_directory)


build_wheel = _CustomBuildMetaBackend().build_wheel
