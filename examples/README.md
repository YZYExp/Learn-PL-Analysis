# 教学分析器

Python 3.10+，仅使用标准库。在项目根目录运行：

```bash
python3 examples/analyzer.py examples/refund.json
python3 -m unittest discover -s examples -v
```

输入为显式控制流 JSON IR，节点见 `refund.json`。整数无限精度；`div` 使用 Python `//` 的向负无穷取整，不同于C有符号整数除法向零截断。变量入口均可为任意整数；本工具不检查未初始化读取。`input` 覆盖为未知整数。`branch` 保留两条边且不精化条件。`assert_nonzero` 是观测点，不裁剪后继。`stop` 无后继。不可达环境为 `null`，未知值为 `"?"`；两者不可混淆。

支持 const/input/copy/add/sub/mul/div/branch/goto/assert_nonzero/stop。异常、函数、堆、字符串、并发及真实语言前端均不支持；遇到未知指令拒绝分析。零分母后仍传播未知结果，是保守继续，不是具体执行语义。报告均为候选；抽象图上的可达性不等于存在可行具体路径。

实现用于观察常量传播与工作列表，不是生产级安全扫描器。测试覆盖汇合、循环收敛、不可达、常量分母、拒绝非法IR及刻意不做分支裁剪的行为。

## 更多实作

- [崩溃恢复、摘要失效与有限合成实验](EXTENSION.md)
- [Lean证明文件与复查命令](lean/README.md)
