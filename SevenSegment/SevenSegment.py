from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List

# Segment identity (Enum)
# -------------------------
class SegmentName(Enum):
    Top = auto()
    TopRight = auto()
    BottomRight = auto()
    Bottom = auto()
    BottomLeft = auto()
    TopLeft = auto()
    Middle = auto()

# Data model
# -------------------------
# one of 7 segments in a display digit
@dataclass
class Segment:
    isOn: bool = False

# one digit with 7 segments
# nb: does not need to be an actual number, just any shape that can be made with 7 segments.
@dataclass
class Digit:
    color: str = "white"
    segments: Dict[SegmentName, Segment] = field(
        default_factory=lambda: {name: Segment() for name in SegmentName}
    )

# all of our digits combine to form the display.
@dataclass
class Display:
    digits: List[Digit] = field(default_factory=list)


# Public Clock API
# -------------------------
def ClearDisplay(display: Display) -> None:
    """Turn off all segments in every digit of the display."""
    for digit in display.digits:
        for segment in digit.segments.values():
            segment.isOn = False

# Public ASCII Debug API
# -------------------------
def MakeDigitASCII(digit: Digit) -> str:
    """Return a 7-row ASCII representation of a single seven-segment digit."""
    segments = digit.segments
    ascii_rows: List[str] = [
        _DrawHorizontalSegment(segments[SegmentName.Top].isOn),
        _DrawVerticalSegment(segments[SegmentName.TopLeft].isOn, segments[SegmentName.TopRight].isOn),
        _DrawVerticalSegment(segments[SegmentName.TopLeft].isOn, segments[SegmentName.TopRight].isOn),
        _DrawHorizontalSegment(segments[SegmentName.Middle].isOn),
        _DrawVerticalSegment(segments[SegmentName.BottomLeft].isOn, segments[SegmentName.BottomRight].isOn),
        _DrawVerticalSegment(segments[SegmentName.BottomLeft].isOn, segments[SegmentName.BottomRight].isOn),
        _DrawHorizontalSegment(segments[SegmentName.Bottom].isOn),
    ]
    return "\n".join(ascii_rows)

def MakeDigitsASCII(digits: List[Digit], gapSpaces: int = 2) -> str:
    """
    Return a multi-digit ASCII string by rendering each Digit and stitching rows side-by-side.
    gap_spaces controls the number of spaces between digits.
    """
    digit_ascii_list: List[str] = [MakeDigitASCII(digit) for digit in digits]
    return CombineDigitASCIIStrings(digit_ascii_list, gapSpaces)

def CombineDigitASCIIStrings(digit_ascii_list: List[str], gapSpaces: int = 2) -> str:
    """
    Given a list of single-digit ASCII strings (each 7 rows), combine them horizontally.
    """
    if not digit_ascii_list:
        return ""

    gap_text = " " * gapSpaces
    # For every string in digit_ascii_list, call .splitlines() on it, and collect those into digit_rows_list..
    digit_rows_list: List[List[str]] = [digit_ascii.splitlines() for digit_ascii in digit_ascii_list]

    # Validation, every string should be same length if we did this properly
    expected_rows = len(digit_rows_list[0])
    for rows in digit_rows_list:
        if len(rows) != expected_rows:
            return "Erorr--not every line is same length wtf?"

    combined_rows: List[str] = []
    # now go through each row and join them together seperated by the gap.
    for row_index in range(expected_rows):
        row_parts = [rows[row_index] for rows in digit_rows_list]
        combined_rows.append(gap_text.join(row_parts))

    # then add a new line between each of our rows and we are good to go.
    return "\n".join(combined_rows)

# Internal helpers - ASCII
# -------------------------
def _DrawHorizontalSegment(isOn: bool) -> str:
    """Return ASCII for a horizontal segment row (width 7, padded 1 on each side)."""
    return " " + ("*****" if isOn else "     ") + " "

def _DrawVerticalSegment(is_left_on: bool, is_right_on: bool) -> str:
    """Return ASCII for a vertical pair row: left edge, 5 spaces, right edge."""
    left_edge = "*" if is_left_on else " "
    right_edge = "*" if is_right_on else " "
    return f"{left_edge}" + "     " + f"{right_edge}"


# Testing in Main
# -------------------------
if __name__ == "__main__":
    example_digit = Digit()
    example_digit.segments[SegmentName.Top].isOn = True

    
    print(MakeDigitASCII(example_digit)) 

    right_digit = Digit()
    
    right_digit.segments[SegmentName.Top].isOn = True
    right_digit.segments[SegmentName.Bottom].isOn = True

    print(MakeDigitsASCII([example_digit, right_digit]))
 

