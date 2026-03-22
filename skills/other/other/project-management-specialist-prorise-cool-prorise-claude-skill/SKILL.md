---
description: 提供项目管理、任务跟踪、团队协调和项目交付能力。当需要管理项目、跟踪进度或协调团队时使用。
name: project-management-specialist
---
# Project Management Specialist

提供项目管理、任务跟踪、团队协调和项目交付能力。当需要管理项目、跟踪进度或协调团队时使用。

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

#### experiment-tracker (1)
- `experiment-tracker`
  - 触发语义: Expert project manager specializing in experiment design, execution tracking, and data-driven decision making. Focused on managing A/B tests, feature experiments, and hypothesis validation through systematic experimentation and rigorous analysis.
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/experiment-tracker/SKILL.md`

#### issue-lifecycle (1)
- `issue-manage`
  - 触发语义: Interactive issue management with menu-driven CRUD operations. Use when managing issues, viewing issue status, editing issue fields, performing bulk operations, or viewing issue history. Triggers on "manage issue", "list issues", "edit issue", "delete issue", "bulk update", "issue dashboard", "issue history", "completed issues".
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/issue-lifecycle/SKILL.md`

#### jira-workflow-steward (1)
- `jira-workflow-steward`
  - 触发语义: Expert delivery operations specialist who enforces Jira-linked Git workflows, traceable commits, structured pull requests, and release-safe branch strategy across software teams.
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/jira-workflow-steward/SKILL.md`

#### meeting-intelligence (1)
- `meeting-insights-analyzer`
  - 触发语义: 分析会议记录和录音，以发现行为模式、沟通洞察和可行的反馈。识别您何时避免冲突、使用填充词、主导对话或错过倾听的机会。非常适合寻求提高沟通和领导技能的专业人士。
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/meeting-intelligence/SKILL.md`

#### project-manager-senior (1)
- `senior-project-manager`
  - 触发语义: Converts specs to tasks and remembers previous projects. Focused on realistic scope, no background processes, exact spec requirements
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/project-manager-senior/SKILL.md`

#### project-shepherd (1)
- `project-shepherd`
  - 触发语义: Expert project manager specializing in cross-functional project coordination, timeline management, and stakeholder alignment. Focused on shepherding projects from conception to completion while managing resources, risks, and communications across multiple teams and departments.
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/project-shepherd/SKILL.md`

#### studio-operations (1)
- `studio-operations`
  - 触发语义: Expert operations manager specializing in day-to-day studio efficiency, process optimization, and resource coordination. Focused on ensuring smooth operations, maintaining productivity standards, and supporting all teams with the tools and processes needed for success.
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/studio-operations/SKILL.md`

#### studio-producer (1)
- `studio-producer`
  - 触发语义: Senior strategic leader specializing in high-level creative and technical project orchestration, resource allocation, and multi-project portfolio management. Focused on aligning creative vision with business objectives while managing complex cross-functional initiatives and ensuring optimal studio operations.
  - 入口文件: `.claude/skills/project-management-specialist/references/domains/studio-producer/SKILL.md`

<!-- AUTO-GENERATED-SKILL-INDEX:END -->

## Notes

- 顶层 `SKILL.md` 仅做索引导航，不承载大体量细节内容。
- 详细资料下沉到 `references/domains/`，按树形结构组织。
