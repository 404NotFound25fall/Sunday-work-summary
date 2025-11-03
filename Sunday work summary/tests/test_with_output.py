#!/usr/bin/env python3
"""
测试脚本 - 显示详细输出
"""
import sys
import traceback
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_file(bff_path, description):
    """测试一个 bff 文件"""
    print(f"\n{'='*70}")
    print(f"测试: {description}")
    print(f"文件: {bff_path}")
    print('='*70)
    
    try:
        from lazor_core import parse_bff, Board, solve_optimized, simulate_board
        
        # 解析
        print("\n[1] 解析文件...")
        spec = parse_bff(bff_path)
        board = Board.from_bffspec(spec)
        print("✓ 解析成功")
        
        # 显示信息
        print(f"  棋盘大小: {board.nrows}x{board.ncols}")
        print(f"  可放置方块: A={board.free_blocks.get('REFLECT', 0)}, B={board.free_blocks.get('OPAQUE', 0)}, C={board.free_blocks.get('REFRACT', 0)}")
        print(f"  激光数量: {len(board.lasers)}")
        for i, laser in enumerate(board.lasers):
            print(f"    激光{i+1}: ({laser.x}, {laser.y}), 方向 ({laser.vx}, {laser.vy})")
        print(f"  目标点: {sorted(board.points)}")
        
        # 求解
        print("\n[2] 开始求解...")
        import time
        start_time = time.time()
        solved = solve_optimized(board)
        elapsed = time.time() - start_time
        
        if solved:
            print(f"✓ 找到解！ (耗时: {elapsed:.2f}秒)")
            
            # 验证
            print("\n[3] 验证解...")
            hit_points = simulate_board(solved)
            expected = board.points
            match = hit_points == expected
            
            print(f"  目标点: {sorted(expected)}")
            print(f"  击中点: {sorted(hit_points)}")
            print(f"  匹配: {'✓' if match else '✗'}")
            
            if match:
                print("\n✓✓✓ 完全匹配！解正确！")
                return True
            else:
                print("\n✗ 解不匹配，可能有bug")
                return False
        else:
            print(f"✗ 未找到解 (耗时: {elapsed:.2f}秒)")
            return False
            
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        traceback.print_exc()
        return False

def main():
    print("Lazor 求解器测试")
    
    # 测试本地文件
    tests = [
        ("mini_test.bff", "本地测试 - mini_test"),
        ("test_reflect.bff", "反射测试"),
        ("test_opaque.bff", "遮挡测试"),
        ("test_refract.bff", "分束测试"),
    ]
    
    # 测试外部文件
    external_dir = Path("/Users/tommyboy/Downloads/bff_files")
    if external_dir.exists():
        tests.extend([
            (str(external_dir / "tiny_5.bff"), "外部 - tiny_5"),
            (str(external_dir / "mad_1.bff"), "外部 - mad_1"),
        ])
    
    results = []
    for bff_path, desc in tests:
        bff_file = Path(bff_path)
        if bff_file.exists():
            success = test_file(str(bff_file), desc)
            results.append((desc, success))
        else:
            print(f"\n跳过: {bff_path} (不存在)")
    
    # 汇总
    print(f"\n{'='*70}")
    print("测试汇总")
    print('='*70)
    success_count = sum(1 for _, s in results if s)
    for desc, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{status}: {desc}")
    print(f"\n总计: {success_count}/{len(results)} 通过")

if __name__ == "__main__":
    main()

