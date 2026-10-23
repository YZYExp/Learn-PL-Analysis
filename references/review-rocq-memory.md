# Rocq扩展交叉审稿：内存资源组

本组制作稳定ID55及HeapModel.v，交叉审阅稳定ID54与CompilerModel.v。

## 第55章制作范围

- 正文约2100汉字，3张760×900纵向SVG，全部XML解析、fitz渲染并逐张查看，链接有效。
- 实际浏览VST官方Verif_sumarray、Verif_reverse教程、VST progs/verif_sumarray.v源码与CompCert Clight定义。
- 原创bump例子区分Tsh可写对象资源、数值上界、unsigned回绕及非空指针不足；解释用funspec骨架明确未独立编译。
- 官方数组例子保留机器模求和语义、计数范围、前缀和与资源不变三类责任；不宣称在本环境重编VST。
- HeapModel.v以Fin.t bound构成有限地址域，option Z表示独占单元，堆相等使用逐地址相等；不依赖函数外延性假设。框架结论仅用于已有单元的写入前提；模型不含C布局、对齐、释放、共享份额或并发。

## 对第54章的审查

- 核对官方Compiler模块的transf_c_program_correct：从成功的CompCert C AST→Asm AST转换得到指定backward_simulation，正文端点与方向准确。
- 核对Smallstep模块：允许零步匹配时以良基关系排除无限停顿，正文没有将任意前向模拟误当作目标无额外行为。
- 核对Behaviors模块：终止、静默发散、持续交互、出错的区分，以及behavior_improves的出错前缀关系准确。
- 分别编译的形式链接条件与实际系统链接器边界明确；未将核心定理扩大到外部汇编/链接/运行环境。
- Allocproof的validated RTL→LTL翻译定位准确；正文没有把启发式提出候选等同于已证明优化器。

CompilerModel.v源码审阅：smart_add只折叠常量或删除右侧字面零；eval_smart_add分类覆盖各构造；optimize_correct对子表达式结构归纳；observes基于返回自然数，明确不含机器溢出、内存、I/O与非终止。demo的形状为x+5，环境值10时结果15。未发现逻辑阻断项。

## 代码检查状态

Rocq 9.0.0实际检查结果等待主编提供工具链后补充。目前只有源码审阅，不宣称已由Rocq接受。

初始源码标识：

- HeapModel.v SHA-256：2f8e509f9d1f559828f17778a469a2eb8f8aae7d0cd87be7c19e759cc5ef9900。
- CompilerModel.v SHA-256：a9c4b676e804a10d132049fe746eef0ea9c4e8908c075fe9f92033fbec3fb8e3。

两文件均无Admitted、admit、自设Axiom或Parameter，包含Print Assumptions。源码无这些标记不替代实际内核检查，后者以运行日志为准。

## 整合后的机器检查

本文上面的待检描述保留审稿时状态。整合后，三份Rocq文件已在9.0.0下编译与独立重查通过；最终源码摘要、实际命令和假设查询见[统一审校记录](review-rocq.md)及[原始检查报告](../examples/rocq/check-results.json)。
