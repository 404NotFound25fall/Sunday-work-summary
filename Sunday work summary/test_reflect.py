exec(open('lazor_solver.py').read().split('if __name__')[0])

print("TEST: A block reflection")
grid = [['A']]
lasers = [Ray(x=0, y=0, vx=1, vy=1)]
board = Board(grid=grid, lasers=lasers, targets=[])
hit = trace_all_rays(board)
print(f"Result: {sorted(hit)}")
print(f"Expected: Should see reflected laser path")
print()
