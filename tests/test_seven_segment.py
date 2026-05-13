import unittest

import SevenSegment.segment_types as segment_types
from SevenSegment.segment_types import DigitState, DisplayState, clear_digit
from SevenSegment.glyphs import (
    apply_glyph,
    create_display_for_symbols,
    create_digit_for_symbol,
    supported_symbols,
    write_symbols,
)
from SevenSegment.ascii_renderer import render_digit_ascii, render_display_ascii


class SevenSegmentGlyphTests(unittest.TestCase):
    def test_supported_symbols_include_expected_basics(self) -> None:
        self.assertEqual(
            supported_symbols(),
            (" ", "-", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
        )

    def test_zero_glyph_uses_expected_segments(self) -> None:
        digit = create_digit_for_symbol("0")
        self.assertEqual(
            digit.active_segments(),
            (
                segment_types.SEGMENT_TOP,
                segment_types.SEGMENT_TOP_RIGHT,
                segment_types.SEGMENT_BOTTOM_RIGHT,
                segment_types.SEGMENT_BOTTOM,
                segment_types.SEGMENT_BOTTOM_LEFT,
                segment_types.SEGMENT_TOP_LEFT,
            ),
        )

    def test_hyphen_only_uses_middle_segment(self) -> None:
        digit = create_digit_for_symbol("-")
        self.assertEqual(digit.active_segments(), (segment_types.SEGMENT_MIDDLE,))

    def test_blank_turns_everything_off(self) -> None:
        digit = create_digit_for_symbol(" ")
        self.assertEqual(digit.active_segments(), ())

    def test_unsupported_symbol_raises(self) -> None:
        with self.assertRaises(ValueError):
            create_digit_for_symbol("A")


class SevenSegmentAsciiTests(unittest.TestCase):
    def test_single_digit_ascii_for_eight(self) -> None:
        digit = create_digit_for_symbol("8")
        self.assertEqual(
            render_digit_ascii(digit),
            "\n".join(
                [
                    " ***** ",
                    "*     *",
                    "*     *",
                    " ***** ",
                    "*     *",
                    "*     *",
                    " ***** ",
                ]
            ),
        )

    def test_multi_digit_ascii_for_one_two(self) -> None:
        display = create_display_for_symbols("12")
        self.assertEqual(
            render_display_ascii(display),
            "\n".join(
                [
                    "          ***** ",
                    "      *        *",
                    "      *        *",
                    "          ***** ",
                    "      *  *      ",
                    "      *  *      ",
                    "          ***** ",
                ]
            ),
        )


class SevenSegmentStateTests(unittest.TestCase):
    def test_clear_digit_turns_everything_off(self) -> None:
        digit = create_digit_for_symbol("8")
        clear_digit(digit)
        self.assertEqual(digit.active_segments(), ())

    def test_write_symbols_clears_unused_digits(self) -> None:
        display = DisplayState(4)
        write_symbols(display, "88")
        write_symbols(display, "1")
        self.assertEqual(
            display.digits[0].active_segments(),
            (segment_types.SEGMENT_TOP_RIGHT, segment_types.SEGMENT_BOTTOM_RIGHT),
        )
        self.assertEqual(display.digits[1].active_segments(), ())
        self.assertEqual(display.digits[2].active_segments(), ())
        self.assertEqual(display.digits[3].active_segments(), ())

    def test_write_symbols_rejects_too_many_symbols(self) -> None:
        display = DisplayState(2)
        with self.assertRaises(ValueError):
            write_symbols(display, "123")

    def test_apply_glyph_overwrites_previous_state(self) -> None:
        digit = DigitState()
        apply_glyph(digit, "8")
        apply_glyph(digit, "1")
        self.assertEqual(
            digit.active_segments(),
            (segment_types.SEGMENT_TOP_RIGHT, segment_types.SEGMENT_BOTTOM_RIGHT),
        )


if __name__ == "__main__":
    unittest.main()
