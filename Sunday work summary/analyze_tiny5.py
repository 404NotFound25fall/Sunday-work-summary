exec(open('lazor_solver.py').read().split('if __name__')[0])

from pathlib import Path
bff = Path('examples/official/tiny_5.bff')
board, inventory, open_slots = parse_bff(bff)

print("=" * 60)
print("TINY_5 ANALYSIS")
print("=" * 60)
print(f"Grid: {board.H}x{board.W}")
for r in range(board.H):
    print(f"  {' '.join(board.grid[r])}")

print(f"\nLaser: start=({board.lasers[0].x}, {board.lasers[0].y}), dir=({board.lasers[0].vx}, {board.lasers[0].vy})")
print(f"Targets: {sorted(board.targets)}")

print("\n" + "=" * 60)
print("MANUAL TRACE:")
print("=" * 60)

x, y = 4, 5
vx, vy = -1, -1

for step in range(10):
    print(f"\nStep {step}: at ({x}, {y}), direction ({vx}, {vy})")
    
    nx, ny = x + vx, y + vy
    print(f"  Moving to ({nx}, {ny})")
    
    if nx < 0 or ny < 0 or nx > board.W * 2 or ny > board.H * 2:
        print(f"  Out of bounds, stopping")
        break
    
    # Check crossings
    crossed_v = (nx % 2 == 0)
    crossed_h = (ny % 2 == 0)
    
    if crossed_v:
        c_edge = nx // 2
        r_idx = min(y, ny) // 2
        t_col = c_edge if vx > 0 else c_edge - 1
        t_row = r_idx
        print(f"  Crossed vertical at x={nx}: checking cell ({t_row}, {t_col})")
        cell = board.cell_at(t_row, t_col) if board.cell_at(t_row, t_col) else 'out'
        print(f"    Cell: '{cell}'")
        if cell == 'B':
            print(f"    HIT B - STOP")
            break
        elif cell == 'A':
            print(f"    HIT A - REFLECT VERTICAL")
            vx = -vx
    
    if crossed_h:
        r_edge = ny // 2
        c_idx = min(x, nx) // 2
        t_row = r_edge if vy > 0 else r_edge - 1
        t_col = c_idx
        print(f"  Crossed horizontal at y={ny}: checking cell ({t_row}, {t_col})")
        cell = board.cell_at(t_row, t_col) if board.cell_at(t_row, t_col) else 'out'
        print(f"    Cell: '{cell}'")
        if cell == 'B':
            print(f"    HIT B - STOP")
            break
        elif cell == 'A':
            print(f"    HIT A - REFLECT HORIZONTAL")
            vy = -vy
    
    x, y = nx, ny
    
    if (x, y) in board.targets:
        print(f"  *** TARGET HIT: ({x}, {y}) ***")

print("\n" + "=" * 60)
