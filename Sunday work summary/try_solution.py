exec(open('lazor_solver.py').read().split('if __name__')[0])

from pathlib import Path
bff = Path('examples/official/tiny_5.bff')
board, inventory, open_slots = parse_bff(bff)

print("Trying to find where to place A to redirect laser to (6,3)")
print()

# The laser path is: (4,5) → (3,4) → (2,3) → (1,2) → (0,1) → out
# We need to place A somewhere to redirect it RIGHT

# Try placing A at (0, 0) - this is where laser crosses at step 2
test_configs = [
    # Format: list of (row, col, type)
    [(0, 0, 'A'), (0, 2, 'A'), (1, 1, 'A'), (1, 2, 'C')],  # A at top-left
    [(0, 0, 'A'), (0, 2, 'A'), (2, 0, 'A'), (2, 1, 'C')],  # Different layout
    [(0, 0, 'C'), (0, 2, 'A'), (1, 0, 'A'), (2, 2, 'A')],  # C at top-left
    [(1, 1, 'A'), (1, 2, 'A'), (2, 1, 'A'), (2, 2, 'C')],  # Lower placement
]

for i, config in enumerate(test_configs):
    print(f"\nTest {i+1}:")
    test_grid = [row[:] for row in board.grid]
    for r, c, typ in config:
        test_grid[r][c] = typ
    
    for row in test_grid:
        print(f"  {' '.join(row)}")
    
    test_board = Board(grid=test_grid, lasers=board.lasers, targets=board.targets)
    hit = trace_all_rays(test_board)
    
    print(f"  Hit: {sorted(hit)}")
    print(f"  Targets: {sorted(board.targets)}")
    
    if len(hit) >= 2 and set(board.targets).issubset(hit):
        print("  ✅ SOLUTION FOUND!")
        break
    else:
        print(f"  ❌ Hit {len(hit)}/2 targets")
