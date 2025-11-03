#!/usr/bin/env python3
"""测试修复后的坐标系统"""
from lazor_core import parse_bff, Board, simulate_board

print("=== 测试 mini_test.bff ===")
spec = parse_bff("mini_test.bff")
board = Board.from_bffspec(spec)

print("激光:", board.lasers[0])
print("目标点:", sorted(board.points))

# 测试模拟器
hit_points = simulate_board(board)
print(f"\n击中的点: {sorted(hit_points)}")
print(f"期望的点: {sorted(board.points)}")
print(f"匹配: {hit_points == board.points}")

# 显示网格中的方块
print("\n网格中的方块:")
for (r, c), block in board.fixed_blocks.items():
    print(f"  网格 ({r}, {c}) 有 {block.kind.value}")

# 手动计算 half-block 坐标
print("\n方块的 half-block 坐标:")
for (r, c), block in board.fixed_blocks.items():
    hb_x = 2 * c + 1
    hb_y = 2 * r + 1
    print(f"  网格 ({r}, {c}) → half-block ({hb_x}, {hb_y})")

