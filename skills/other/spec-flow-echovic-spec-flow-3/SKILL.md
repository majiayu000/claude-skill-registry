---
name: spec-flow
description: "Spec-driven development workflow. Interactive phase-by-phase confirmation from proposal to implementation. Trigger: 'spec-flow', 'spec mode', 'need a plan', 'structured development', 'write a spec', 'feature spec', 'technical spec', '需求文档', '技术方案', '任务拆解', '规格驱动', '写个方案', '做个规划', '结构化开发', 'plan this feature', 'break this down', 'design doc'. Creates .spec-flow/ directory with proposal, requirements, design, and tasks."
argument-hint: "[feature description] [--fast] [--skip-design]"
---

# Spec-Flow - Structured Development Workflow

Structured workflow for complex feature development. Creates living documentation that guides implementation and serves as team reference.

## Core Principles

1. **One phase at a time** — NEVER generate documents for subsequent phases in advance
2. **Mandatory confirmation** — After each phase, STOP and wait for user confirmation
3. **User-driven progression** — Only proceed when user says "continue"/"ok"/"next"/"继续"/"好"

## Parameters

| 参数 | 说明 |
|------|------|
| `--fast` | 跳过逐阶段确认，一次性生成所有文档（最后整体确认） |
| `--skip-design` | 跳过 Design 阶段（简单功能，架构显而易见时） |

## Language Rule

**所有生成的 .md 文件必须使用中文。**

## Interaction Rules

Load `references/interaction-rules.md` for detailed confirmation templates and prohibited behaviors.

---

## Five-Phase Workflow

Copy this checklist and check off items as you complete them:

### Spec-Flow Progress:

- [ ] **Phase 0: Initialize** ⚠️ REQUIRED
  - [ ] 0.1 Run `scripts/init-spec-flow.sh <feature-name>` or create `.spec-flow/active/<feature>/`
  - [ ] 0.2 Check if `.spec-flow/steering/` exists — if so, read for project context
  - [ ] 0.3 问自己：**这个功能的核心价值是什么？用一句话能说清吗？**

- [ ] **Phase 1: Proposal** ⚠️ REQUIRED
  - [ ] 1.1 Create `.spec-flow/active/<feature>/proposal.md` using `templates/proposal.md.template`
  - [ ] 1.2 包含：Background, Goals, Non-Goals, Scope, Risks, Open Questions
  - [ ] 1.3 问自己：**有没有隐含的需求没写出来？**
  - [ ] 1.4 问自己：**Non-Goals 是否足够明确？能防止 scope creep 吗？**
  - [ ] 1.5 ⏸️ 确认节点 — 等待用户确认后继续

- [ ] **Phase 2: Requirements**
  - [ ] 2.1 Create `.spec-flow/active/<feature>/requirements.md` using `templates/requirements.md.template`
  - [ ] 2.2 Load `references/ears-format.md` — 使用 EARS 格式编写需求
  - [ ] 2.3 包含：FR-xxx 功能需求, NFR-xxx 非功能需求, AC-xxx 验收标准
  - [ ] 2.4 问自己：**每条需求都是可测试的吗？**
  - [ ] 2.5 问自己：**边界情况覆盖了吗？错误场景呢？**
  - [ ] 2.6 ⏸️ 确认节点 — 等待用户确认后继续

- [ ] **Phase 3: Design**（除非 `--skip-design`）
  - [ ] 3.1 Create `.spec-flow/active/<feature>/design.md` using `templates/design.md.template`
  - [ ] 3.2 包含：Architecture (Mermaid), Components, API, Data Model, Error Handling
  - [ ] 3.3 问自己：**这个设计能满足所有 requirements 吗？逐条对照**
  - [ ] 3.4 问自己：**有没有更简单的方案？过度设计了吗？**
  - [ ] 3.5 ⏸️ 确认节点 — 等待用户确认后继续

- [ ] **Phase 4: Tasks**
  - [ ] 4.1 Create `.spec-flow/active/<feature>/tasks.md` using `templates/tasks.md.template`
  - [ ] 4.2 Load `references/task-decomposition.md` — 遵循任务拆解规范
  - [ ] 4.3 每个任务：1-2 tool calls 可完成，标注复杂度 Low/Medium/High
  - [ ] 4.4 分组：Setup → Implementation → Testing → Documentation
  - [ ] 4.5 问自己：**任务之间的依赖关系对吗？有没有可以并行的？**
  - [ ] 4.6 ⏸️ 确认节点 — 等待用户确认后继续

- [ ] **Phase 5: Implementation**
  - [ ] 5.1 Load `references/execution-modes.md` — 确认执行模式
  - [ ] 5.2 默认 Step Mode（逐任务确认），用户可切换 Batch/Phase Mode
  - [ ] 5.3 每个任务执行前：读 tasks.md → 检查依赖 → 读 design.md
  - [ ] 5.4 每个任务执行后：更新 tasks.md 状态（`- [ ]` → `- [x]`）
  - [ ] 5.5 全部完成后：归档到 `.spec-flow/archive/`

---

## Directory Structure

```
.spec-flow/
├── steering/           # 全局项目上下文（可选）
│   ├── constitution.md
│   ├── product.md
│   ├── tech.md
│   └── structure.md
├── active/             # 进行中
│   └── <feature>/
│       ├── proposal.md
│       ├── requirements.md
│       ├── design.md
│       └── tasks.md
└── archive/            # 已完成
```

## Steering Documents (Optional)

| Document | Purpose | Template |
|----------|---------|----------|
| `constitution.md` | 项目治理原则 | `templates/steering/constitution.md.template` |
| `product.md` | 产品愿景、目标用户 | `templates/steering/product.md.template` |
| `tech.md` | 技术栈、约束 | `templates/steering/tech.md.template` |
| `structure.md` | 代码组织、命名规范 | `templates/steering/structure.md.template` |

## Phase Transitions

| From | To | Condition |
|------|-----|-----------|
| Proposal | Requirements | Proposal approved, questions resolved |
| Requirements | Design | Requirements complete, testable |
| Requirements | Tasks | `--skip-design`, simple feature |
| Design | Tasks | Design approved |
| Tasks | Implementation | Tasks confirmed |
| Implementation | Done | All tasks complete → archive |

## Compatibility

Works with any AI agent that supports Skills format: Claude Code, Blade, OpenClaw, Cursor, Windsurf, etc.
