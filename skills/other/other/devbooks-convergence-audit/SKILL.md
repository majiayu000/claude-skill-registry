---
name: devbooks-convergence-audit
description: devbooks-convergence-audit：以证据优先、声明存疑的原则评估 DevBooks 工作流收敛性，检测"西西弗斯反模式"和"假完成"。主动验证而非信任文档声明。用户说"评估收敛性/检查升级健康度/西西弗斯检测/工作流审计"等时使用。
recommended_experts: ["System Architect"]
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash
---

# DevBooks：收敛性审计（Convergence Audit）

## 渐进披露
### 基础层（必读）
目标：以证据优先审计收敛性，识别假完成、假绿与伪证据。
输入：变更包、verification.md、evidence/、tests/、代码与 git 历史。
输出：审计报告、可信度评分、需返工或补证据清单。
边界：不修改代码或 tests/；不替代实际测试执行；结论以可验证证据为准。
证据：报告引用的日志/命令输出路径或时间戳。

### 进阶层（可选）
适用：需要具体检查脚本、评分规则或交叉验证策略时。

### 扩展层（可选）
适用：需要定制输出模板或与现有闸门联动时。

## 核心要点
- 原则：声明存疑、证据优先、交叉验证。
- 覆盖检查：Status/AC/任务完成度/证据有效性/git 历史/实时测试。
- 输出：收敛性审计报告 + 可信度评分。

## 参考资料
- `skills/devbooks-convergence-audit/references/收敛性审计细则.md`：反迷惑原则、检查清单与脚本、评分算法、报告模板与完成状态。

## 推荐 MCP 能力类型
- 代码检索（code-search）
- 引用追踪（reference-tracking）
- 影响分析（impact-analysis）
