# Rocq扩展版审校与验证记录

本版在51章扩展版上增加四章，统一为55章、九篇。源文件稳定ID保留，显示编号依据book.json；完整对照见[章节身份表](chapter-map.md)。本记录对应2026-10-23的整合检查。

| 显示章号 | 稳定ID／源码 | 本次新增内容 |
|---:|---|---|
| 28 | [52.md](../chapters/52.md) | Gallina定义、归纳、证明状态与内核检查 |
| 29 | [53.md](../chapters/53.md) | 与Lean对同一列表计数性质逐层比较 |
| 32 | [54.md](../chapters/54.md) | CompCert模拟、语义保持与工具链边界 |
| 33 | [55.md](../chapters/55.md) | VST规格、Clight、数组循环与分离资源 |

## 内容和图文

- 四章由三组并行编写，循环交叉审查；报告见[基础与VST审查](review-rocq-foundations.md)、[Rocq与Lean对照审查](review-rocq-compiler.md)、[CompCert与内存模型审查](review-rocq-memory.md)。
- 新增10张760×900纵向SVG。正文共98张教学图，另有全书地图和封面；99份SVG结构检查通过。新图与更新地图共11张均经Inkscape实际渲染，并查看两张总览联系表，没有文字遮挡或裁切。
- 更新55章标题、图号、小节号和数字跨章引用；稳定源文件名与链接不变。补充Lean→Rocq、等价→CompCert、形状→VST与可信边界→真实案例的衔接。
- 目录、五条阅读路线、术语与来源索引按新清单整合。旧02章残留的CPU/内存数字引用改为稳定标题链接。历史报告保留当时语境。
- 案例就近引用Rocq官方手册、CompCert Compiler/Smallstep/Behaviors/Clight、Software Foundations与VST实际源码。版本与定理边界以对应引用为准，不从教学模型推导额外工程保证。

## 实际检查

Rocq固定版本是本书复现目标，不声称为最新版本。实际安装的rocq-prover、rocq-core、rocq-runtime、rocq-stdlib均为9.0.0，OCaml为4.14.1；[安装清单](../examples/rocq/installation.json)及其摘要与[检查报告](../examples/rocq/check-results.json)关联。

| 检查对象 | 实际操作 | 结果 |
|---|---|---|
| Foundations.v | 编译、5次Print Assumptions、独立rocq check | 通过，5份全局假设查询闭合 |
| CompilerModel.v | 编译、5次Print Assumptions、独立rocq check | 通过，5份全局假设查询闭合 |
| HeapModel.v | 编译、6次Print Assumptions、独立rocq check | 通过，6份全局假设查询闭合 |
| 教学分析器与工程实验 | unittest发现并执行16项测试 | 通过 |
| 55章书稿 | 清单、标题、长度、图像、就近来源及章节相对链接检查 | 通过 |
| Lean两份文件 | 对照既有通过日志的SHA-256与当前源码 | 一致；本次未重新运行Lean |

复现入口是[示例说明](../examples/rocq/README.md)与[scripts/check_rocq.py](../scripts/check_rocq.py)。脚本以任务专用build目录暂存源码，重新生成证明对象；重查没有使用跳过模块或依赖验证的参数。完整命令、标准输出、错误输出、退出码和源码SHA-256均保留在JSON中。全局假设闭合不等于无需信任逻辑、检查器或规格。

机器编译发现基础文件的`Nat.add_succ`不在该版本环境中，已改为实际可用的`Nat.add_succ_r`，并同步正文与审稿记录。HeapModel保留Fin.t替代类型建议警告，不把警告隐藏或当作失败。

本次安装使用用户目录中的OCaml与opam，任务本地编译器启动器只调整可执行文件、运行时和库路径；Rocq内核与标准库未修改。复现所需的正常安装命令已给出，临时编译器运行时不打包进入书稿。

## 验证范围

CompCert章实际阅读官方定理及源码，再以纯自然数表达式模型解释优化保持；没有重新构建或验证完整CompCert。VST章实际阅读sumarray与链表案例，另以有限地址独占堆模型解释框架推理；没有导入VST/Clight依赖，也没有运行示例C函数的semax_body工程。

列表模型不含业务请求去重；自然数表达式不含机器溢出、I/O或异常；有限堆不含C字节布局、对齐、释放和共享份额。真实可执行文件的保证还依赖源文件对应、前端、编译与外部环境条件。正文和示例README均明确区分这些层次。

## 工程归档

构建输出合并Markdown、分章稿、图像、示例、检查脚本与完整工程ZIP。Git提交保留规划、并行内容和整合验证步骤；ZIP内的build/history.bundle可恢复全部已提交历史。生成的证明对象和临时运行时不属于源码交付，读者可用固定版本重新生成。

[51章版审校报告](review-expanded.md)与更早交叉报告作为历史证据保留，本版章号以当前对照表为准。
