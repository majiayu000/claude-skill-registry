---
name: status
description: |
  Display concise project status including git state, latest commits, open issues, and active plans.
  TRIGGER when: user asks for project status, current state, what's happening, progress check, or "where are we".
  DO NOT TRIGGER when: user wants detailed overview (use /overview), or wants to start/finish issues.
version: "2.0.0"
---

# Status - Quick Project Status Check

Display structured project status in ~300 words across three time horizons:
- **Long-term/Global** (~100 words): Project purpose and goals
- **Mid-term** (~100 words): Recent 5 issues/features progress
- **Short-term/Current** (~100 words): Current/adjacent issue status and blockers

## Purpose

Provide layered context from strategic vision to tactical execution:
- **Global view**: What is this project fundamentally about?
- **Recent history**: What have we been working on? (last 5 issues)
- **Current focus**: What's happening right now? What's blocked?

**When to use**: Session start, context switch, or progress check.

**When NOT to use**: For detailed metrics and comprehensive reports, use `/overview` instead.

## Workflow

### 1. Gather Long-term Context

Read project overview from `CLAUDE.md` or `README.md`:
```bash
# Get project description (first paragraph or ## What Is This section)
head -50 CLAUDE.md | grep -A 10 "## 🎯 What Is This Project"
```

Extract: Purpose, tech stack, architecture pattern (≤100 words).

### 2. Gather Mid-term Context (Recent 5 Issues)

```bash
# Recently closed issues (last 3)
gh issue list --state closed --limit 3 --json number,title,closedAt

# Currently open issues (next 2-3)
gh issue list --state open --limit 3 --json number,title,labels
```

Focus on: What was completed recently? What's in progress? What's next?

### 3. Gather Short-term Context (Current Issue)

```bash
# Current branch (might indicate active issue)
git branch --show-current

# Working directory status
git status --short

# Active plans
ls .claude/plans/active/*.md 2>/dev/null

# Latest commits
git log --oneline -3
```

Identify: Current issue, previous issue, next issue, blockers.

### 4. Format Three-Layer Output (~300 words)

```markdown
📊 项目状态 (YYYY-MM-DD)

## 🎯 长期/全局 (~100 字)
**项目定位**: [本项目是干什么的 - 核心价值主张]

**技术架构**: [技术栈 profile + 核心 Pillars]
**主要目标**: [3-5 个核心功能模块/里程碑]
**当前阶段**: [Alpha/Beta/Production/Migration Phase X/Y]

## 📈 中期进展 - 最近 5 个 Issues (~100 字)
**已完成** (最近 2-3 个):
- ✅ #X: [Title] - [1-2 句关键成果]
- ✅ #Y: [Title] - [1-2 句关键成果]

**进行中/待开发** (接下来 2-3 个):
- 🔄 #A: [Title] - [当前状态/进度]
- ⏳ #B: [Title] - [优先级/依赖]
- ⏳ #C: [Title] - [优先级/依赖]

## 🎯 短期/当下 (~100 字)
**当前 Issue**: #X - [Title]
- 分支: [branch-name] | 工作区: [✅ 干净 | ⚠️ 有修改]
- 进度: [X/Y tasks 完成] | 活跃计划: [plan-name.md]
- 最新提交: [commit hash] - [message]

**前一个**: #Y - [Title] ([状态]: ✅ 完成 | ⚠️ 被阻塞)
**下一个**: #Z - [Title] (优先级: P0/P1/P2)

**当前问题/阻塞**: [如有] | **下一步**: [具体行动]
```

**Key constraints**:
- ~300 words total (100 per layer)
- Each layer serves different time horizon
- Global → Recent → Current (funnel view)
- Always include actionable next step

### 5. Present to User

Show formatted status report with emoji indicators for quick scanning.

## Output Format Rules

**Do**:
- Use emoji for visual scanning (✅ ⚠️ ❌ 📊 🎯)
- Show only top 3 items per category
- Include commit hashes for reference
- Suggest concrete next action

**Don't**:
- List all open issues (just top 3 priority)
- Include detailed file changes
- Show complete git log
- Repeat information from recent conversation

## Integration

**Quick check workflow**:
```
/status              # Get current state
/start-issue #X      # Start recommended issue
```

**After long break**:
```
/status              # See what's been done
/next                # Resume active work
```

**Before planning**:
```
/status              # Check current state
/plan "new feature"  # Plan next work
```

## Examples

### Example 1: AI Development Framework (ai-dev project)

**User**: "show me the project status"

