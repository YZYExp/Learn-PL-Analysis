# 扩展版交叉审稿：第37–39章与 Foundations.lean

本报告按稳定ID记录审查位置；最终展示章号见[编号对照](chapter-map.md)。

审稿者：细化／信息流／数值组。阅读三章正文、对应6张SVG、完整Lean文件及已有验证记录；SVG经Inkscape渲染后查看联系图。复核Lean官方教材的命题与证明、归纳递归、公理与计算章节。

## 结论

未发现需要阻断交付的逻辑、源码或图解错误。形式模型与业务实现的边界有明确说明，命题、有限计算和全称证明没有混淆。第39章所示定义和列表归纳定理与实际源码对应。

## 实际复核 Lean

使用主编验证记录提供的工具路径和兼容适配，在项目根目录独立重跑：

```sh
env LD_PRELOAD=/workspace/scratch/e80ec5415df1/program-analysis-book/build/lean-app-path-compat.so /workspace/scratch/e80ec5415df1/lean-runtime/lean-4.19.0-linux/bin/lean --version
env LD_PRELOAD=/workspace/scratch/e80ec5415df1/program-analysis-book/build/lean-app-path-compat.so /workspace/scratch/e80ec5415df1/lean-runtime/lean-4.19.0-linux/bin/lean examples/lean/Foundations.lean
```

实际版本：Lean 4.19.0，x86_64-unknown-linux-gnu，提交6caaee842e94，Release。实际退出码0；输出计算值2；and_swap、implication_chain、twoPerItem_eq_add、acceptedCount_le_length均报告无公理依赖。没有以仅阅读源码代替运行。

## 检查要点

- 37章原子账本模型中，初态及接受/重复/非法动作保持累计不超过已支付金额；不同键700+700的反例正确。
- 37章明确原子前提、未建模网络崩溃，以及重复键更换内容时的返回语义缺口；永远拒绝满足部分安全性但不满足服务目标的例子有用。
- 38章合取交换、蕴含组合、量词次序与Bool/Prop区别正确；未把P→Q解释成时间先后。
- 38章正确提醒Nat减法截断，防止把模型类型选择当成业务事实。
- 39章acceptedCount的true/false分支与代码一致；归纳假设仅作用于尾列表；twoPerItem等式链的方向与所用自然数定理正确。
- 39章把“计数不超长度”与“确实只计接受条目”分开，练习能暴露弱规格。
- 6张图未见文字溢出、关系箭头错误或对模型保证的夸大。

## 小幅工程建议

固定工具链目前主要通过书中文字及验证命令体现。交付中宜同时提供标准工具链选择文件（例如examples/lean/lean-toolchain或根目录的等效文件），方便普通环境通过elan选择4.19.0；这不影响本次已通过的实际检查。兼容适配与绝对环境路径仅属于本次执行记录，普通读者继续使用正文的标准命令。

未直接修改37–39章或他人证明文件。
