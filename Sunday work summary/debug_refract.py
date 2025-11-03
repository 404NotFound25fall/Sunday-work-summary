exec(open('lazor_solver.py').read().split('if __name__')[0])

# Detailed trace for C block
grid = [['C']]
lasers = [Ray(x=0, y=1, vx=1, vy=0)]
board = Board(grid=grid, lasers=lasers, targets=[])

print("=" * 60)
print("DEBUGGING C BLOCK (REFRACT)")
print("=" * 60)
print(f"Grid: {grid}")
print(f"Laser: x=0, y=1, vx=1, vy=0 (moving RIGHT)")
print()

# Manually trace
x, y, vx, vy = 0, 1, 1, 0
print(f"Step 0: Position ({x}, {y}), direction ({vx}, {vy})")

# Next position
nx, ny = x + vx, y + vy
print(f"Step 1: Moving to ({nx}, {ny})")

# Check what edge we're crossing
crossed_vertical = (nx % 2 == 0)
crossed_horizontal = (ny % 2 == 0)
print(f"  Crossed vertical: {crossed_vertical} (nx={nx})")
print(f"  Crossed horizontal: {crossed_horizontal} (ny={ny})")

if crossed_vertical:
    c_edge = nx // 2
    r_idx = min(y, ny) // 2
    t_col = c_edge if vx > 0 else c_edge - 1
    t_row = r_idx
    print(f"  Checking cell at row={t_row}, col={t_col}")
    if 0 <= t_row < len(grid) and 0 <= t_col < len(grid[0]):
        cell = grid[t_row][t_col]
        print(f"  Cell value: '{cell}'")
        if cell == 'C':
            print(f"  → Should create reflected ray at ({nx}, {ny}) with direction ({-vx}, {vy})")
    else:
        print(f"  Cell out of bounds!")

print()
print("Now running actual trace_all_rays:")
hit = trace_all_rays(board)
print(f"Hit points: {sorted(hit)}")
