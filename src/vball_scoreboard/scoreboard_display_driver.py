"""LED mapping and render helpers for the four-digit scoreboard."""

from .segment_types import ALL_SEGMENTS, DisplayState

SegmentKey = tuple[int, int]

# LED Mapping Constants
# ---------------------------------------------------------------------------
# Editable mapping: (digit_index, segment_id) -> tuple(pixel_index, ...).
# This placeholder mapping covers all 28 keys with variable-length tuples.
DIGIT_SEGMENT_PIXEL_MAP: dict[SegmentKey, tuple[int, ...]] = {
    (0, 0): (0, 1),    # Digit:0 Segment:top
    (0, 1): (2, 3),    # Digit:0 Segment:top_right
    (0, 2): (4, 5),    # Digit:0 Segment:bottom_right
    (0, 3): (6, 7),    # Digit:0 Segment:bottom
    (0, 4): (8, 9),    # Digit:0 Segment:bottom_left
    (0, 5): (10, 11),  # Digit:0 Segment:top_left
    (0, 6): (12, 13),  # Digit:0 Segment:middle
    (1, 0): (14, 15),  # Digit:1 Segment:top
    (1, 1): (16, 17),  # Digit:1 Segment:top_right
    (1, 2): (18, 19),  # Digit:1 Segment:bottom_right
    (1, 3): (20, 21),  # Digit:1 Segment:bottom
    (1, 4): (22, 23),  # Digit:1 Segment:bottom_left
    (1, 5): (24, 25),  # Digit:1 Segment:top_left
    (1, 6): (26, 27),  # Digit:1 Segment:middle
    (2, 0): (28, 29),  # Digit:2 Segment:top
    (2, 1): (30, 31),  # Digit:2 Segment:top_right
    (2, 2): (32, 33),  # Digit:2 Segment:bottom_right
    (2, 3): (34, 35),  # Digit:2 Segment:bottom
    (2, 4): (36, 37),  # Digit:2 Segment:bottom_left
    (2, 5): (38, 39),  # Digit:2 Segment:top_left
    (2, 6): (40, 41),  # Digit:2 Segment:middle
    (3, 0): (42, 43),  # Digit:3 Segment:top
    (3, 1): (44, 45),  # Digit:3 Segment:top_right
    (3, 2): (46, 47),  # Digit:3 Segment:bottom_right
    (3, 3): (48, 49),  # Digit:3 Segment:bottom
    (3, 4): (50, 51),  # Digit:3 Segment:bottom_left
    (3, 5): (52, 53),  # Digit:3 Segment:top_left
    (3, 6): (54, 55),  # Digit:3 Segment:middle
}


# Driver
# ---------------------------------------------------------------------------
class ScoreboardDisplayDriver:
    """Applies DisplayState to a NeoPixel-like pixel buffer."""

    _pixels: object
    _segment_pixel_map: dict[SegmentKey, tuple[int, ...]]
    _on_color: tuple[int, int, int]
    _off_color: tuple[int, int, int]
    _warned_missing_keys: set[SegmentKey]
    _warned_out_of_range_indices: set[int]

    def __init__(
        self,
        pixels: object,
        segment_pixel_map: dict[SegmentKey, tuple[int, ...]],
        on_color: tuple[int, int, int] = (0, 255, 0),
        off_color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        self._pixels = pixels
        self._segment_pixel_map = segment_pixel_map
        self._on_color = on_color
        self._off_color = off_color
        self._warned_missing_keys = set()
        self._warned_out_of_range_indices = set()

    def get_mapped_pixels(self, digit_index: int, segment_id: int) -> tuple[int, ...]:
        key: SegmentKey = (digit_index, segment_id)
        if key not in self._segment_pixel_map:
            self._warn_missing_key_once(key)
            return ()
        return self._segment_pixel_map[key]

    def render(self, display: DisplayState) -> None:
        pixel_count: int = len(self._pixels)

        for pixel_index in range(pixel_count):
            self._pixels[pixel_index] = self._off_color

        for digit_index, digit in enumerate(display.digits):
            for segment_id in ALL_SEGMENTS:
                if not digit.is_segment_on(segment_id):
                    continue
                pixel_indices: tuple[int, ...] = self.get_mapped_pixels(digit_index, segment_id)
                for pixel_index in pixel_indices:
                    if pixel_index < 0 or pixel_index >= pixel_count:
                        self._warn_out_of_range_once(pixel_index)
                        continue
                    self._pixels[pixel_index] = self._on_color

        if hasattr(self._pixels, "show"):
            self._pixels.show()

    def _warn_missing_key_once(self, key: SegmentKey) -> None:
        if key in self._warned_missing_keys:
            return
        self._warned_missing_keys.add(key)
        print("WARN: missing segment mapping for key=%s" % (key,))

    def _warn_out_of_range_once(self, pixel_index: int) -> None:
        if pixel_index in self._warned_out_of_range_indices:
            return
        self._warned_out_of_range_indices.add(pixel_index)
        print("WARN: pixel index out of range: %d" % pixel_index)


# Calibration Builders
# ---------------------------------------------------------------------------
def build_calibration_steps(digit_count: int) -> tuple[SegmentKey, ...]:
    if digit_count < 0:
        raise ValueError("digit_count must be non-negative")

    steps: list[SegmentKey] = []
    for digit_index in range(digit_count):
        for segment_id in ALL_SEGMENTS:
            steps.append((digit_index, segment_id))
    return tuple(steps)


def create_calibration_display(digit_count: int, active_digit: int, active_segment: int) -> DisplayState:
    display = DisplayState(digit_count)
    display.digits[active_digit].set_segment(active_segment, True)
    return display
