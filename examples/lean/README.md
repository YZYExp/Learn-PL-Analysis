# Lean 证明文件与检查

工具链固定为 `leanprover/lean4:v4.19.0`，在根目录 lean-toolchain 中声明。文件只 import Std，不需要Mathlib或Lake工程。两个文件各自独立；从本项目根目录运行。

## 常规环境

已安装该版本并可从PATH调用Lean时：

```bash
lean --version
lean examples/lean/Foundations.lean
lean examples/lean/ProgramProofs.lean
python3 scripts/check_lean.py
```

若使用elan管理工具链，可按[官方安装说明](https://lean-lang.org/lean4/doc/quickstart.html)安装，随后安装固定版本；也可使用[Lean4.19.0官方发布包](https://github.com/leanprover/lean4/releases/tag/v4.19.0)并向检查脚本传入 `--lean /path/to/lean`。工具链下载与本书Markdown构建分开，书稿构建不要求安装Lean。

## 实际检查记录

[check-results.json](check-results.json)记录工具链版本、每份文件的SHA-256、退出码、标准输出与公理依赖。该记录对应本次交付代码，重新检查将覆盖此记录。

Foundations.lean的四个定理分别展示合取交换、蕴含组合、自然数归纳、接受项计数上界。ProgramProofs.lean的五个主要定理涉及自然数金额守恒、至多一次模型、纯函数变换等价，以及微型抽象转移和有限多步覆盖。后者不等于证明整套Python分析器、真实支付系统或编译器正确。

`#print axioms`展示当前定理在Lean逻辑中的依赖。基础文件四个定理无公理依赖；程序证明采用标准基础中的propext，部分还使用Quot.sound，详见日志。不使用sorry/admit或自行添加公理完成目标；检查脚本拒绝非零退出和日志中的sorryAx。

## 特定Linux运行环境的可选启动适配

本次运行环境允许读取 `/proc/self/exe`，但不允许Lean4.19.0采用的 `/proc/<自身pid>/exe` 路径发现方式。因此检查使用了 [linux_app_path_compat.c](linux_app_path_compat.c)。适配仅将当前进程自己的可执行文件定位路径改为 `/proc/self/exe`，其他readlink调用透传；未修改Lean内核、证明规则、标准库或证明文件。

遇到相同启动错误时，可在具备C编译器的Linux环境选择：

```bash
python3 scripts/check_lean.py --lean /path/to/lean --linux-app-path-compat
```

适配库生成到build目录，只用于该命令启动的Lean子进程。普通环境不需要此参数。实现依据是[Lean4.19.0运行时io.cpp中的lean_io_app_path](https://github.com/leanprover/lean4/blob/v4.19.0/src/runtime/io.cpp)。
