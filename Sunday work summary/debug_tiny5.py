from pathlib import Path
import sys

# Parse tiny_5
exec(open('lazor_solver.py').read().split('if __name__')[0])

bff = Path('examples/official/tiny_5.bff')
board, inventory, open_slots = parse_bff(bff)

print("=" * 60)
print("BOARD INFO:")
print(f"Grid dimensions: {board.H}x{board.W}")
print(f"Grid content:")
for r in range(board.H):
    print(f"  Row {r}: {board.grid[r]}")

print(f"\nOpen slots ({len(open_slots)}): {open_slots}")
print(f"Inventory: {inventory}")

print("\n" + "=" * 60)
print("LASER INFO:")
for i, laser in enumerate(board.lasers):
    print(f"Laser {i}: start=({laser.x}, {laser.y}), direction=({laser.vx}, {laser.vy})")

print("\nTarget points:")
for target in board.targets:
    print(f"  {target}")

print("\n" + "=" * 60)
print("TEST: Trace with original board (fixed B only)")
hit = trace_all_rays(board)
print(f"Hit points: {sorted(hit)}")
print(f"Targets: {sorted(board.targets)}")
print(f"Match: {hit >= set(board.targets)}")

print("\n" + "=" * 60)
print("TEST: Manual placement - let's try the solution from test_no_fixed")
# test_no_fixed solution was: AAB / Coo / ooA
# That's: A at (0,0), A at (0,1), B at (0,2), C at (1,0), A at (2,2)

test_grid = [row[:] for row in board.grid]
# For tiny_5 with fixed B at (0,1), we can't place anything there
# Let's try: A at (0,0), A at (0,2), A at (1,0), C at (1,1)
test_grid[0][0] = 'A'
test_grid[0][2] = 'A'
test_grid[1][0] = 'A'
test_grid[1][1] = 'C'

test_board = Board(grid=test_grid, lasers=board.lasers, targets=board.targets)
print("Test configuration:")
for r in range(test_board.H):
    print(f"  {' '.join(test_grid[r])}")

hit = trace_all_rays(test_board)
print(f"\nHit points: {sorted(hit)}")
print(f"Targets: {sorted(board.targets)}")
print(f"Match: {hit >= set(board.targets)}")
