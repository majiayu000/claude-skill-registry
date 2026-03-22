---
name: ccw-help
description: CCW command help system. Search, browse, recommend commands, skills, teams. Triggers "ccw-help", "ccw-issue".
allowed-tools: Read, Grep, Glob, AskUserQuestion
version: 8.0.0
---

# CCW-Help Skill

CCW 命令帮助系统，提供命令搜索、推荐、文档查看、Skill/Team 浏览功能。

## Trigger Conditions

- 关键词: "ccw-help", "ccw-issue", "帮助", "命令", "怎么用", "ccw 怎么用", "工作流", "skill", "team"
- 场景: 询问命令用法、搜索命令、请求下一步建议、询问任务应该用哪个工作流、浏览 Skill/Team 目录

## Operation Modes

### Mode 1: Command Search

**Triggers**: "搜索命令", "find command", "search"

**Process**:
1. Query `command.json` commands array
2. Filter by name, description, category
3. Present top 3-5 relevant commands

### Mode 2: Smart Recommendations

**Triggers**: "下一步", "what's next", "推荐"

**Process**:
1. Query command's `flow.next_steps` in `command.json`
2. Explain WHY each recommendation fits

### Mode 3: Documentation

**Triggers**: "怎么用", "how to use", "详情"

**Process**:
1. Locate command in `command.json`
2. Read source file via `source` path
3. Provide context-specific examples

### Mode 4: Beginner Onboarding

**Triggers**: "新手", "getting started", "常用命令"

**Process**:
1. Query `essential_commands` array
2. Guide appropriate workflow entry point

### Mode 5: CCW Command Orchestration

**Triggers**: "ccw ", "自动工作流", "自动选择工作流", "帮我规划"

**Process**:
1. Analyze user intent (task type, complexity, clarity)
2. Auto-select workflow level (1-4 or Issue)
3. Build command chain based on workflow
4. Get user confirmation
5. Execute chain with TODO tracking

**Supported Workflows** (参考 [ccw.md](../../commands/ccw.md)):
- **Level 1** (Lite-Lite-Lite): Ultra-simple quick tasks
- **Level 2** (Rapid/Hotfix): Bug fixes, simple features, documentation
- **Level 2.5** (Rapid-to-Issue): Bridge from quick planning to issue workflow
- **Level 3** (Coupled): Complex features with planning, execution, review, tests
- **Level 3 Variants**:
  - TDD workflows (test-first development)
  - Test-fix workflows (debug failing tests)
  - Review workflows (code review and fixes)
  - UI design workflows
  - Multi-CLI collaborative workflows
  - Cycle workflows (integration-test, refactor)
- **Level 4** (Full): Exploratory tasks with brainstorming
- **With-File Workflows**: Documented exploration with multi-CLI collaboration
  - `brainstorm-with-file`: Multi-perspective ideation → workflow-plan → workflow-execute
  - `debug-with-file`: Hypothesis-driven debugging (standalone)
  - `analyze-with-file`: Collaborative analysis → workflow-lite-plan
  - `collaborative-plan-with-file`: Multi-agent planning → unified-execute
  - `roadmap-with-file`: Strategic requirement roadmap → team-planex
- **Issue Workflow**: Batch issue discovery, planning, queueing, execution
- **Team Workflow**: team-planex wave pipeline for parallel execution

### Mode 6: Issue Reporting

**Triggers**: "ccw-issue", "报告 bug"

**Process**:
1. Use AskUserQuestion to gather context
2. Generate structured issue template

### Mode 7: Skill & Team Browsing

**Triggers**: "skill", "team", "技能", "团队", "有哪些 skill", "team 怎么用"

**Process**:
1. Query `command.json` skills array
2. Filter by category: workflow / team / review / meta / utility / standalone
3. Present categorized skill list with descriptions
4. For team skills, explain team architecture and usage patterns

## Data Source

Single source of truth: **[command.json](command.json)**

