#!/usr/bin/env python3
"""Build a platform wheel containing the Rust engine; no Rust needed at runtime."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

from setuptools import Distribution, setup
from setuptools.command.build_py import build_py
from setuptools.command.bdist_wheel import bdist_wheel

ROOT = Path(__file__).resolve().parent


class NativeDistribution(Distribution):
    def has_ext_modules(self):
        return True


class BuildNative(build_py):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        if package == "Mejiro.dictionaries.default":
            # Legacy Python rules are retained as a migration oracle in the
            # source checkout, but never shipped or imported by the plugin.
            modules = [m for m in modules if m[1] in ("__init__", "mejiro", "recording")]
        return modules

    def run(self):
        source = Path(os.environ.get("MEJIRO_ENGINE_SOURCE", ROOT / "vendor/mejiro-engine")).resolve()
        target = (ROOT / "build/rust").resolve()
        subprocess.run(["cargo", "build", "--locked", "--release", "-p", "mejiro-native",
                        "--manifest-path", str(source / "Cargo.toml"),
                        "--target-dir", str(target)], check=True)
        super().run()
        name = ("mejiro_native.dll" if sys.platform == "win32" else
                "libmejiro_native.dylib" if sys.platform == "darwin" else
                "libmejiro_native.so")
        destination = Path(self.build_lib) / "Mejiro/_native"
        destination.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(target / "release" / name, destination / name)


class NativeWheel(bdist_wheel):
    def get_tag(self):
        _, _, platform = super().get_tag()
        return "py3", "none", platform


setup(include_package_data=True, distclass=NativeDistribution,
      cmdclass={"build_py": BuildNative, "bdist_wheel": NativeWheel})
