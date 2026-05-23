---
name: devbooks-void
description: devbooks-void：Void 协议执行器：处理高熵/不确定/多方案争议问题，只产出 research_report + ADR + Freeze/Thaw 工件，不产出生产代码。用户说"进入 void/卡住了/不确定/需要调研/冻结解冻"等时使用。
recommended_experts: ["Research Lead", "System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Edit
  - Bash
---

# DevBooks：Void（高熵问题协议）

## 渐进披露
### 基础层（必读）
目标：把“输入不足/不确定/多方案争议”转换为可审计的知识与决策工件，并通过 Freeze/Thaw 控制后续执行。
输入：用户请求、变更包元数据（proposal front matter）、已存在的证据与 Gate Report（若有）。
输出（MUST）：
- `void/research_report.md`：结论、约束、证据来源、影响面、风险与下一步建议
- `void/ADR.md`：Context / Options / Decision / Consequences
- `void/void.yaml`：Freeze/Thaw 状态、阻塞问题清单、已解决问题与引用

边界（MUST）：
- Void 阶段不得产出生产代码变更；不得修改 tests/ 或 src/。
- Void 的产物必须可被脚本校验（见 `void-protocol-check.sh`）。

证据：Void 工件存在且非空；Freeze/Thaw 状态与变更包 state/next_action 一致。

### 进阶层（可选）
适用：需要把 research_report 的结论回写为 Truth（Decision/Constraints）或生成后续 Knife/Bootstrap 的输入索引时。

## 核心要点
- 先做配置发现（`.devbooks/config.yaml`）与规则文档读取，再进入 Void 输出。
- 结论必须可操作：包含明确的 next_action（Bootstrap/Knife/DevBooks）与阻塞解除条件。
- Freeze 时必须阻断后续执行；Thaw 必须链接 ADR 与证据，并记录吸收路径。

## 参考资料
- `dev-playbooks/specs/void/spec.md`
