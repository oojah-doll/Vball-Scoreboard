"""Runtime loop for scoreboard bring-up and mapping calibration."""

import time

try:
    import board  # type: ignore
    import neopixel  # type: ignore
except ImportError:
    board = None
    neopixel = None

from .ascii_renderer import render_display_ascii
from .glyphs import supported_symbols, write_symbols
from .segment_types import DisplayState, SEGMENT_NAMES

from .scoreboard_display_driver import (
    DIGIT_SEGMENT_PIXEL_MAP,
    ScoreboardDisplayDriver,
    build_calibration_steps,
    create_calibration_display,
)

MODE_CYCLE: int = 0
MODE_CALIBRATION: int = 1
RUN_MODE: int = MODE_CYCLE

DIGIT_COUNT: int = 4
PIXEL_COUNT: int = 70

PIXEL_BRIGHTNESS: float = 0.20

CYCLE_VALUES: tuple[str, ...] = ("0000", "0102", "9913", "9999")
CYCLE_STEP_SECONDS: float = 2.0
CALIBRATION_STEP_SECONDS: float = 2.5

_WARNED_UNSUPPORTED_SYMBOLS: set[str] = set()
_SUPPORTED_SYMBOLS: set[str] = set(supported_symbols())


class _SimulatedPixels:
    """Host-side fallback so code can run without CircuitPython hardware."""

    _pixels: list[tuple[int, int, int]]

    def __init__(self, pixel_count: int) -> None:
        self._pixels = []
        for _ in range(pixel_count):
            self._pixels.append((0, 0, 0))

    def __len__(self) -> int:
        return len(self._pixels)

    def __setitem__(self, index: int, color: tuple[int, int, int]) -> None:
        self._pixels[index] = color

    def show(self) -> None:
        return


def _create_pixels():
    if board is None or neopixel is None:
        print("WARN: board/neopixel unavailable, using simulated pixel buffer")
        return _SimulatedPixels(PIXEL_COUNT)
    return neopixel.NeoPixel(board.D13, PIXEL_COUNT, brightness=PIXEL_BRIGHTNESS, auto_write=False)


def _sanitize_symbols(raw_value: str) -> tuple[str, ...]:
    sanitized: list[str] = []
    for symbol in raw_value:
        if symbol in _SUPPORTED_SYMBOLS:
            sanitized.append(symbol)
            continue

        if symbol not in _WARNED_UNSUPPORTED_SYMBOLS:
            print("WARN: unsupported symbol %r; rendering as blank" % symbol)
            _WARNED_UNSUPPORTED_SYMBOLS.add(symbol)
        sanitized.append(" ")
    return tuple(sanitized)


def _render_value(display: DisplayState, value: str) -> None:
    symbols: tuple[str, ...] = _sanitize_symbols(value)
    if len(symbols) < display.digit_count():
        symbols = symbols + (" ",) * (display.digit_count() - len(symbols))
    write_symbols(display, symbols[: display.digit_count()])


def main() -> None:
    if RUN_MODE != MODE_CYCLE and RUN_MODE != MODE_CALIBRATION:
        raise ValueError("RUN_MODE must be MODE_CYCLE or MODE_CALIBRATION")

    pixels = _create_pixels()
    driver = ScoreboardDisplayDriver(pixels, DIGIT_SEGMENT_PIXEL_MAP)
    display = DisplayState(DIGIT_COUNT)

    tick: int = 0
    step_index: int = 0
    calibration_steps: tuple[tuple[int, int], ...] = build_calibration_steps(DIGIT_COUNT)

    while True:
        if RUN_MODE == MODE_CYCLE:
            value: str = CYCLE_VALUES[step_index % len(CYCLE_VALUES)]
            _render_value(display, value)
            driver.render(display)

            print("mode=cycle tick=%d value=%s" % (tick, value))
            print(render_display_ascii(display))

            step_index += 1
            tick += 1
            time.sleep(CYCLE_STEP_SECONDS)
            continue

        active_digit, active_segment = calibration_steps[step_index % len(calibration_steps)]
        display = create_calibration_display(DIGIT_COUNT, active_digit, active_segment)
        driver.render(display)

        segment_name: str = SEGMENT_NAMES[active_segment]
        mapped_pixels: tuple[int, ...] = driver.get_mapped_pixels(active_digit, active_segment)
        print(
            "mode=calibration tick=%d digit=%d segment=%s pixels=%s"
            % (tick, active_digit, segment_name, mapped_pixels)
        )
        print(render_display_ascii(display))

        step_index += 1
        tick += 1
        time.sleep(CALIBRATION_STEP_SECONDS)


# Standard module entrypoint so `python -m vball_scoreboard.runtime` runs the loop.
if __name__ == "__main__":
    main()
