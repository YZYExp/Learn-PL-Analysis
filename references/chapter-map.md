# 展示编号与稳定身份对照

阅读顺序以 `book.json` 的 `number` 为准。本版共55章，形式化篇为展示25—34章；稳定ID、文件名和URL保留身份，新增Rocq专题的稳定ID为52—55。旧审稿报告中的数字按报告注明的版本或稳定ID解释，不直接当作本版展示章号。

| 展示章号 | 稳定ID | 源文件 | 章节 |
|---|---|---|---|
| 01 | ch01 | [chapters/01.md](../chapters/01.md) | 程序分析的地图与边界 |
| 02 | ch02 | [chapters/02.md](../chapters/02.md) | 程序语义：状态、求值与可观察行为 |
| 03 | ch03 | [chapters/03.md](../chapters/03.md) | 语言设计：类型、效果与所有权 |
| 04 | ch04 | [chapters/04.md](../chapters/04.md) | 分析对象：数值、对象、资源与协议 |
| 05 | ch05 | [chapters/05.md](../chapters/05.md) | 运行时：解释器、虚拟机、GC 与 JIT |
| 06 | ch06 | [chapters/06.md](../chapters/06.md) | 正确性、规格与分析的可信边界 |
| 07 | ch07 | [chapters/07.md](../chapters/07.md) | 从源码到 AST 与符号表 |
| 08 | ch08 | [chapters/08.md](../chapters/08.md) | 中间表示、SSA 与编译过程 |
| 09 | ch09 | [chapters/09.md](../chapters/09.md) | 控制流、支配关系与循环 |
| 10 | ch10 | [chapters/10.md](../chapters/10.md) | 调用图、动态分派与跨函数边界 |
| 11 | ch11 | [chapters/11.md](../chapters/11.md) | 依赖图与程序切片 |
| 12 | ch12 | [chapters/12.md](../chapters/12.md) | 指针、别名、堆与对象模型 |
| 13 | ch13 | [chapters/13.md](../chapters/13.md) | 数据流分析与工作列表 |
| 14 | ch14 | [chapters/14.md](../chapters/14.md) | 格、不动点与抽象解释 |
| 15 | ch15 | [chapters/15.md](../chapters/15.md) | 数值抽象、关系与路径敏感性 |
| 16 | ch16 | [chapters/16.md](../chapters/16.md) | 跨函数摘要与上下文敏感性 |
| 17 | ch17 | [chapters/17.md](../chapters/17.md) | 类型状态、资源与污点分析 |
| 18 | ch18 | [chapters/18.md](../chapters/18.md) | 规则、Datalog 与查询式分析 |
| 19 | ch19 | [chapters/19.md](../chapters/19.md) | 插桩、轨迹与覆盖率 |
| 20 | ch20 | [chapters/20.md](../chapters/20.md) | 动态检测、Sanitizer 与运行时验证 |
| 21 | ch21 | [chapters/21.md](../chapters/21.md) | 符号执行、SMT 与路径爆炸 |
| 22 | ch22 | [chapters/22.md](../chapters/22.md) | 模糊测试、Concolic 与混合分析 |
| 23 | ch23 | [chapters/23.md](../chapters/23.md) | 并发、异步与记录重放 |
| 24 | ch24 | [chapters/24.md](../chapters/24.md) | 模型检查、契约与演绎验证 |
| 25 | ch37 | [chapters/37.md](../chapters/37.md) | 形式化方法的地图与规格细化 |
| 26 | ch38 | [chapters/38.md](../chapters/38.md) | 命题、类型与证明助手 |
| 27 | ch39 | [chapters/39.md](../chapters/39.md) | Lean 实作：从定理陈述到内核检查 |
| 28 | ch52 | [chapters/52.md](../chapters/52.md) | Rocq 实作：定义、归纳与内核检查 |
| 29 | ch53 | [chapters/53.md](../chapters/53.md) | Lean 与 Rocq 同题对照：证据、目标与自动化 |
| 30 | ch40 | [chapters/40.md](../chapters/40.md) | 证明程序满足规格：归纳、契约与状态转换 |
| 31 | ch41 | [chapters/41.md](../chapters/41.md) | 程序等价、精化与编译变换验证 |
| 32 | ch54 | [chapters/54.md](../chapters/54.md) | CompCert 案例：程序语义、模拟与编译正确性 |
| 33 | ch55 | [chapters/55.md](../chapters/55.md) | VST 案例：C 程序、内存资源与验证责任 |
| 34 | ch42 | [chapters/42.md](../chapters/42.md) | 证明分析器与理解可信计算基础 |
| 35 | ch25 | [chapters/25.md](../chapters/25.md) | CPU、ABI 与机器级程序行为 |
| 36 | ch26 | [chapters/26.md](../chapters/26.md) | 内存模型、原子操作与可见性 |
| 37 | ch27 | [chapters/27.md](../chapters/27.md) | 逆向、反汇编与反编译 |
| 38 | ch28 | [chapters/28.md](../chapters/28.md) | GPU：SIMT、内存与同步 |
| 39 | ch29 | [chapters/29.md](../chapters/29.md) | 性能分析：CPU、GPU 与数据搬运 |
| 40 | ch30 | [chapters/30.md](../chapters/30.md) | 跨语言、FFI 与动态机制 |
| 41 | ch43 | [chapters/43.md](../chapters/43.md) | 形状分析、分离逻辑与内存所有权 |
| 42 | ch44 | [chapters/44.md](../chapters/44.md) | 字符串、容器与数据结构分析 |
| 43 | ch45 | [chapters/45.md](../chapters/45.md) | 终止性、递归与资源复杂度 |
| 44 | ch47 | [chapters/47.md](../chapters/47.md) | 信息流、非干扰与隐私边界 |
| 45 | ch48 | [chapters/48.md](../chapters/48.md) | 浮点语义、数值误差与稳定性 |
| 46 | ch46 | [chapters/46.md](../chapters/46.md) | 反例解释、可行性检查与抽象细化 |
| 47 | ch49 | [chapters/49.md](../chapters/49.md) | 分布式、持久化与崩溃恢复 |
| 48 | ch50 | [chapters/50.md](../chapters/50.md) | 增量分析、大型工程与摘要失效 |
| 49 | ch51 | [chapters/51.md](../chapters/51.md) | 程序合成、自动修复与验证闭环 |
| 50 | ch31 | [chapters/31.md](../chapters/31.md) | 缺陷、安全性质与威胁模型 |
| 51 | ch32 | [chapters/32.md](../chapters/32.md) | 优化、维护与变更影响分析 |
| 52 | ch33 | [chapters/33.md](../chapters/33.md) | 代表工具与分析架构 |
| 53 | ch34 | [chapters/34.md](../chapters/34.md) | AI 辅助分析与证据管理 |
| 54 | ch35 | [chapters/35.md](../chapters/35.md) | 评估分析器与实验设计 |
| 55 | ch36 | [chapters/36.md](../chapters/36.md) | 搭建一个可运行的教学分析器 |
