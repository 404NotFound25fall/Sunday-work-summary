# BFF 文件测试指南

## 文件位置
BFF 测试文件位于：`/Users/tommyboy/Downloads/bff_files/`

## 可用的 BFF 文件
- `tiny_5.bff` - 简单测试
- `mad_1.bff` - 普通测试 1
- `mad_4.bff` - 普通测试 4
- `yarn_5.bff` - 中等测试
- `showstopper_4.bff` - 挑战测试
- `dark_1.bff` - 困难测试
- `numbered_6.bff` - 复杂测试
- `mad_7.bff` - 高级测试

## 运行方式

### 1. 单个文件测试
```bash
python lazor_solver.py /Users/tommyboy/Downloads/bff_files/tiny_5.bff
```

### 2. 批量测试
```bash
python run_bff_tests.py
```

### 3. 使用解析演示
```bash
python parse_bff_demo.py /Users/tommyboy/Downloads/bff_files/tiny_5.bff
```

## 当前已知问题
1. 坐标系统需要进一步验证
2. 激光模拟可能需要优化
3. 求解器性能需要测试

## 下一步
1. 先运行 `tiny_5.bff`（最简单）
2. 验证输出结果
3. 逐步测试更复杂的文件