| Field | Purpose |
|-------|---------|
| `commands[]` | Flat command list with metadata |
| `commands[].flow` | Relationships (next_steps, prerequisites) |
| `agents[]` | Agent directory |
| `skills[]` | Skill directory with categories |
| `skills[].is_team` | Whether skill uses team architecture |
| `essential_commands[]` | Core commands list |

### Source Path Format

`source` 字段是相对路径（从 `skills/ccw-help/` 目录）：

```json
{
  "name": "lite-plan",
  "source": "../../../commands/workflow/lite-plan.md"
}
```

## Skill Catalog

### Workflow Skills (核心工作流)

| Skill | 内部流水线 | 触发词 |
|-------|-----------|--------|
| `workflow-lite-plan` | explore → plan → confirm → execute | "lite-plan", 快速任务 |
| `workflow-plan` | session → context → convention → gen → verify | "workflow-plan", 正式规划 |
| `workflow-execute` | session discovery → task processing → commit | "workflow-execute", 执行 |
| `workflow-tdd-plan` | 6-phase TDD plan → verify | "tdd-plan", TDD 开发 |
| `workflow-test-fix` | session → context → analysis → gen → cycle | "test-fix", 测试修复 |
| `workflow-multi-cli-plan` | ACE context → CLI discussion → plan → execute | "multi-cli", 多CLI协作 |
| `workflow-skill-designer` | Meta-skill for designing workflow skills | "skill-designer" |

### Team Skills (团队协作)

Team Skills 使用 `team-worker` agent 架构，Coordinator 编排流水线，Workers 是加载了 role-spec 的 `team-worker` agents。

| Skill | 用途 | 架构 |
|-------|------|------|
| `team-planex` | 规划+执行 wave pipeline | planner + executor, 适合清晰 issue/roadmap |
| `team-lifecycle` | 完整生命周期 (spec/impl/test) | team-worker agents with role-specs |
| `team-lifecycle-v4` | 优化版生命周期 | Optimized pipeline |
| `team-lifecycle-v3` | 基础版生命周期 | All roles invoke unified skill |
| `team-coordinate` | 通用动态团队协调 | 运行时动态生成 role-specs |
| `team-coordinate` | 通用团队协调 v1 | Dynamic role generation |
| `team-brainstorm` | 团队头脑风暴 | Multi-perspective analysis |
| `team-frontend` | 前端开发团队 | Frontend specialists |
| `team-issue` | Issue 解决团队 | Issue resolution pipeline |
| `team-iterdev` | 迭代开发团队 | Iterative development |
| `team-review` | 代码扫描/漏洞审查 | Scanning + vulnerability review |
| `team-roadmap-dev` | Roadmap 驱动开发 | Requirement → implementation |
| `team-tech-debt` | 技术债务清理 | Debt identification + cleanup |
| `team-testing` | 测试团队 | Test planning + execution |
| `team-quality-assurance` | QA 团队 | Quality assurance pipeline |
| `team-uidesign` | UI 设计团队 | Design system + prototyping |
| `team-ultra-analyze` | 深度协作分析 | Deep collaborative analysis |
| `team-executor` | 轻量执行 (恢复会话) | Resume existing sessions |
| `team-executor` | 轻量执行 v2 | Improved session resumption |

### Standalone Skills (独立技能)

| Skill | 用途 |
|-------|------|
| `brainstorm` | 双模头脑风暴 (auto pipeline / single role) |
| `review-code` | 多维度代码审查 |
| `review-cycle` | 审查+自动修复编排 |
| `spec-generator` | 6阶段规格文档链 (product-brief → PRD → architecture → epics) |
| `issue-manage` | 交互式 Issue 管理 (CRUD) |
| `memory-capture` | 统一记忆捕获 (session compact / quick tip) |
| `memory-manage` | 统一记忆管理 (CLAUDE.md + documentation) |
| `command-generator` | 命令文件生成器 |
| `skill-generator` | Meta-skill: 创建新 Skill |
| `skill-tuning` | Skill 诊断与优化 |

## Workflow Mapping (CCW Auto-Route)

CCW 根据任务意图自动选择工作流级别（参考 [ccw.md](../../commands/ccw.md)）：