**Output**:
```markdown
📊 项目状态 (2026-03-09)

## 🎯 长期/全局
**项目定位**: AI-assisted 开发框架 - 为 Claude Code 提供可复用的编码标准、工作流命令和技能系统

**技术架构**:
- Framework: 18 个 Pillars (编码标准) + 40+ Rules (快速参考)
- Skills: 20+ workflow commands + Python-only policy (ADR-003)

**主要目标**:
- ✅ 标准化编码模式 (Pillars A-R)
- 🔄 Bash-to-Python 迁移 (5 phases, 1182 lines)
- ⏳ CLI 工具和示例项目

**当前阶段**: Migration Phase 1/5 完成 (20%)

## 📈 中期进展 - 最近 5 个 Issues
**已完成**:
- ✅ #83: Phase 1 共享 Python 工具库 - 实现 git/fs/format utilities (562 行)，60+ 测试
- ✅ #82: Bash-to-Python 迁移总览 - 创建 5 个 phase issues，deadline 2026-03-22

**进行中/待开发**:
- ⏳ #84: Phase 2 - finish-issue 迁移 (28 lines Bash → Python)
- ⏳ #85: Phase 3 - overview 数据收集迁移 (465 lines)
- ⏳ #86: Phase 4 - overview 格式化迁移 (426 lines)

## 🎯 短期/当下
**当前 Issue**: 无 (刚完成 #83)
- 分支: main | 工作区: ✅ 干净
- 最新提交: 3f01e1a - feat: add /status skill

**前一个**: #83 - Shared utilities (✅ PR #88 已合并)
**下一个**: #84 - Migrate finish-issue (优先级: Phase 2)

**当前问题/阻塞**: 无 | **下一步**: `/start-issue #84` 开始 Phase 2
```

### Example 2: Active Development (with uncommitted changes)

**User**: "what's the current status?"

**Output**:
```markdown
📊 项目状态 (2026-03-09)

## 🎯 长期/全局
**项目定位**: AI-assisted 开发框架 - 为 Claude Code 提供可复用的编码标准、工作流命令和技能系统

**技术架构**: 18 Pillars + 40+ Rules + 20+ Skills | Python-only (ADR-003)
**主要目标**: Bash-to-Python 迁移 (5 phases, 1182 lines) + 标准化编码模式
**当前阶段**: Migration Phase 2/5 进行中 (40%)

## 📈 中期进展 - 最近 5 个 Issues
**已完成**:
- ✅ #83: 共享 Python 工具库 - 562 行实现 + 727 行测试
- ✅ #82: 迁移总览 issue 创建

**进行中/待开发**:
- 🔄 #84: finish-issue 迁移 - 进度 1/2 脚本完成 (check_tests.py ✅)
- ⏳ #85: overview 数据收集 (依赖 #84)
- ⏳ #86: overview 格式化 (依赖 #85)

## 🎯 短期/当下
**当前 Issue**: #84 - Migrate finish-issue scripts
- 分支: feature/84-migrate-finish-issue | 工作区: ⚠️ 有修改 (2 文件)
- 进度: 1/2 tasks (50%) | 活跃计划: issue-84-plan.md
- 最新提交: a1b2c3d - feat: create Python check_tests.py

**前一个**: #83 - Shared utilities (✅ 完成)
**下一个**: #85 - Overview data collection (P1, 依赖 #84)

**当前问题/阻塞**: check_sync.py 待实现 | **下一步**: 提交修改，继续实现 check_sync.py
```

## Performance

- **Execution time**: <10 seconds (3-layer structure)
- **Data sources**:
  - CLAUDE.md/README (project overview)
  - Git: 3-4 commands (branch, status, log)
  - GitHub API: 2 calls (closed + open issues)
  - File system: active plans check
- **Output size**: ~300 words (100 per layer)

Slightly slower than simple status but provides strategic context.

## Best Practices

1. **Three time horizons**: Always include all three layers (global → recent → current)
2. **Balanced length**: ~100 words per layer, ~300 words total
3. **Funnel view**: Broad context → recent history → current focus
4. **Actionable**: Every layer should inform decision-making
5. **Visual hierarchy**: Use emoji and markdown structure for quick scanning
6. **Context switching**: Run at session start or after long breaks
7. **Update global**: Refresh project overview when major milestones change

## Related Skills

- **/overview** - Detailed comprehensive report (use for deep analysis)
- **/next** - Get next task from active plan
- **/start-issue** - Begin work on recommended issue

---

**Version:** 2.0.0
**Last Updated:** 2026-03-09
**Changelog:**
- v2.0.0 (2026-03-09): Three-layer structure - long/mid/short-term planning
- v1.0.0 (Initial): Initial release - basic status display

**Pattern:** Simple (SKILL.md only, no scripts)
**Compliance:** ADR-001 ✅
