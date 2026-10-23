# Foundations.lean 验证记录

- 文件：`examples/lean/Foundations.lean`
- 工具：Lean 4.19.0，提交 `6caaee842e94`（由主编核对工具版本）
- 依赖：`import Std`，无 Mathlib。
- 最终实际检查退出码：0。
- 验证日期：2026-10-22。

## 实际命令

从项目根目录执行：

```sh
env LD_PRELOAD=/workspace/scratch/e80ec5415df1/program-analysis-book/build/lean-app-path-compat.so /workspace/scratch/e80ec5415df1/lean-runtime/lean-4.19.0-linux/bin/lean examples/lean/Foundations.lean
```

本次受限执行环境对程序定位自身路径有约束。主编提供的兼容适配仅将查询本进程可执行文件的路径改到 `/proc/self/exe`，未修改 Lean 内核或证明规则；源码见 `examples/lean/linux_app_path_compat.c`。普通 Lean 安装使用书中标准命令 `lean examples/lean/Foundations.lean`，不需要该适配。

## 最终实际输出

```text
2
'Foundations.and_swap' does not depend on any axioms
'Foundations.implication_chain' does not depend on any axioms
'Foundations.twoPerItem_eq_add' does not depend on any axioms
'Foundations.acceptedCount_le_length' does not depend on any axioms
```

四项定理依次覆盖命题合取交换、蕴含组合、自然数归纳与列表归纳。没有使用证明占位符、自设公理或原生计算证明策略。

## 修订与保证范围

自然数归纳的初版使用较宽泛的化简集，触发递归深度错误，未被作为通过版本交付。最终改成显式 `calc` 等式链及 `congrArg`，逐步应用归纳假设、`Nat.add_succ` 和 `Nat.succ_add`，然后重新检查并获得上述输出。

此项检查证明的是文件内形式定义与形式命题；接受条目数并不表示不同业务请求数，`Nat` 也不等于固定机器位宽计数器。模型未覆盖外部支付、持久化或并发，不据此宣称生产退款系统已验证。
