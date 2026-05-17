"""ASCII rendering for seven-segment digits."""

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

ASCII_DIGIT_HEIGHT = 7


# Public Rendering API
# ---------------------------------------------------------------------------
def render_digit_ascii(digit: DigitState) -> str:
    rows = [
        _draw_horizontal_segment(digit.is_segment_on(SEGMENT_TOP)),
        _draw_vertical_segments(
            digit.is_segment_on(SEGMENT_TOP_LEFT),
            digit.is_segment_on(SEGMENT_TOP_RIGHT),
        ),
        _draw_vertical_segments(
            digit.is_segment_on(SEGMENT_TOP_LEFT),
            digit.is_segment_on(SEGMENT_TOP_RIGHT),
        ),
        _draw_horizontal_segment(digit.is_segment_on(SEGMENT_MIDDLE)),
        _draw_vertical_segments(
            digit.is_segment_on(SEGMENT_BOTTOM_LEFT),
            digit.is_segment_on(SEGMENT_BOTTOM_RIGHT),
        ),
        _draw_vertical_segments(
            digit.is_segment_on(SEGMENT_BOTTOM_LEFT),
            digit.is_segment_on(SEGMENT_BOTTOM_RIGHT),
        ),
        _draw_horizontal_segment(digit.is_segment_on(SEGMENT_BOTTOM)),
    ]
    return "\n".join(rows)


def render_digits_ascii(digits, gap_columns: int = 2) -> str:
    if gap_columns < 0:
        raise ValueError("gap_columns must be non-negative")

    digit_rows = []
    for digit in digits:
        digit_rows.append(render_digit_ascii(digit).splitlines())

    if not digit_rows:
        return ""

    gap_text = " " * gap_columns
    combined_rows = []
    for row_index in range(ASCII_DIGIT_HEIGHT):
        row_parts = []
        for rows in digit_rows:
            row_parts.append(rows[row_index])
        combined_rows.append(gap_text.join(row_parts))

    return "\n".join(combined_rows)


def render_display_ascii(display: DisplayState, gap_columns: int = 2) -> str:
    return render_digits_ascii(display.digits, gap_columns)


def combine_digit_ascii_strings(digit_ascii_list, gap_columns: int = 2) -> str:
    if gap_columns < 0:
        raise ValueError("gap_columns must be non-negative")

    if not digit_ascii_list:
        return ""

    split_digits = []
    for digit_ascii in digit_ascii_list:
        rows = digit_ascii.splitlines()
        if len(rows) != ASCII_DIGIT_HEIGHT:
            raise ValueError("Each ASCII digit must contain exactly 7 rows")
        split_digits.append(rows)

    gap_text = " " * gap_columns
    combined_rows = []
    for row_index in range(ASCII_DIGIT_HEIGHT):
        row_parts = []
        for rows in split_digits:
            row_parts.append(rows[row_index])
        combined_rows.append(gap_text.join(row_parts))

    return "\n".join(combined_rows)


# Segment Drawing Primitives
# ---------------------------------------------------------------------------
def _draw_horizontal_segment(is_on: bool) -> str:
    if is_on:
        return " ***** "
    return "       "


def _draw_vertical_segments(is_left_on: bool, is_right_on: bool) -> str:
    left_edge = " "
    right_edge = " "
    if is_left_on:
        left_edge = "*"
    if is_right_on:
        right_edge = "*"
    return left_edge + "     " + right_edge
