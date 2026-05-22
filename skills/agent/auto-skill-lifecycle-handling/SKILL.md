---
id: "c4a030e5-356f-4d95-9421-93f4a499d458"
name: "auto-skill-lifecycle-handling"
description: "自动处理 Agent Skill 的全生命周期：在用户反馈中识别稳定约束以触发技能抽取；合并新增偏好实现版本演进（如 v0.1.0 → v0.1.1）；并在后续相似任务中精准检索并注入对应技能。"
version: "0.1.0"
tags:
  - "skill-lifecycle"
  - "ell"
  - "agent-skill"
  - "feedback-loop"
  - "versioned-skill"
triggers:
  - "技能抽取"
  - "技能更新"
  - "技能检索"
  - "自动版本升级"
  - "反馈驱动进化"
---

# auto-skill-lifecycle-handling

自动处理 Agent Skill 的全生命周期：在用户反馈中识别稳定约束以触发技能抽取；合并新增偏好实现版本演进（如 v0.1.0 → v0.1.1）；并在后续相似任务中精准检索并注入对应技能。

## Prompt

# Goal
自动识别用户交互中可复用的稳定约束，执行技能抽取 → 技能更新 → 技能检索三阶段闭环，确保能力随真实反馈持续进化且不冗余。

# Constraints & Style
- 必须仅在用户显式给出**稳定、可泛化、非一次性**的约束时触发抽取（如“别幻觉”“要标出处”“用Word格式”），禁止对通用请求（如“写个报告”）生成技能。
- 技能抽取必须生成标准 `SKILL.md` 制品，含明确 `name`、`description`、`prompt`、`triggers` 等字段，支持本地存储与跨系统迁移。
- 技能更新必须基于语义相似性匹配已有技能，优先合并而非新建，并自动递增 patch 版本（如 `v0.1.0` → `v0.1.1`），保留演化轨迹。
- 技能检索必须在新任务中基于向量化语义匹配，严格按 `top_k` 与 `min-score` 过滤，仅注入高置信度技能上下文。
- 禁止虚构技能逻辑、版本规则或工程细节（如不假设具体 embedding 模型或文件路径）；所有行为必须忠实反映用户定义的生命周期策略。

# Workflow
- Step 1: 监听用户消息，检测是否含稳定约束（如否定式指令“不要…”、补充式要求“还要…”、格式化指令“用…格式”）。
- Step 2: 若满足抽取条件，生成 Skill Candidate 并进入维护流程：先相似匹配 → 再决定新增/合并/丢弃 → 合并则自动 bump patch version。
- Step 3: 在后续用户 Query 中，执行 query 重写 → 向量检索 → 技能筛选 → 注入 prompt 上下文 → 驱动 LLM 生成结果。

## Triggers

- 技能抽取
- 技能更新
- 技能检索
- 自动版本升级
- 反馈驱动进化
