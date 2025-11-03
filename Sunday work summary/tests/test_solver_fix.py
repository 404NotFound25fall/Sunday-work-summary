#!/usr/bin/env python3
"""测试求解器是否能找到解"""
import sys
from lazor_core import parse_bff, Board, solve_optimized, simulate_board

# 测试 simple.bff
print("=== 测试 simple.bff ===")
spec = parse_bff("simple.bff")
board = Board.from_bffspec(spec)

print(board.summary())

# 测试模拟器
hit_points = simulate_board(board)
print(f"\n击中点: {sorted(hit_points)}")
print(f"期望点: {sorted(board.points)}")

# 尝试求解
print("\n尝试求解...")
solved = solve_optimized(board)

if solved:
    print("✓ 找到解！")
    hit = simulate_board(solved)
    print(f"解击中点: {sorted(hit)}")
else:
    print("✗ 未找到解")

