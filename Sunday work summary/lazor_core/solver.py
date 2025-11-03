#!/usr/bin/env python3
"""
Lazor Stage 2 — single-file solver

Run:
    python lazor_solver.py -i <path_to_bff> -o <output_path> [--diagnose]

Features
- Robust .bff parser (GRID, inventory lines, lasers, targets).
- Movable vs fixed blocks (A/B/C in GRID are fixed; counts lines are inventory).
- Ray tracer on a doubled grid (half-step = 1). Physics:
    A (Reflect): reflect on the boundary hit (vertical → flip vx; horizontal → flip vy)
    B (Opaque): absorb ray
    C (Refract): split — original continues + a reflected copy
- Combinational search by block type (no factorial over empties).
- Early exit on first valid solution; optional diagnostics for best partial hit.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
import argparse
import sys

Cell = str
Point = Tuple[int, int]  # doubled-grid point (half-lattice)

@dataclass(frozen=True)
class Ray:
    x: int
    y: int
    vx: int  # normalized to ±1
    vy: int

@dataclass
class Board:
    grid: List[List[Cell]]           # [row][col], row 0 is top
    lasers: List[Ray]
    targets: List[Point]

    @property
    def H(self) -> int:
        return len(self.grid)

    @property
    def W(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def cell_at(self, r: int, c: int) -> Optional[Cell]:
        if 0 <= r < self.H and 0 <= c < self.W:
            return self.grid[r][c]
        return None

def _tok_int(s: str) -> int:
    return int(s.replace("=", ""))

def parse_bff(path: Path) -> Tuple[Board, Dict[str, int], List[Tuple[int, int]]]:
    lines = []
    for raw in path.read_text().splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        lines.append(s)

    grid: List[List[Cell]] = []
    lasers: List[Ray] = []
    targets: List[Point] = []
    inv = {"A": 0, "B": 0, "C": 0}

    i = 0
    while i < len(lines):
        tok = lines[i]
        up = tok.upper()
        if up == "GRID START":
            i += 1
            row_buf: List[List[Cell]] = []
            while i < len(lines) and lines[i].upper() != "GRID STOP":
                row = list(lines[i].replace(" ", ""))
                for ch in row:
                    if ch not in {"o", "x", "A", "B", "C"}:
                        raise ValueError(f"Invalid cell '{ch}' in GRID line: {lines[i]}")
                row_buf.append(row)
                i += 1
            if i == len(lines) or lines[i].upper() != "GRID STOP":
                raise ValueError("Missing GRID STOP")
            grid = row_buf
        elif tok[0] in {"A", "B", "C"} and tok[1:].strip():
            parts = tok.split()
            if len(parts) != 2:
                raise ValueError(f"Bad inventory line: {tok}")
            kind, num = parts[0], _tok_int(parts[1])
            if kind not in inv:
                raise ValueError(f"Unknown inventory key: {kind}")
            inv[kind] = num
        elif tok.startswith("L"):
            parts = tok.split()
            if len(parts) != 5:
                raise ValueError(f"Bad laser line: {tok}")
            _, sx, sy, vx, vy = parts
            lasers.append(Ray(_tok_int(sx), _tok_int(sy), 1 if _tok_int(vx) > 0 else -1, 1 if _tok_int(vy) > 0 else -1))
        elif tok.startswith("P"):
            parts = tok.split()
            if len(parts) != 3:
                raise ValueError(f"Bad target line: {tok}")
            _, px, py = parts
            targets.append((_tok_int(px), _tok_int(py)))
        i += 1

    if not grid:
        raise ValueError("GRID not found")

    w = len(grid[0])
    if any(len(r) != w for r in grid):
        raise ValueError("GRID is not rectangular")

    open_slots: List[Tuple[int, int]] = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "o":
                open_slots.append((r, c))

    return Board(grid=grid, lasers=lasers, targets=targets), inv, open_slots

def trace_all_rays(board: Board, step_cap: int = 2000) -> Set[Point]:
    hit: Set[Point] = set()
    rays: List[Ray] = list(board.lasers)
    seen: Set[Tuple[int, int, int, int]] = set()
    xmax, ymax = board.W * 2, board.H * 2

    while rays:
        r = rays.pop()
        x, y, vx, vy = r.x, r.y, (1 if r.vx > 0 else -1), (1 if r.vy > 0 else -1)
        steps = 0

        while 0 <= x <= xmax and 0 <= y <= ymax:
            if steps > step_cap:
                break
            state = (x, y, vx, vy)
            if state in seen:
                break
            seen.add(state)

            nx, ny = x + vx, y + vy
            cur_vx, cur_vy = vx, vy

            if nx % 2 == 0:
                c_edge = nx // 2
                r_mid = (y + ny) // 2
                target_c = c_edge if cur_vx > 0 else c_edge - 1
                target_r = r_mid
                cell = board.cell_at(target_r, target_c)
                if cell == "A":
                    vx = -vx
                elif cell == "B":
                    break
                elif cell == "C":
                    rays.append(Ray(nx, ny, -cur_vx, cur_vy))

            if ny % 2 == 0:
                r_edge = ny // 2
                c_mid = (x + nx) // 2
                target_r = r_edge if cur_vy > 0 else r_edge - 1
                target_c = c_mid
                cell = board.cell_at(target_r, target_c)
                if cell == "A":
                    vy = -vy
                elif cell == "B":
                    break
                elif cell == "C":
                    rays.append(Ray(nx, ny, cur_vx, -cur_vy))

            x, y = nx, ny
            steps += 1
            if (x, y) in board.targets:
                hit.add((x, y))

    return hit

def place_and_solve(base: Board, inventory: Dict[str, int], open_slots: List[Tuple[int, int]], diagnose: bool = False) -> Optional[List[List[Cell]]]:
    targets = set(base.targets)
    grid0 = [row[:] for row in base.grid]

    def with_layout(posA, posB, posC):
        g = [row[:] for row in grid0]
        for r, c in posA: g[r][c] = "A"
        for r, c in posB: g[r][c] = "B"
        for r, c in posC: g[r][c] = "C"
        return g

    best_hit = 0
    best_layout: Optional[List[List[Cell]]] = None
    slots = open_slots
    nA, nB, nC = inventory["A"], inventory["B"], inventory["C"]

    for posA in combinations(slots, nA) if nA <= len(slots) else [()]:
        rem1 = [p for p in slots if p not in posA]
        for posB in combinations(rem1, nB) if nB <= len(rem1) else [()]:
            rem2 = [p for p in rem1 if p not in posB]
            for posC in combinations(rem2, nC) if nC <= len(rem2) else [()]:
                g = with_layout(posA, posB, posC)
                brd = Board(grid=g, lasers=base.lasers, targets=base.targets)
                got = trace_all_rays(brd)
                if len(got) > best_hit:
                    best_hit = len(got)
                    best_layout = g
                if got >= targets:
                    return g

    if diagnose and best_layout is not None:
        print(f"[Diagnosis] Best hit = {best_hit}/{len(targets)}")
    return None

def grid_to_string(grid: List[List[Cell]]) -> str:
    return "\n".join("".join(row) for row in grid)

def write_solution(path: Path, grid: List[List[Cell]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(grid_to_string(grid))

def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Lazor Stage 2 Solver (single file)")
    p.add_argument("-i", "--input", required=True, help=".bff file path")
    p.add_argument("-o", "--output", required=True, help="Where to write solution grid (.txt)")
    p.add_argument("--diagnose", action="store_true", help="Print best partial hit if no solution")
    args = p.parse_args(argv)

    bff = Path(args.input)
    if not bff.exists():
        root = Path(__file__).resolve().parent
        alt = root / args.input
        if alt.exists():
            bff = alt
        else:
            print(f"Input not found: {args.input}", file=sys.stderr)
            return 2

    board, inventory, open_slots = parse_bff(bff)
    print(f"Processing {bff.name}... Inventory: A={inventory['A']}, B={inventory['B']}, C={inventory['C']} | slots={len(open_slots)}")
    solved = place_and_solve(board, inventory, open_slots, diagnose=args.diagnose)
    outp = Path(args.output)

    if solved is None:
        print("No solution found." + (" (See diagnosis above)" if args.diagnose else ""))
        return 1

    write_solution(outp, solved)
    print(f"Solution written to {outp}")
    print(grid_to_string(solved))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
