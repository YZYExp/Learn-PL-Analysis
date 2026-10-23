# 程序分析图解：语言、运行时与机器行为

![程序分析：从语言结构到运行时与机器行为的视觉隐喻](assets/images/cover.png)

以程序行为为主线的中文图解入门书。覆盖语言语义、程序表示、静态推理、动态分析、验证、CPU/GPU、逆向、AI 辅助分析与评估。

先读 [导读](appendices/reading-guide.md)，再按目录阅读。范围边界与写作计划见 [PLAN.md](PLAN.md)。

## 第 1 篇 语言与行为

- [01　程序分析的地图与边界](chapters/01.md)
- [02　程序语义：状态、求值与可观察行为](chapters/02.md)
- [03　语言设计：类型、效果与所有权](chapters/03.md)
- [04　分析对象：数值、对象、资源与协议](chapters/04.md)
- [05　运行时：解释器、虚拟机、GC 与 JIT](chapters/05.md)
- [06　正确性、规格与分析的可信边界](chapters/06.md)

## 第 2 篇 程序表示

- [07　从源码到 AST 与符号表](chapters/07.md)
- [08　中间表示、SSA 与编译过程](chapters/08.md)
- [09　控制流、支配关系与循环](chapters/09.md)
- [10　调用图、动态分派与跨函数边界](chapters/10.md)
- [11　依赖图与程序切片](chapters/11.md)
- [12　指针、别名、堆与对象模型](chapters/12.md)

## 第 3 篇 静态推理

- [13　数据流分析与工作列表](chapters/13.md)
- [14　格、不动点与抽象解释](chapters/14.md)
- [15　数值抽象、关系与路径敏感性](chapters/15.md)
- [16　跨函数摘要与上下文敏感性](chapters/16.md)
- [17　类型状态、资源与污点分析](chapters/17.md)
- [18　规则、Datalog 与查询式分析](chapters/18.md)

## 第 4 篇 动态与验证

- [19　插桩、轨迹与覆盖率](chapters/19.md)
- [20　动态检测、Sanitizer 与运行时验证](chapters/20.md)
- [21　符号执行、SMT 与路径爆炸](chapters/21.md)
- [22　模糊测试、Concolic 与混合分析](chapters/22.md)
- [23　并发、异步与记录重放](chapters/23.md)
- [24　模型检查、契约与演绎验证](chapters/24.md)

## 第 5 篇 机器与异构

- [25　CPU、ABI 与机器级程序行为](chapters/25.md)
- [26　内存模型、原子操作与可见性](chapters/26.md)
- [27　逆向、反汇编与反编译](chapters/27.md)
- [28　GPU：SIMT、内存与同步](chapters/28.md)
- [29　性能分析：CPU、GPU 与数据搬运](chapters/29.md)
- [30　跨语言、FFI 与动态机制](chapters/30.md)

## 第 6 篇 应用与构建

- [31　缺陷、安全性质与威胁模型](chapters/31.md)
- [32　优化、维护与变更影响分析](chapters/32.md)
- [33　代表工具与分析架构](chapters/33.md)
- [34　AI 辅助分析与证据管理](chapters/34.md)
- [35　评估分析器与实验设计](chapters/35.md)
- [36　搭建一个可运行的教学分析器](chapters/36.md)

## 附录与复现

- [术语速查](appendices/glossary.md)
- [资料索引](references/source-index.md)
- [审校记录](references/review.md)
- [教学分析器](examples/)

```bash
python3 scripts/check_book.py
python3 -m unittest discover -s examples -p "test*.py"
python3 scripts/build_book.py
```

构建只使用 Python 标准库，生成合并 Markdown 和完整工程包。图片采用可编辑 SVG；章节可以独立阅读。工具文档链接用于继续学习，在线内容可能更新。

工程包内包含 Git 历史 bundle，可用 `git clone build/history.bundle restored-book` 恢复已提交的版本历史。解压工程包直接阅读，无需恢复 Git。网页与 PDF 导出留待需要时配置，使用同一套正文与资源。
