#!/usr/bin/env python3
"""使用外部提供的文件测试"""
import sys
from pathlib import Path
from lazor_core import parse_bff, Board, solve_optimized

# 测试 tiny_5.bff
filepath = Path("/Users/tommyboy/Downloads/bff_files/tiny_5.bff")

print(f"=== 测试 {filepath.name} ===")

if filepath.exists():
    spec = parse_bff(str(filepath))
    board = Board.from_bffspec(spec)
    
    print(board.summary())
    
    print("\n尝试求解...")
    solved = solve_optimized(board)
    
    if solved:
        print("✓ 找到解！")
    else:
        print("✗ 未找到解")
else:
    print(f"文件不存在: {filepath}")

