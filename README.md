# Local Development And Board Deploy

## Local Host Setup

Install the project in editable mode from the repository root:

```powershell
pip install -e .[dev]
```

This exposes the shared package as `vball_scoreboard`.

## Firmware Deploy To Board

Deploy code to a mounted board by explicitly providing its mount path:

```powershell
python tools/sync_to_board.py --board-path <path-to-CIRCUITPY>
```

What gets copied:
- `firmware/code.py` -> `<board>/code.py`
- `src/vball_scoreboard` -> `<board>/lib/vball_scoreboard`
- required `.mpy` libs (currently `neopixel.mpy`) -> `<board>/lib`
