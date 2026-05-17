"""Core seven-segment data types.

This module is intentionally small and explicit so it stays easy to run on
both desktop Python and CircuitPython.
"""

SEGMENT_TOP = 0
SEGMENT_TOP_RIGHT = 1
SEGMENT_BOTTOM_RIGHT = 2
SEGMENT_BOTTOM = 3
SEGMENT_BOTTOM_LEFT = 4
SEGMENT_TOP_LEFT = 5
SEGMENT_MIDDLE = 6

SEGMENT_COUNT = 7
ALL_SEGMENTS = (
    SEGMENT_TOP,
    SEGMENT_TOP_RIGHT,
    SEGMENT_BOTTOM_RIGHT,
    SEGMENT_BOTTOM,
    SEGMENT_BOTTOM_LEFT,
    SEGMENT_TOP_LEFT,
    SEGMENT_MIDDLE,
)
SEGMENT_NAMES = (
    "top",
    "top_right",
    "bottom_right",
    "bottom",
    "bottom_left",
    "top_left",
    "middle",
)


# Core Types
# ---------------------------------------------------------------------------
class DigitState:
    """Stores the on/off state for one seven-segment digit."""

    _segments: "list[bool]"

    def __init__(self, segments: list = None) -> None:
        if segments is None:
            self._segments = [False, False, False, False, False, False, False]
            return

        if len(segments) != SEGMENT_COUNT:
            raise ValueError("DigitState requires exactly 7 segment values")

        self._segments = []
        for value in segments:
            self._segments.append(bool(value))

    def clear(self) -> None:
        for segment_id in ALL_SEGMENTS:
            self._segments[segment_id] = False

    def copy(self):
        return DigitState(self._segments)

    def set_segment(self, segment_id: int, is_on: bool) -> None:
        _validate_segment(segment_id)
        self._segments[segment_id] = bool(is_on)

    def set_segments(self, segment_ids: list, is_on: bool) -> None:
        for segment_id in segment_ids:
            self.set_segment(segment_id, is_on)

    def is_segment_on(self, segment_id: int) -> bool:
        _validate_segment(segment_id)
        return self._segments[segment_id]

    def to_list(self) -> list:
        return list(self._segments)

    def active_segments(self) -> tuple:
        active = []
        for segment_id in ALL_SEGMENTS:
            if self._segments[segment_id]:
                active.append(segment_id)
        return tuple(active)

    def __repr__(self) -> str:
        return "DigitState(%s)" % self._segments


class DisplayState:
    """Stores a fixed number of digits in display order."""

    digits: "list[DigitState]"

    def __init__(self, digit_count: int) -> None:
        if digit_count < 0:
            raise ValueError("digit_count must be non-negative")

        self.digits = []
        for _ in range(digit_count):
            self.digits.append(DigitState())

    def clear(self) -> None:
        for digit in self.digits:
            digit.clear()

    def digit_count(self) -> int:
        return len(self.digits)

    def copy(self):
        copied_display = DisplayState(0)
        copied_display.digits = []
        for digit in self.digits:
            copied_display.digits.append(digit.copy())
        return copied_display

    """python debug printing"""
    def __repr__(self) -> str:
        return "DisplayState(%s)" % self.digits


# Validation and Utilities
# ---------------------------------------------------------------------------
def _validate_segment(segment_id: int) -> None:
    if segment_id < 0 or segment_id >= SEGMENT_COUNT:
        raise ValueError("segment_id must be in the range [0, 6]")


def clear_digit(digit: DigitState) -> None:
    digit.clear()


def clear_display(display: DisplayState) -> None:
    display.clear()