| 输入示例 | 类型 | 级别 | 流水线 |
|---------|------|------|--------|
| "Add API endpoint" | feature (low) | 2 | workflow-lite-plan → workflow-test-fix |
| "Fix login timeout" | bugfix | 2 | workflow-lite-plan → workflow-test-fix |
| "协作分析: 认证架构" | analyze-file | 3 | analyze-with-file → workflow-lite-plan |
| "重构 auth 模块" | refactor | 3 | workflow:refactor-cycle |
| "multi-cli: API设计" | multi-cli | 3 | workflow-multi-cli-plan → workflow-test-fix |
| "头脑风暴: 通知系统" | brainstorm | 4 | brainstorm-with-file → workflow-plan → workflow-execute |
| "roadmap: OAuth + 2FA" | roadmap | 4 | roadmap-with-file → team-planex |
| "specification: 用户系统" | spec-driven | 4 | spec-generator → workflow-plan → workflow-execute |
| "team planex: 用户系统" | team-planex | Team | team-planex |

## Slash Commands

```bash
/ccw "task description"          # Auto-select workflow and execute
/ccw-help                        # General help entry
/ccw-help search <keyword>       # Search commands
/ccw-help next <command>         # Get next step suggestions
/ccw-help skills                 # Browse skill catalog
/ccw-help teams                  # Browse team skills
/ccw-issue                       # Issue reporting
```

### CCW Command Examples

```bash
/ccw "Add user authentication"          # → auto-select level 2-3
/ccw "Fix memory leak in WebSocket"     # → auto-select bugfix workflow
/ccw "Implement with TDD"               # → detect TDD, use tdd-plan → execute → tdd-verify
/ccw "头脑风暴: 用户通知系统"          # → detect brainstorm, use brainstorm-with-file
/ccw "深度调试: 系统随机崩溃"          # → detect debug-file, use debug-with-file
/ccw "协作分析: 认证架构设计"          # → detect analyze-file, use analyze-with-file
/ccw "roadmap: OAuth + 2FA 路线图"     # → roadmap-with-file → team-planex
/ccw "集成测试: 支付流程"              # → integration-test-cycle
/ccw "重构 auth 模块"                  # → refactor-cycle
```

## Maintenance

### Update Mechanism

CCW-Help skill supports manual updates through user confirmation dialog.
Script scans `commands/`, `agents/`, and `skills/` directories to regenerate all indexes.

#### How to Update

**Option 1: When executing the skill, user will be prompted:**

```
Would you like to update CCW-Help command index?
- Yes: Run auto-update and regenerate command.json
- No: Use current index
```

**Option 2: Manual update**

```bash
cd D:/Claude_dms3/.claude/skills/ccw-help
python scripts/auto-update.py
```

This runs `analyze_commands.py` to scan commands/, agents/, and skills/ directories and regenerate `command.json` + all index files.

#### Update Scripts

- **`auto-update.py`**: Simple wrapper that runs analyze_commands.py
- **`analyze_commands.py`**: Scans directories and generates command/agent/skill indexes

#### Generated Index Files

| File | Content |
|------|---------|
| `command.json` | Master index: commands + agents + skills |
| `index/all-commands.json` | Flat command list |
| `index/all-agents.json` | Agent directory |
| `index/all-skills.json` | Skill directory with metadata |
| `index/skills-by-category.json` | Skills grouped by category |
| `index/by-category.json` | Commands by category |
| `index/by-use-case.json` | Commands by usage scenario |
| `index/essential-commands.json` | Core commands for onboarding |
| `index/command-relationships.json` | Command flow relationships |

## Statistics

- **Commands**: 50+
- **Agents**: 22
- **Skills**: 36+ (7 workflow, 19 team, 10+ standalone/utility)
- **Workflows**: 6 main levels + 5 with-file variants + 2 cycle variants
- **Essential**: 10 core commands

## Core Principle

**智能整合，非模板复制**

- 理解用户具体情况
- 整合多个来源信息
- 定制示例和说明
