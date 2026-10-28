"""Check the bundled native engine after installing a wheel outside the checkout."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


def main():
    wheels = list(Path(sys.argv[1]).resolve().glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"Expected exactly one wheel, found {len(wheels)}")
    wheel = wheels[0]
    library = ("mejiro_native.dll" if sys.platform == "win32" else
               "libmejiro_native.dylib" if sys.platform == "darwin" else
               "libmejiro_native.so")
    with zipfile.ZipFile(wheel) as archive:
        assert f"Mejiro/_native/{library}" in archive.namelist(), "Native library missing"
    with tempfile.TemporaryDirectory() as directory:
        installed = Path(directory) / "installed"
        env = os.environ.copy()
        env.pop("MEJIRO_ENGINE_LIBRARY", None)
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--no-deps", "--no-index", "--no-cache-dir",
            "--target", str(installed), str(wheel),
        ], cwd=directory, env=env, check=True)
        subprocess.run([
            sys.executable, "-I", "-c",
            "import sys; sys.path.insert(0, sys.argv[1]); "
            "from Mejiro.engine import Engine; "
            "engine = Engine(); "
            "assert engine.preview('KI-').body == '\u304d'; "
            "print('Installed wheel: native engine OK')",
            str(installed),
        ], cwd=directory, env=env, check=True)


if __name__ == "__main__":
    main()
