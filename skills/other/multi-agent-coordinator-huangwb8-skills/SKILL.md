---
name: multi-agent-coordinator
description: Use when executing implementation plans with independent tasks - dispatches fresh subagent for each task with code review between tasks, enabling fast iteration with quality gates. Supports orchestrator, peer-to-peer, and pipeline coordination modes.
metadata:
  short-description: 多代理协调与编排
  keywords:
    - multi-agent-coordinator
    - 多代理
    - 协调器
    - 并行处理
    - 任务编排
    - 工作流
    - 任务分发
    - 结果聚合
    - subagent-driven-development
    - coordination
  category: 架构设计
  author: Bensz Conan
  platform: Claude Code | OpenAI Codex | ChatGPT
---

# Multi-Agent Coordinator - 多代理协调专家

目标：把“复杂开发任务”拆成可并行的独立任务，分派给子代理执行，并在任务间做质量门禁（代码审查 + 轻量测试），最后聚合成一致的可交付结果。

为满足社区推荐的 `SKILL.md` 500 行以内约束：完整细节/长示例已下沉到 `awesome-code/agents/multi-agent-coordinator/references/legacy-skill-full.md`。

## 核心原则（Subagent-Driven Development）

- 任务拆分要原子：每个任务有明确输入/输出/验收标准
- 每个任务用“全新子代理”：降低上下文污染与确认偏差
- 任务之间强制门禁：至少一次代码审查；必要时补回归测试
- 结果必须可聚合：统一术语、接口约定、日志口径与错误处理风格

## 何时使用

- 用户给出明确实施计划/任务清单，需要并行推进
- 任务跨度大（多文件/多模块/多领域），单线程容易遗漏或拖慢
- 需要严格质量门禁（合并前必须审查、必须验证）

## 输入

- 计划来源：用户文字 / `PLAN.md` / issue 列表 / TODO 列表
- 约束：时间、兼容性、目录边界、不可破坏性要求
- 验收：测试要求、性能目标、行为回归标准

## 输出

- 一个可执行的“任务编排表”（任务 → 负责人子代理 → 依赖 → 验收）
- 每个任务的结果摘要（改动点、风险、验证）
- 最终聚合报告（P0/P1/P2 风险 + 下一步）

## 工作流

1. 读取计划并生成任务清单
   - 将大任务拆成 3-15 个原子任务
   - 为每个任务写清：目标、范围、验收、风险、依赖

2. 选择协调模式
   - orchestrator：默认；中心协调器分派任务并统一口径
   - peer-to-peer：小团队/低耦合；允许子代理互相同步但必须记录决定
   - pipeline：强依赖链；按阶段推进（例如：设计→实现→测试→文档）

3. 分派任务（可并行）
   - 并行仅限“文件/模块不重叠”或“改动可安全合并”的任务
   - 明确要求：输出必须包含（a）改动说明（b）验证方式（c）潜在回滚点

4. 任务间门禁（强制）
   - 对每个任务结果做快速审查：安全/正确性/一致性/边界条件
   - 必要时补回归测试或最小验证步骤

5. 聚合与冲突解决
   - 先合并“口径/接口/命名/日志风格”，再合并代码
   - 如出现冲突：优先保持正确性与可读性；无法判定时暂停并向用户确认

6. 最终交付检查
   - 关键路径功能可跑通
   - 无明显安全/路径越界/敏感信息泄露
   - 产出文档与代码一致（如有）

## 协调器自检清单

- [ ] 任务拆分是否避免重叠修改同一文件？
- [ ] 是否为每个任务定义了可验证的验收标准？
- [ ] 并行任务是否有清晰的依赖边界？
- [ ] 每个任务是否经过最小审查与验证？
- [ ] 聚合后是否统一了术语与接口风格？

