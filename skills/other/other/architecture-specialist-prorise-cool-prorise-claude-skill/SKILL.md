---
description: 提供系统架构设计、技术选型、架构审查和组件设计能力。当需要设计新系统、重构现有架构或进行架构审查时使用。
name: architecture-specialist
---
# Architecture Specialist

提供系统架构设计、技术选型、架构审查和组件设计能力。当需要设计新系统、重构现有架构或进行架构审查时使用。

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

#### autonomous-optimization-architect (1)
- `autonomous-optimization-architect`
  - 触发语义: Intelligent system governor that continuously shadow-tests APIs for performance while enforcing strict financial and security guardrails against runaway costs.
  - 入口文件: `.claude/skills/architecture-specialist/references/domains/autonomous-optimization-architect/SKILL.md`

#### lsp-index-engineer (1)
- `lsp-index-engineer`
  - 触发语义: Language Server Protocol specialist building unified code intelligence systems through LSP client orchestration and semantic indexing
  - 入口文件: `.claude/skills/architecture-specialist/references/domains/lsp-index-engineer/SKILL.md`

#### project-analysis (1)
- `project-analyze`
  - 触发语义: Multi-phase iterative project analysis with Mermaid diagrams. Generates architecture reports, design reports, method analysis reports. Use when analyzing codebases, understanding project structure, reviewing architecture, exploring design patterns, or documenting system components. Triggers on "analyze project", "architecture report", "design analysis", "code structure", "system overview".
  - 入口文件: `.claude/skills/architecture-specialist/references/domains/project-analysis/SKILL.md`

#### software-architect (1)
- `software-architect`
  - 触发语义: Expert software architect specializing in system design, domain-driven design, architectural patterns, and technical decision-making for scalable, maintainable systems.
  - 入口文件: `.claude/skills/architecture-specialist/references/domains/software-architect/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
