"""Deploy firmware and shared package code to a mounted CIRCUITPY board."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

THIRD_PARTY_MPY_LIBS: tuple[str, ...] = ("neopixel.mpy",)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync local firmware artifacts to a mounted CIRCUITPY board."
    )
    parser.add_argument(
        "--board-path",
        required=True,
        help="Path to the mounted CIRCUITPY volume (for example E:\\ or /Volumes/CIRCUITPY).",
    )
    return parser.parse_args()


def _copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    print("copied file: %s -> %s" % (source, destination))


def _copy_tree(source: Path, destination: Path) -> None:
    shutil.copytree(source, destination)
    print("copied tree: %s -> %s" % (source, destination))


def _sync(board_path: Path, repo_root: Path) -> None:
    if not board_path.exists():
        raise FileNotFoundError("Board path does not exist: %s" % board_path)
    if not board_path.is_dir():
        raise NotADirectoryError("Board path is not a directory: %s" % board_path)

    firmware_code: Path = repo_root / "firmware" / "code.py"
    package_source: Path = repo_root / "src" / "vball_scoreboard"
    libs_source: Path = repo_root / "firmware" / "lib"

    if not firmware_code.exists():
        raise FileNotFoundError("Missing firmware entrypoint: %s" % firmware_code)
    if not package_source.exists():
        raise FileNotFoundError("Missing package source: %s" % package_source)

    board_code: Path = board_path / "code.py"
    board_lib: Path = board_path / "lib"
    deployed_package: Path = board_lib / "vball_scoreboard"

    if deployed_package.exists():
        shutil.rmtree(deployed_package)
        print("removed stale package: %s" % deployed_package)

    _copy_file(firmware_code, board_code)
    board_lib.mkdir(parents=True, exist_ok=True)
    _copy_tree(package_source, deployed_package)

    for lib_name in THIRD_PARTY_MPY_LIBS:
        source_lib: Path = libs_source / lib_name
        if not source_lib.exists():
            raise FileNotFoundError("Missing required third-party library: %s" % source_lib)
        _copy_file(source_lib, board_lib / lib_name)


def main() -> int:
    args = _parse_args()
    script_path: Path = Path(__file__).resolve()
    repo_root: Path = script_path.parent.parent
    board_path: Path = Path(args.board_path).resolve()

    _sync(board_path, repo_root)
    print("sync complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
