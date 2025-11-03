exec(open('lazor_solver.py').read().split('if __name__')[0])
from pathlib import Path
from itertools import combinations

bff = Path('examples/official/tiny_5.bff')
board, inventory, open_slots = parse_bff(bff)

print(f"Testing tiny_5: {len(open_slots)} slots")

best = 0
count = 0

for pos in combinations(open_slots, 4):
    for c_idx in range(4):
        grid = [row[:] for row in board.grid]
        for i, p in enumerate(pos):
            grid[p[0]][p[1]] = 'C' if i == c_idx else 'A'
        
        b = Board(grid=grid, lasers=board.lasers, targets=board.targets)
        hit = trace_all_rays(b)
        count += 1
        
        if len(hit) > best:
            best = len(hit)
            print(f"Config {count}: hits {best}/2")
            for r in grid:
                print(f"  {''.join(r)}")
            
            if best >= 2:
                print("FOUND!")
                break
    if best >= 2:
        break

print(f"\nTested {count}, best: {best}/2")
