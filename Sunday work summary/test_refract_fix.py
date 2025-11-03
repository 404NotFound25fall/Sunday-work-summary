exec(open('lazor_solver.py').read().split('if __name__')[0])

# Test with laser starting at even coordinate (boundary)
grid = [['C']]
lasers = [Ray(x=0, y=0, vx=1, vy=1)]  # Start at corner, move diagonally
targets = [(2, 2), (0, 2)]

board = Board(grid=grid, lasers=lasers, targets=targets)
hit = trace_all_rays(board)

print("Test: Laser from boundary hitting C block")
print(f"Laser: start=(0,0), direction=(1,1)")
print(f"Hit points: {sorted(hit)}")
print(f"Expected: Should see splits from C")
print(f"Result: {'PASS' if len(hit) >= 2 else 'FAIL'}")
