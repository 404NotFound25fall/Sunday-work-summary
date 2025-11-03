# 如何运行测试

## 🎯 已创建的文件

### 测试脚本
1. `simple_run.py` - 最简单的测试
2. `test_with_output.py` - 详细输出测试
3. `run_bff_tests.py` - 批量测试

### 测试数据
- `mini_test.bff` - 本地测试文件
- `test_reflect.bff` - 反射测试
- `test_opaque.bff` - 遮挡测试
- `test_refract.bff` - 分束测试

### 外部测试数据
在 `/Users/tommyboy/Downloads/bff_files/` 目录下：
- `tiny_5.bff` - 简单测试 ⭐ 推荐先测试这个
- `mad_1.bff` - 普通测试
- 其他难度递增的测试文件

## 🚀 运行方式

### 方法1：在编辑器运行
1. 打开 `lazor_solver.py`
2. 设置参数为 `mini_test.bff`
3. 运行并查看输出

### 方法2：终端运行
```bash
cd "lazor_stage2_vscode_bundle (1)"
python lazor_solver.py mini_test.bff
```

### 方法3：使用测试脚本
```bash
python simple_run.py
```

### 方法4：详细输出测试
```bash
python test_with_output.py
```

## 📝 预期输出示例

```
正在解析文件: mini_test.bff
解析成功！
Board 4x4
Grid:
o o o o
o x o o
o A o o
o o o C
Free blocks: REFLECT:1, OPAQUE:0, REFRACT:1
Lasers: L(2,7,1,-1)
Points: P(3,0); P(4,3)

开始求解...
✓ 找到解！ (耗时: 0.XX秒)
```

## ⚠️ 注意事项

1. 如果终端没有输出，可能在运行但卡住了
2. 求解器可能需要时间（特别是复杂的情况）
3. 检查是否有错误信息
4. 确保 Python 版本正确（建议 Python 3.8+）

## 🔍 查看结果

- 控制台输出：查看 `print` 语句
- 解文件：如果成功会生成 `.sol` 文件
- 错误信息：查看异常堆栈跟踪

## 💡 建议顺序

1. 先运行 `simple_run.py` 确保基础解析工作
2. 然后测试 `mini_test.bff`
3. 再尝试 `tiny_5.bff`（复制到本地目录）
4. 最后测试更复杂的文件

---

如遇到问题，请查看 STATUS.md 了解当前状态

