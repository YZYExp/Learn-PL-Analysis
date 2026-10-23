# 扩展版交叉审稿：程序证明组

本报告按稳定ID记录审查位置；最终展示章号见[编号对照](chapter-map.md)。

本组制作稳定ID40–42三章与六张纵向SVG，另审阅稳定ID46–48全文与六张图。

## ProgramProofs.lean 实际检查

- 文件：examples/lean/ProgramProofs.lean。
- SHA-256：fcd71ca2dfbb9dcff9ac5ee4ae09e3f63e15b2cd33dc42c5524bdff24a79247d。
- 工具链：Lean 4.19.0（主编安装的固定版本）。仅import Std，不依赖Mathlib。
- 命令（从工程根目录）：

```bash
env LD_PRELOAD=/workspace/scratch/e80ec5415df1/program-analysis-book/build/lean-app-path-compat.so \
  /workspace/scratch/e80ec5415df1/lean-runtime/lean-4.19.0-linux/bin/lean \
  examples/lean/ProgramProofs.lean
```

- 结果：退出码0。自然数金额守恒、拒绝重复请求、任意有限请求序列成功次数≤1、纯自然数改写等价、局部加一抽象覆盖、任意有限步覆盖，全部检查成功。
- 环境适配：LD_PRELOAD库仅处理该运行环境下Lean自身可执行文件位置发现，源码由主编放在examples/lean/linux_app_path_compat.c。未改变Lean内核、证明规则和逻辑；普通Lean环境不需要该适配。
- `#print axioms`结果：refund_conservation、at_most_one、remove_zero_correct依赖propext；inc_sound、run_sound依赖propext与Quot.sound。没有自设公理，没有sorry、admit，不宣称“零公理”。
- 覆盖限制：证明对象为配套极小Lean模型。没有证明Python教学分析器、真实支付服务、通用编译器或实际硬件执行。纯函数等式没有性能结论；顺序状态机没有并发或崩溃恢复结论。
- 三章中的Lean摘录与配套文件保持同名、同定义、同定理；run_sound通过对任意中间抽象/具体状态的一般化归纳组合inc_sound。

## 本组制图检查

40–42共六张760×900纵向SVG，正文有相对链接、替代文本和图注。已XML解析、fitz渲染并逐张查看，未发现文字溢出、遮挡或语义错配。字号24以上，定义→义务→推理→结论自上而下。

## 对46–48的交叉审查

| 稳定ID | 审查重点 | 结论 |
|---|---|---|
| 46 | CEGAR近似方向、完整路径约束、三值求解结果、未知调用副作用 | 复制例子的不可满足公式正确；细化保留真实行为；unknown未被冒充安全；没有把深度扩展与抽象细化混淆 |
| 47 | 非干扰的双执行语义、显式/隐式流、观察边界、降密与差分隐私 | 确定终止模型假设明确；两秘密输入未强制相同；返回值与终止/时间观察分开；去标识化未被冒充隐私证明 |
| 48 | binary64舍入、两种结合顺序、稳定改写、条件数、FMA | 2^53例子及2^54平方根例子正确；κ(x)=0.5√(x/(x+1))推导成立；FMA示例遵循明确舍入位置而非硬件实测 |

六张SVG均已渲染查看，未发现阻断图文问题。特别核对ch48-stability.svg的条件数根号作用于整个x/(x+1)，与正文一致。

## 复核执行

在当前Python环境（radix=2、mant_dig=53）独立执行：

- x=2^53时，左结合结果0.0，右结合结果1.0。
- x=2^54时，平方根直接相减为0.0，有理化结果为2^-28。
- a=2^27+1、b=2^27-1，整数精确乘积减2^54为-1；分离binary64乘法与减法结果为0.0。

没有执行硬件FMA，也没有把有限数值检查写成全域稳定性证明。对46–48未发现阻断交付的问题，无需修改他人章节。
