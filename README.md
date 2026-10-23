# 程序分析图解：语言、运行时与机器行为

![程序结构、运行时与机器行为的视觉隐喻](assets/images/cover.png)

围绕程序行为，贯通语言语义、静态与动态分析、形式化证明、机器执行和工程验证。

从[导读](appendices/reading-guide.md)开始，按以下目录阅读。章节文件与链接保持稳定，阅读顺序由统一清单维护。

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

## 第 5 篇 形式化规格与机器检查证明

- [25　形式化方法的地图与规格细化](chapters/37.md)
- [26　命题、类型与证明助手](chapters/38.md)
- [27　Lean 实作：从定理陈述到内核检查](chapters/39.md)
- [28　证明程序满足规格：归纳、契约与状态转换](chapters/40.md)
- [29　程序等价、精化与编译变换验证](chapters/41.md)
- [30　证明分析器与理解可信计算基础](chapters/42.md)

## 第 6 篇 机器与异构

- [31　CPU、ABI 与机器级程序行为](chapters/25.md)
- [32　内存模型、原子操作与可见性](chapters/26.md)
- [33　逆向、反汇编与反编译](chapters/27.md)
- [34　GPU：SIMT、内存与同步](chapters/28.md)
- [35　性能分析：CPU、GPU 与数据搬运](chapters/29.md)
- [36　跨语言、FFI 与动态机制](chapters/30.md)

## 第 7 篇 数据、内存与资源的深入推理

- [37　形状分析、分离逻辑与内存所有权](chapters/43.md)
- [38　字符串、容器与数据结构分析](chapters/44.md)
- [39　终止性、递归与资源复杂度](chapters/45.md)
- [40　信息流、非干扰与隐私边界](chapters/47.md)
- [41　浮点语义、数值误差与稳定性](chapters/48.md)

## 第 8 篇 分析细化与工程闭环

- [42　反例解释、可行性检查与抽象细化](chapters/46.md)
- [43　分布式、持久化与崩溃恢复](chapters/49.md)
- [44　增量分析、大型工程与摘要失效](chapters/50.md)
- [45　程序合成、自动修复与验证闭环](chapters/51.md)

## 第 9 篇 应用与构建

- [46　缺陷、安全性质与威胁模型](chapters/31.md)
- [47　优化、维护与变更影响分析](chapters/32.md)
- [48　代表工具与分析架构](chapters/33.md)
- [49　AI 辅助分析与证据管理](chapters/34.md)
- [50　评估分析器与实验设计](chapters/35.md)
- [51　搭建一个可运行的教学分析器](chapters/36.md)

## 附录与复现

- [术语速查](appendices/glossary.md)
- [延伸领域地图](appendices/frontiers.md)
- [资料索引](references/source-index.md)
- [扩展版审校记录](references/review-expanded.md)
- [展示编号与稳定身份对照](references/chapter-map.md)
- [教学分析器](examples/README.md)
- [Lean 证明文件与检查说明](examples/lean/README.md)

```bash
python3 scripts/check_book.py
python3 -m unittest discover -s examples -p "test*.py"
python3 scripts/build_book.py
```

构建与内容检查仅需 Python 3.10+ 标准库；可选图像预览使用 Pillow 与 Inkscape，或 Pillow 与 PyMuPDF。Lean 文件另按所附说明使用固定版本检查，不是普通书稿构建的必装依赖。

构建输出合并 Markdown 和完整工程包，资源保留相对路径。工程包内的 build/history.bundle 可用 `git clone build/history.bundle restored-book` 恢复完整已提交历史；直接阅读无需恢复 Git。

本次交付为 Markdown、SVG/封面与可运行示例；网页和 PDF 可复用相同主稿另行发布。
