
# Lazor Stage 2: Parsing & Data Structures (Starter)

This mini-package provides:
- A robust `.bff` parser (`parse_bff`) that reads GRID, counts (A/B/C), lasers (`L x y vx vy`), and points (`P x y`).
- Core data classes (`Block`, `Laser`, `Board`) with a clean API to hold the game state.

## File layout
- `lazor_core/models.py` — dataclasses and enums
- `lazor_core/board.py`  — Board container with helpers
- `lazor_core/parser.py` — `parse_bff(path)` implementation
- `parse_bff_demo.py`    — Command-line demo

## Quick start
```bash
python parse_bff_demo.py /path/to/your_board.bff
```

The demo prints a summary and ASCII view of the grid, including any fixed blocks encoded in the GRID.

## Notes
- We treat `A/B/C` inside the `GRID` as *fixed* blocks. The base `grid` keeps only `o`/`x`.
- Free blocks from lines like `A 2` remain available to place later (solving stage).
- Laser/point coordinates are stored verbatim in half-block units; geometric validation belongs to the simulation stage.
- `Block.interact(...)` contains **placeholder** rules to unblock your Stage 2; finalize physics in Stage 3.
