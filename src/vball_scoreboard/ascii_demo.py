"""Manual ASCII demo for the scoreboard package.

Examples:
    python -m vball_scoreboard.ascii_demo
    python -m vball_scoreboard.ascii_demo 1234
    python -m vball_scoreboard.ascii_demo "8-1 "
"""

import sys

from .ascii_renderer import render_display_ascii
from .glyphs import create_display_for_symbols, supported_symbols

DEFAULT_SYMBOLS = "1234"


# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    symbols = DEFAULT_SYMBOLS
    if len(sys.argv) >= 2:
        symbols = sys.argv[1]

    try:
        display = create_display_for_symbols(symbols)
    except ValueError as error:
        print("Error:", error)
        print("Supported symbols:", " ".join(supported_symbols()))
        _print_usage()
        return 1

    print("Symbols:", repr(symbols))
    print(render_display_ascii(display))
    return 0


# Usage Output
# ---------------------------------------------------------------------------
def _print_usage() -> None:
    print("Usage: python -m vball_scoreboard.ascii_demo [symbols]")
    print("Example: python -m vball_scoreboard.ascii_demo 1234")
    print('Example: python -m vball_scoreboard.ascii_demo "8-1 "')


if __name__ == "__main__":
    raise SystemExit(main())
