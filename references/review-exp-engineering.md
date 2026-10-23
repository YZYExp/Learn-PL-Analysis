# 工程闭环组对证明篇的交叉审稿

本报告按稳定ID记录审查位置；最终展示章号见[编号对照](chapter-map.md)。

范围：完整阅读稳定ID40–42正文与`examples/lean/ProgramProofs.lean`，实际渲染查看六张对应SVG；核对`examples/lean/check-results.json`记录的工具版本、退出码与公理输出。Lean运行环境由主编维护，本审稿没有另行更换工具链或重复声明独立检查。

## 核对结果

- **金额守恒**：`refund_conservation`的前提`amount≤paid`与`Nat.sub_add_cancel`相符。正文明确自然数减法截断，越界反例100/200正确。
- **请求计数**：`successes`递归以请求数量为递减参数，成功后转移状态，拒绝后保留状态；`refunded_successes`、`paid_successes`与`at_most_one`的组合和正文归纳说明一致。计数是抽象成功转换，未冒充真实支付效果。
- **程序等价**：`remove_zero_correct`只针对纯、总、无限精度自然数函数。正文明确没有证明耗时相等，没有将其外推到副作用、浮点或未定义行为。行为子集精化示例和无限均匀正整数练习均准确。
- **局部与多步可靠性**：`gamma`/`incAbs`/`inc`定义与`inc_sound`一致；`run_sound`对任意中间a、z泛化后归纳，能正确组合局部定理。正文明确模型没有CFG、分支、工作列表，不认证Python分析器。
- **可信边界**：证明代码未见sorry、admit或自设公理；文件中有五个`#print axioms`。check-results.json记录前三项含propext、后二项含propext与Quot.sound，与42章陈述对应。正文没有把“无自设业务公理”说成“没有任何公理”。
- **图文对应**：六图均纵向展示输入→推理→结论或边界；40章状态归纳、41章外部构建边界、42章覆盖关系和TCB分层未发现语义方向错误。

## 建议主编整合

1. **补充检查对象身份（低优先级，工程追溯改进）**：`check-results.json`目前有版本与退出码，但每个文件条目未见内容摘要。建议最终检查时记录证明源文件SHA-256，并将其与检查命令/输出绑定，便于确认报告对应当前交付字节。它只提供对象身份，不增加形式保证。
2. **明确编写与展示编号差异（主编已计划）**：源文件采用稳定ID40–42，展示章号将变更。最终统一正文小节号、图号和导航，不重命名证明文件中的稳定章节说明。
3. **无需扩大证明承诺**：本组49章恢复模型与40章顺序状态机不同。两者相互补充：顺序一次成功定理没有覆盖崩溃窗口；恢复有限图也未验证真实支付服务。建议保持当前两个边界说明。

未直接修改40–42或ProgramProofs.lean；未发现必须修复的数学或代码语义错误。

## 本组新增工程实验实测记录

命令：`python3 examples/extension_checks.py`与`python3 -m unittest discover -s examples -p 'test_extension_checks.py' -v`。

- 退款无去重：8状态，重复轨迹为提交意图、同键送达、确认前崩溃、同键重送。
- 退款有原子远端去重：5状态，模型中未出现效果次数2。
- 失效闭包：gateway-model、refund-summary、handler-summary、report；unrelated未被纳入。
- 有限CEGIS：always-zero由(1,1)反例排除，raw-request由(0,-1)排除，clamp在固定18组输入中通过。
- 8项测试全部通过。模型范围与未建模条件已在49–51章和examples/EXTENSION.md说明。
