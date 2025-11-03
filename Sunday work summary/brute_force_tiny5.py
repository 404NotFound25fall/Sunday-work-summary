exec(open('lazor_solver.py').read().split('if __name__')[0])

from pathlib import Path
from itertools import combinations

bff = Path('examples/official/tiny_5.bff')
board, inventory, open_slots = parse_bff(bff)

print(f"Exhaustive search: {len(open_slots)} slots, need 3A + 1C")

best_hit = 0
tested = 0

for positions in combinations(open_slots, 4):
    for c_idx in range(4):
        test_grid = [row[:] for row in board.grid]
        for i, pos in enumerate(positions):
            test_grid[pos[0]][pos[1]] = 'C' if i == c_idx else 'A'
        
        test_board = Board(grid=test_grid, lasers=board.lasers, targets=board.targets)
        hit = trace_all_rays(test_board)
        tested += 1
        
        if len(hit) > best_hit:
            best_hit = len(hit)
            print(f"Best so far: {len(hit)}/2 targets (tested {tested})")
            for row in test_grid:
                print(f"  {' '.join(row)}")
            
            if len(hit) == 2:
                print("\n🎉 FOUND!")
                break
    if best_hit == 2:
        break

print(f"\nTested {tested} configs. Best: {best_hit}/2")
if best_hit < 2:
    print("❌ NO SOLUTION EXISTS")
