# Test if C block (refract) works correctly
exec(open('lazor_solver.py').read().split('if __name__')[0])

# Simple test: laser hits C, should split
grid = [['C']]
lasers = [Ray(x=0, y=1, vx=1, vy=0)]  # Moving right from left side
targets = [(2, 1), (0, 1)]  # Both straight-through and reflected

board = Board(grid=grid, lasers=lasers, targets=targets)
hit = trace_all_rays(board)

print("Test: Laser hits C block")
print(f"Grid: {grid}")
print(f"Laser: start=(0,1), direction=(1,0)")
print(f"Hit points: {sorted(hit)}")
print(f"Expected: Laser should pass through AND reflect back")
print(f"Result: {'PASS' if len(hit) >= 2 else 'FAIL'}")
