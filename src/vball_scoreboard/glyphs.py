"""Symbol to seven-segment mapping helpers."""

from .segment_types import (
    DisplayState,
    DigitState,
    SEGMENT_BOTTOM,
    SEGMENT_BOTTOM_LEFT,
    SEGMENT_BOTTOM_RIGHT,
    SEGMENT_MIDDLE,
    SEGMENT_TOP,
    SEGMENT_TOP_LEFT,
    SEGMENT_TOP_RIGHT,
)

GLYPH_SEGMENTS = {
    " ": (),
    "-": (SEGMENT_MIDDLE,),
    "0": (
        SEGMENT_TOP,
        SEGMENT_TOP_RIGHT,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
        SEGMENT_BOTTOM_LEFT,
        SEGMENT_TOP_LEFT,
    ),
    "1": (
        SEGMENT_TOP_RIGHT,
        SEGMENT_BOTTOM_RIGHT,
    ),
    "2": (
        SEGMENT_TOP,
        SEGMENT_TOP_RIGHT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_LEFT,
        SEGMENT_BOTTOM,
    ),
    "3": (
        SEGMENT_TOP,
        SEGMENT_TOP_RIGHT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
    ),
    "4": (
        SEGMENT_TOP_LEFT,
        SEGMENT_TOP_RIGHT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_RIGHT,
    ),
    "5": (
        SEGMENT_TOP,
        SEGMENT_TOP_LEFT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
    ),
    "6": (
        SEGMENT_TOP,
        SEGMENT_TOP_LEFT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_LEFT,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
    ),
    "7": (
        SEGMENT_TOP,
        SEGMENT_TOP_RIGHT,
        SEGMENT_BOTTOM_RIGHT,
    ),
    "8": (
        SEGMENT_TOP,
        SEGMENT_TOP_RIGHT,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
        SEGMENT_BOTTOM_LEFT,
        SEGMENT_TOP_LEFT,
        SEGMENT_MIDDLE,
    ),
    "9": (
        SEGMENT_TOP,
        SEGMENT_TOP_LEFT,
        SEGMENT_TOP_RIGHT,
        SEGMENT_MIDDLE,
        SEGMENT_BOTTOM_RIGHT,
        SEGMENT_BOTTOM,
    ),
}


def supported_symbols() -> tuple:
    symbols = list(GLYPH_SEGMENTS.keys())
    symbols.sort()
    return tuple(symbols)


def get_glyph_segments(symbol: str) -> tuple:
    if symbol not in GLYPH_SEGMENTS:
        raise ValueError("Unsupported seven-segment symbol: %r" % symbol)
    return GLYPH_SEGMENTS[symbol]


def apply_glyph(digit: DigitState, symbol: str) -> None:
    digit.clear()
    for segment_id in get_glyph_segments(symbol):
        digit.set_segment(segment_id, True)


def create_digit_for_symbol(symbol: str) -> DigitState:
    digit = DigitState()
    apply_glyph(digit, symbol)
    return digit


def write_symbols(display: DisplayState, symbols) -> None:
    if len(symbols) > display.digit_count():
        raise ValueError("Too many symbols for display")

    display.clear()
    for digit_index, symbol in enumerate(symbols):
        apply_glyph(display.digits[digit_index], symbol)


def create_display_for_symbols(symbols) -> DisplayState:
    display = DisplayState(len(symbols))
    write_symbols(display, symbols)
    return display
