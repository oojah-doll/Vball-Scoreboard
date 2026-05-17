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


# Classes
# ---------------------------------------------------------------------------
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


class RuntimeState:
    """Mutable runtime loop state shared by each run-mode step."""

    # Display buffer currently rendered to physical/simulated pixels.
    display: DisplayState
    # Monotonic loop counter used for logging and sequencing visibility.
    tick: int
    # Current index into the mode-specific step sequence.
    step_index: int

    def __init__(self, digit_count: int) -> None:
        self.display = DisplayState(digit_count)
        self.tick = 0
        self.step_index = 0


# Main
# ---------------------------------------------------------------------------
def main() -> None:
    if RUN_MODE != MODE_CYCLE and RUN_MODE != MODE_CALIBRATION:
        raise ValueError("RUN_MODE must be MODE_CYCLE or MODE_CALIBRATION")

    pixels = _create_pixels()
    driver = ScoreboardDisplayDriver(pixels, DIGIT_SEGMENT_PIXEL_MAP)
    state = RuntimeState(DIGIT_COUNT)
    calibration_steps: tuple[tuple[int, int], ...] = build_calibration_steps(DIGIT_COUNT)

    while True:
        if RUN_MODE == MODE_CYCLE:
            _run_cycle_mode_step(state, driver)
            continue

        _run_calibration_mode_step(state, driver, calibration_steps)


# Helper Functions
# ---------------------------------------------------------------------------
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

# Mode logic
# ---------------------------------------------------------------------------
def _run_cycle_mode_step(
    state: RuntimeState,
    driver: ScoreboardDisplayDriver,
) -> None:
    """Cycle through representative scoreboard values for bring-up and debug checks."""
    value: str = CYCLE_VALUES[state.step_index % len(CYCLE_VALUES)]
    _render_value(state.display, value)
    driver.render(state.display)

    print("mode=cycle tick=%d value=%s" % (state.tick, value))
    print(render_display_ascii(state.display))

    time.sleep(CYCLE_STEP_SECONDS)
    state.tick += 1
    state.step_index += 1


def _run_calibration_mode_step(
    state: RuntimeState,
    driver: ScoreboardDisplayDriver,
    calibration_steps: tuple[tuple[int, int], ...],
) -> None:
    """Step slowly through each digit/segment so LED mapping can be visually validated."""
    active_digit, active_segment = calibration_steps[state.step_index % len(calibration_steps)]
    state.display = create_calibration_display(DIGIT_COUNT, active_digit, active_segment)
    driver.render(state.display)

    segment_name: str = SEGMENT_NAMES[active_segment]
    mapped_pixels: tuple[int, ...] = driver.get_mapped_pixels(active_digit, active_segment)
    print(
        "mode=calibration tick=%d digit=%d segment=%s pixels=%s"
        % (state.tick, active_digit, segment_name, mapped_pixels)
    )
    print(render_display_ascii(state.display))

    time.sleep(CALIBRATION_STEP_SECONDS)
    state.tick += 1
    state.step_index += 1


# Standard module entrypoint so `python -m vball_scoreboard.runtime` runs the loop.
if __name__ == "__main__":
    main()
