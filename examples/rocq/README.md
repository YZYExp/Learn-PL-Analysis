# Rocq 自包含证明模型

固定使用 **Rocq 9.0.0 与 Stdlib 9.0.0**。它是本书选定的复现版本，不是对最新版本的声明。三个文件只依赖核心和标准库，互不导入，不需要 CompCert、VST 或第三方策略库。

| 文件 | 内容 | 假设查询数 |
|---|---|---:|
| [Foundations.v](Foundations.v) | 合取、蕴含、自然数归纳与列表计数 | 5 |
| [CompilerModel.v](CompilerModel.v) | 纯自然数表达式优化与求值保持 | 5 |
| [HeapModel.v](HeapModel.v) | 有限地址、独占单元与局部更新框架 | 6 |

## 安装与检查

参考 [Rocq 9.0 发布说明](https://rocq-prover.org/releases/9.0)及[官方安装说明](https://rocq-prover.org/install)。已安装 OCaml/opam 的常规环境可创建独立 switch，再明确约束核心与标准库版本：

```sh
opam switch create book-rocq ocaml-base-compiler.4.14.1
opam install --switch=book-rocq rocq-prover.9.0.0 rocq-core.9.0.0 rocq-stdlib.9.0.0
eval $(opam env --switch=book-rocq)
python3 scripts/check_rocq.py
```

以上 Python 命令从全书项目根目录运行，也可传 `--rocq /path/to/rocq`。元包版本不能代替实际 `rocq --version` 与标准库版本检查；依赖求解可能选择较新的兼容包，因此安装命令同时约束三者。

脚本把源码复制到 `build/rocq-check/`，以逻辑前缀 `BookRocq` 编译，避免把生成文件混入示例目录。每个文件中的 `Print Assumptions` 用于检查定理的全局假设依赖。`Closed under the global context` 说明查询的结论没有全局假设依赖，仍须信任逻辑、内核与所用定义，也须审查命题是否表达了需求。

[检查结果](check-results.json)保存版本、实际命令、源码 SHA-256、退出码和完整输出；编译后还对每个模块执行 `rocq check -silent -Q build/rocq-check BookRocq BookRocq.<模块名>`，重新检查证明对象与依赖。三文件共16份假设查询均闭合，三次独立重查均通过。[实际安装清单](installation.json)另记录OCaml、核心、运行时与标准库包版本。本次检查使用 `--package-inventory examples/rocq/installation.json` 将该清单摘要绑定到报告；自行复现时可不传这个可选参数，或提供自己环境的新清单。应先核对 SHA-256 是否与当前源码相同，再阅读通过标记。工具链安装与操作系统依赖不属于普通 Markdown 构建要求。

## 结论适用于哪里

- 计数定理讨论有限布尔列表与数学自然数，不含请求去重、持久化、网络或机器溢出。
- 表达式定理讨论总的纯函数模型。它没有运行 CompCert 的编译器或重新检查其整套证明。
- 有限堆定理讨论 `Fin.t bound` 地址与独占资源，没有导入 Clight/VST，没有运行 C 函数的 `semax_body` 证明，也没有覆盖字节布局、对齐或共享份额。

CompCert/VST 章节提供真实官方工程的定理、源码与责任边界阅读；随书的小模型用于解释证明结构。它们的验证状态应分别判断。

## 本次实测说明

三份文件已在固定版本下编译并独立重查。`HeapModel.v`保留标准库关于`Fin.t`替代类型的建议警告；它不是未完成证明或检查失败。机器检查曾发现旧引理名`Nat.add_succ`不存在，现源码和同题正文已改为`Nat.add_succ_r`。

构建环境使用用户目录中的OCaml及opam；任务本地启动器调整OCaml工具的可执行文件和库路径。Rocq内核与Stdlib未修改。报告中的绝对路径是本次实测位置，复现时由脚本重新生成。
