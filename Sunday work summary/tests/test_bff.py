#!/usr/bin/env python3
"""简单测试单个 bff 文件"""
import sys
sys.path.insert(0, '.')

from lazor_core import parse_bff, Board

# 测试 tiny_5.bff
filepath = "/Users/tommyboy/Downloads/bff_files/tiny_5.bff"

print("正在解析文件...")
spec = parse_bff(filepath)
board = Board.from_bffspec(spec)

print("解析成功！")
print(board.summary())

