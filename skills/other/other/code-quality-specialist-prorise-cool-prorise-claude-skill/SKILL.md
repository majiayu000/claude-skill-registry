---
description: 提供代码审查、性能分析、重构建议、错误诊断和调试能力。当需要代码质量评估、性能优化、或问题排查时使用。
name: code-quality-specialist
---
# Code Quality Specialist

提供代码审查、性能分析、重构建议、错误诊断和调试能力。当需要代码质量评估、性能优化、或问题排查时使用。

## Skill Index

<!-- AUTO-GENERATED-SKILL-INDEX:START -->
以下索引由 `node scripts/update-skill-index.js` 自动生成，用于让 Claude 在顶层专家触发后继续路由到最相关的子技能。

### Claude 使用说明

1. 先将用户当前任务与每个子技能的 `触发语义` 进行语义匹配，不要只看目录名。
2. 一旦找到最相关的子技能，立即打开其 `入口文件` 指向的 `SKILL.md`，把它作为下一层入口。
3. 进入子技能后，再根据该子技能自己的说明按需加载同目录下的 `references/`、`scripts/`、`assets/`，不要在顶层专家中预先展开大段细节。
4. 如果多个子技能都相关，先加载最贴近主目标的那个，再按需补充其他子技能，避免一次性加载过多上下文。
5. 下方 `入口文件` 路径相对于项目根目录，可直接用于 `Read` 操作。

### 子技能索引

#### code-reviewer (1)
- `code-reviewer`
  - 触发语义: Expert code reviewer who provides constructive, actionable feedback focused on correctness, maintainability, security, and performance — not style preferences.
  - 入口文件: `.claude/skills/code-quality-specialist/references/domains/code-reviewer/SKILL.md`

#### review-workflow (1)
- `review-code`
  - 触发语义: Multi-dimensional code review with structured reports. Analyzes correctness, readability, performance, security, testing, and architecture. Triggers on "review code", "code review", "审查代码", "代码审查".
  - 入口文件: `.claude/skills/code-quality-specialist/references/domains/review-workflow/SKILL.md`

#### skill-quality (1)
- `skill-tuning`
  - 触发语义: Universal skill diagnosis and optimization tool. Detect and fix skill execution issues including context explosion, long-tail forgetting, data flow disruption, and agent coordination failures. Supports Gemini CLI for deep analysis. Triggers on "skill tuning", "tune skill", "skill diagnosis", "optimize skill", "skill debug".
  - 入口文件: `.claude/skills/code-quality-specialist/references/domains/skill-quality/tuning/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
