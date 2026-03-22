---
name: maintain-project
description: |
  Automated maintenance for project-specific content (CLAUDE.md skills list, plans/ cleanup, health reports).
  TRIGGER when: user wants to maintain project documentation ("maintain project", "clean up plans", "update CLAUDE.md skills", "project health check").
  DO NOT TRIGGER when: user wants framework sync (use /update-framework), or just wants to read documentation.
version: "1.0.0"
allowed-tools: Bash(ls *), Bash(find *), Bash(gh *), Bash(git *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Maintain Project - Automated Project Content Maintenance

自动维护项目特定内容，保持 AI 编码基础设施健康运行。

## Overview

**What it does:**
1. 同步 CLAUDE.md 技能列表（从 `.claude/skills/` 扫描已安装技能）
2. 清理 `.claude/plans/` 目录（归档已完成计划，删除废弃计划）
3. 生成项目健康报告（0-100 分数 + 可操作建议）

**Why it's needed:**
随着项目演进，AI 编码基础设施逐渐退化：
- CLAUDE.md 中的技能列表过时（新增技能未列出）
- .claude/plans/ 中积累大量已完成计划（占用空间）
- 文档与实际代码不一致（降低 AI 辅助效率）

This skill automates maintenance to keep project content fresh and accurate.

**When to use:**
- Monthly project maintenance routine
- After installing new skills (sync to CLAUDE.md)
- When .claude/plans/active/ becomes cluttered
- Before major releases (ensure documentation accuracy)
- After completing multiple issues (clean up plans)

## Scope Separation: maintain-project vs update-framework

**Critical distinction:**

| Aspect | /maintain-project | /update-framework |
|--------|-------------------|-------------------|
| **Layer** | 项目层（Project Layer） | 框架层（Framework Layer） |
| **What** | CLAUDE.md, docs/, plans/, ADRs | skills, rules, workflow, pillars |
| **Why** | 维护项目特定内容 | 同步框架组件 |
| **When** | 项目演进后维护 | 框架升级时同步 |
| **Scope** | 当前项目内容 | 跨项目框架 |

**Example:**
```bash
# 项目层维护（本技能）
/maintain-project                # 更新 CLAUDE.md 技能列表
/maintain-project --component plans  # 清理 plans/

# 框架层同步（update-framework）
/update-framework --from ~/dev/ai-dev  # 同步框架组件
```

**No overlap:**
- maintain-project NEVER modifies `.claude/skills/`, `.claude/rules/`, `.prot/pillars/`
- update-framework NEVER modifies `CLAUDE.md`, `docs/`, `.claude/plans/`

## Core Modules (5)

### 1. CLAUDE.md Maintenance (Phase 1: MVP ✅)

**功能：自动同步技能列表**

**检测项：**
- 新增技能未列出（需要添加到 CLAUDE.md）
- 已删除技能仍列出（需要从 CLAUDE.md 移除）
- 技能描述不一致（需要同步）
- 版本号不匹配（需要更新）

**工作流：**
```
1. 扫描 .claude/skills/ 获取已安装技能
2. 解析 CLAUDE.md 当前技能列表
3. 检测差异（新增/删除/版本不匹配）
4. 自动更新 CLAUDE.md 技能表格
5. 保持分类结构（Issue Lifecycle, Planning, Quality 等）
```

**示例输出：**
```
CLAUDE.md Skills Sync
=====================
✅ Scanned 20 installed skills
✅ Found 2 new skills not documented:
   - maintain-project v1.0.0 (Project Maintenance)
   - sync-docs v1.1.0 (Documentation)

✅ Found 1 removed skill still documented:
   - old-skill (deprecated)

✅ Updated CLAUDE.md skills table
```

### 2. docs/ Content Maintenance (Phase 2: Future)

**功能：验证文档内容准确性**

**检测项：**
- 代码示例过时（与实际代码不匹配）
- 链接失效（404 或文件不存在）
- API 文档与实现不一致
- 配置说明过期

**工作流：**
```
1. 读取 DOCUMENTATION_MANUAL.md（文档标准）
2. 扫描 docs/ 下所有 Markdown 文件
3. 提取代码块并验证（对比实际源码）
4. 检测内部链接有效性
5. 生成过时内容报告
```

**Note:** Phase 2 implementation, not included in MVP.

### 3. plans/ Cleanup (Phase 1: MVP ✅)

**功能：清理计划目录**

**归档已完成计划：**
```bash
# 检测 issue 状态
for plan in .claude/plans/active/*.md; do
    issue_num=$(grep -oP 'Issue #\K\d+' "$plan" | head -1)

    # 检查 issue 是否已关闭
    if gh issue view "$issue_num" --json state | grep -q "CLOSED"; then
        mv "$plan" .claude/plans/archived/
    fi
done
```

**删除废弃计划：**
```bash
# 超过 30 天的已关闭 issue 计划
for plan in .claude/plans/archived/*.md; do
    issue_num=$(extract_issue_number "$plan")
    closed_date=$(gh issue view "$issue_num" --json closedAt -q .closedAt)

    if days_since "$closed_date" > 30; then
        rm "$plan"
    fi
done
```

**保持整洁：**
- 只保留当前活跃 issue 的计划在 active/
- 已完成的移到 archived/
- 长时间未活动的删除

**示例输出：**
```
Plans Cleanup
=============
✅ Found 5 completed plans in active/
✅ Moved 5 plans to archived/
✅ Deleted 2 plans (closed > 30 days ago)

Before: 12 files in active/
After:  5 files in active/ (optimal)
```

### 4. ADRs Maintenance (Phase 2: Future)

**功能：维护 ADR 状态和索引**

**检测项：**
- ADR 状态未更新（Proposed → Accepted → Superseded）
- 索引文件过时（README.md 未包含新 ADR）
- 编号跳跃（缺失 ADR 编号）
- 状态不一致（文件名 vs 内容）

**工作流：**
```
1. 扫描 docs/ADRs/ 获取所有 ADR
2. 检测编号连续性
3. 解析每个 ADR 的状态字段
4. 更新 docs/ADRs/README.md 索引
5. 生成状态报告
```

**Note:** Phase 2 implementation, not included in MVP.

### 5. Health Report (Phase 1: MVP ✅)

**功能：生成项目健康评分**

**评分计算：**
```python
def calculate_health_score():
    scores = {
        "claude_md": check_claude_md_health(),    # 0-100
        "plans": check_plans_cleanliness(),       # 0-100
        "overall": 0
    }

    # 加权平均（Phase 1: 仅 2 个组件）
    scores["overall"] = (scores["claude_md"] * 0.5 +
                        scores["plans"] * 0.5)

    return scores

def check_claude_md_health():
    installed = scan_skills_directory(".claude/skills/")
    documented = parse_skills_section("CLAUDE.md")

    # 计算匹配率
    match_rate = len(installed & documented) / len(installed)
    return int(match_rate * 100)

def check_plans_cleanliness():
    active_plans = count_files(".claude/plans/active/")

    # 检查有多少应该归档
    should_archive = count_completed_plans()

    # 清洁度 = (总数 - 应归档) / 总数
    cleanliness = (active_plans - should_archive) / active_plans if active_plans > 0 else 1.0
    return int(cleanliness * 100)
```

**报告格式：**
```
Project Health Report
=====================

Overall Health: 85/100 ✅

Component Health:
- CLAUDE.md: 90/100 ✅
  - 2 new skills not documented
  - Skills section 90% accurate

- plans/: 80/100 ⚠️
  - 5 completed plans should be archived
  - active/ directory: 12 files (optimal: 5)

Recommendations:
1. Update CLAUDE.md skills list (2 additions)
2. Archive 5 completed plans
3. Run /maintain-project to auto-fix
```

## AI Execution Instructions

**CRITICAL: Task creation and component execution**

When executing `/maintain-project`, AI MUST follow this workflow:

### Step 1: Create 5 Subtasks (MVP)

```python
# Create all tasks at the start
tasks = {
    "validate": TaskCreate(
        subject="Validate project structure",
        description="Verify .claude/, CLAUDE.md, plans/ exist",
        activeForm="Validating project..."
    ),
    "claude_md": TaskCreate(
        subject="Sync CLAUDE.md skills list",
        description="Scan .claude/skills/ and update CLAUDE.md",
        activeForm="Syncing CLAUDE.md..."
    ),
    "plans": TaskCreate(
        subject="Clean up plans/ directory",
        description="Archive completed, delete abandoned",
        activeForm="Cleaning plans/..."
    ),
    "health": TaskCreate(
        subject="Generate health report",
        description="Calculate scores and recommendations",
        activeForm="Calculating health..."
    ),
    "summary": TaskCreate(
        subject="Report comprehensive summary",
        description="Display results and next steps",
        activeForm="Generating summary..."
    )
}
```

### Step 2: Execute with Status Updates

```python
# Validation
TaskUpdate(tasks["validate"], "in_progress")
validate_project_structure()
TaskUpdate(tasks["validate"], "completed")

# CLAUDE.md sync (unless --component specified)
if component in [None, "claude-md"]:
    TaskUpdate(tasks["claude_md"], "in_progress")
    sync_claude_md_skills()
    TaskUpdate(tasks["claude_md"], "completed")

# Plans cleanup (unless --component specified)
if component in [None, "plans"]:
    TaskUpdate(tasks["plans"], "in_progress")
    cleanup_plans_directory()
    TaskUpdate(tasks["plans"], "completed")

# Health report (always run unless --report-only)
TaskUpdate(tasks["health"], "in_progress")
health = generate_health_report()
TaskUpdate(tasks["health"], "completed")

# Summary
TaskUpdate(tasks["summary"], "in_progress")
print_summary(health)
TaskUpdate(tasks["summary"], "completed")
```

### Step 3: Component-Specific Execution

**CLAUDE.md sync implementation:**
```python
def sync_claude_md_skills():
    # 1. 扫描已安装技能
    installed_skills = []
    for skill_dir in glob(".claude/skills/*/"):
        skill_md = f"{skill_dir}/SKILL.md"
        if exists(skill_md):
            # 解析 YAML frontmatter
            metadata = parse_yaml_frontmatter(skill_md)
            installed_skills.append({
                "name": metadata["name"],
                "version": metadata.get("version", "unknown"),
                "description": metadata.get("description", "").split("\n")[0]
            })

    # 2. 解析 CLAUDE.md 当前技能列表
    current_skills = parse_skills_table_from_claude_md()

    # 3. 检测差异
    installed_names = {s["name"] for s in installed_skills}
    current_names = {s["name"] for s in current_skills}

    added = installed_names - current_names
    removed = current_names - installed_names

    # 4. 更新 CLAUDE.md
    if added or removed:
        update_skills_section("CLAUDE.md", installed_skills)
        print(f"✅ Updated CLAUDE.md: +{len(added)}, -{len(removed)}")
    else:
        print("✅ CLAUDE.md skills list is up to date")
```

**Plans cleanup implementation:**
```python
def cleanup_plans_directory():
    active_dir = ".claude/plans/active/"
    archived_dir = ".claude/plans/archived/"

    # 确保 archived/ 目录存在
    os.makedirs(archived_dir, exist_ok=True)

    # 1. 归档已完成计划
    archived_count = 0
    for plan_file in glob(f"{active_dir}/*.md"):
        # 提取 issue 编号
        content = read_file(plan_file)
        match = re.search(r'Issue #(\d+)', content)
        if not match:
            continue

        issue_num = match.group(1)

        # 检查 issue 状态
        result = run_command(f"gh issue view {issue_num} --json state -q .state")
        if result.strip() == "CLOSED":
            # 移动到 archived/
            shutil.move(plan_file, archived_dir)
            archived_count += 1

    # 2. 删除超过 30 天的归档计划（可选）
    deleted_count = 0
    for plan_file in glob(f"{archived_dir}/*.md"):
        content = read_file(plan_file)
        match = re.search(r'Issue #(\d+)', content)
        if not match:
            continue

        issue_num = match.group(1)

        # 获取关闭日期
        result = run_command(f"gh issue view {issue_num} --json closedAt -q .closedAt")
        if result.strip():
            closed_date = datetime.fromisoformat(result.strip().rstrip('Z'))
            days_ago = (datetime.now() - closed_date).days

            if days_ago > 30:
                os.remove(plan_file)
                deleted_count += 1

    print(f"✅ Plans cleanup: {archived_count} archived, {deleted_count} deleted")
```

**Health report implementation:**
```python
def generate_health_report():
    # CLAUDE.md 健康评分
    installed = scan_skills_directory(".claude/skills/")
    documented = parse_skills_section("CLAUDE.md")

    claude_md_match_rate = len(installed & documented) / len(installed) if installed else 1.0
    claude_md_score = int(claude_md_match_rate * 100)

    # Plans 清洁度评分
    active_plans = count_files(".claude/plans/active/")
    should_archive = count_completed_plans()

    plans_cleanliness = (active_plans - should_archive) / active_plans if active_plans > 0 else 1.0
    plans_score = int(plans_cleanliness * 100)

    # 整体评分（加权平均）
    overall_score = int((claude_md_score * 0.5 + plans_score * 0.5))

    return {
        "overall": overall_score,
        "claude_md": {
            "score": claude_md_score,
            "issues": list(installed - documented),
        },
        "plans": {
            "score": plans_score,
            "should_archive": should_archive,
            "active_count": active_plans
        }
    }
```

## Workflow Steps (9 Tasks)

**Phase 1: MVP Implementation**

1. ✅ **Create skill structure** (Task 1)
   - `.claude/skills/maintain-project/SKILL.md`
   - `.claude/skills/maintain-project/LICENSE.txt`
   - Follow ADR-001 official patterns

2. ✅ **Implement CLAUDE.md skills sync** (Task 2)
   - Scan `.claude/skills/` directory
   - Parse CLAUDE.md skills table
   - Detect differences (new/removed/updated)
   - Update CLAUDE.md automatically

3. ✅ **Implement plans/ cleanup** (Task 3)
   - Archive completed plans (check GitHub issue status)
   - Delete abandoned plans (closed > 30 days)
   - Keep active/ directory clean

4. ✅ **Implement health report** (Task 4)
   - Calculate component scores (0-100)
   - Generate overall health score
   - Provide actionable recommendations

5. ✅ **Add CLI interface** (Task 5)
   - `--dry-run` - Preview mode
   - `--component <name>` - Run specific component
   - `--report-only` - Health report only
   - `--verbose` - Detailed logging

6. ✅ **Write documentation** (Task 6)
   - Complete SKILL.md (this file)
   - Usage examples
   - Error handling guide
   - Integration with /update-framework

7. ⏳ **Create evaluation tests** (Task 7)
   - Test CLAUDE.md sync
   - Test plans cleanup
   - Test health report
   - Test dry-run mode

8. ⏳ **Update CLAUDE.md** (Task 8)
   - Add maintain-project to skills table
   - Add use case example
   - Document integration

9. ⏳ **Integration testing** (Task 9)
   - Test in real project (buffer)
   - Verify no framework files modified
   - Verify accurate health scores
   - Document results

## Arguments

```bash
/maintain-project                    # 完整维护（CLAUDE.md + plans/ + health report）
/maintain-project --dry-run          # 预览模式（不做修改，仅显示将执行的操作）
/maintain-project --component claude-md  # 仅同步 CLAUDE.md
/maintain-project --component plans      # 仅清理 plans/
/maintain-project --report-only      # 仅生成健康报告（不做修改）
/maintain-project --verbose          # 显示详细日志
```

**参数说明：**

| Argument | Description | Example |
|----------|-------------|---------|
| `--dry-run` | 预览模式，不做任何修改 | `--dry-run` |
| `--component <name>` | 仅运行指定组件（claude-md, plans） | `--component plans` |
| `--report-only` | 仅生成健康报告 | `--report-only` |
| `--verbose` | 显示详细执行日志 | `--verbose` |

**组件名称：**
- `claude-md` - CLAUDE.md 技能列表同步
- `plans` - plans/ 目录清理

**Phase 2 (未来):**
- `docs` - docs/ 内容验证
- `adrs` - ADRs 维护

## Usage Examples

### Example 1: Monthly Maintenance (Recommended)

**User says:**
> "maintain project"

**What happens:**

```
🚀 Starting project maintenance...

Task Progress:
✅ Task 1/5: Validate project structure
✅ Task 2/5: Sync CLAUDE.md skills list
   - Found 2 new skills: maintain-project, sync-docs
   - Updated CLAUDE.md skills table
✅ Task 3/5: Clean up plans/ directory
   - Archived 5 completed plans
   - Deleted 2 abandoned plans
✅ Task 4/5: Generate health report
✅ Task 5/5: Report summary

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Health: 95/100 ✅

Component Health:
- CLAUDE.md: 100/100 ✅
  - All skills documented
  - Versions up to date

- plans/: 90/100 ✅
  - active/ directory: 5 files (optimal)
  - 0 plans need archiving

Recommendations:
✅ No issues found - project is healthy!

Summary:
- CLAUDE.md: 2 skills added
- plans/: 5 archived, 2 deleted
- Health: 82/100 → 95/100 (+13 points)

Time: 8 seconds
```

### Example 2: Preview Changes (Dry Run)

**User says:**
> "show me what maintain-project would do"

**What happens:**

```
/maintain-project --dry-run

🔍 Preview Mode (no changes will be made)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLAUDE.md Sync Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would add 2 skills:
  - maintain-project v1.0.0 (Project Maintenance)
  - sync-docs v1.1.0 (Documentation)

Would remove 1 skill:
  - old-skill (deprecated)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Plans Cleanup Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would archive 5 plans:
  - issue-123-plan.md (closed 2 days ago)
  - issue-124-plan.md (closed 5 days ago)
  - issue-125-plan.md (closed 7 days ago)
  - issue-126-plan.md (closed 10 days ago)
  - issue-127-plan.md (closed 12 days ago)

Would delete 2 abandoned plans:
  - issue-100-plan.md (closed 45 days ago)
  - issue-101-plan.md (closed 60 days ago)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current Health: 82/100 ⚠️
After Fix: 95/100 ✅ (+13 points)

Run without --dry-run to apply changes.
```

### Example 3: CLAUDE.md Sync Only

**User says:**
> "update CLAUDE.md skills list"

**What happens:**

```
/maintain-project --component claude-md

✅ Scanning .claude/skills/ directory...
✅ Found 20 installed skills
✅ Parsing CLAUDE.md current skills table...
✅ Found 18 documented skills

Differences:
  + maintain-project v1.0.0 (new)
  + sync-docs v1.1.0 (new)

✅ Updated CLAUDE.md skills table

Health: CLAUDE.md 90/100 → 100/100 ✅

Time: 3 seconds
```

### Example 4: Plans Cleanup Only

**User says:**
> "clean up plans directory"

**What happens:**

```
/maintain-project --component plans

✅ Scanning .claude/plans/active/...
✅ Found 12 active plans

Checking GitHub issue status...
  - Issue #123: CLOSED → archive
  - Issue #124: CLOSED → archive
  - Issue #125: OPEN → keep
  - Issue #126: CLOSED → archive
  - ...

✅ Archived 5 completed plans
✅ Deleted 2 abandoned plans (closed > 30 days)

Before: 12 files in active/
After:  5 files in active/ ✅

Health: plans/ 70/100 → 90/100 (+20 points)

Time: 5 seconds
```

### Example 5: Health Report Only

**User says:**
> "check project health"

**What happens:**

```
/maintain-project --report-only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project Health Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Health: 82/100 ⚠️

Component Health:
- CLAUDE.md: 90/100 ✅
  - 2 new skills not documented
  - Skills section 90% accurate

- plans/: 75/100 ⚠️
  - 5 completed plans should be archived
  - 2 abandoned plans detected
  - active/ directory: 12 files (optimal: 5)

Recommendations:
1. Run /maintain-project --component claude-md (adds 2 skills)
2. Run /maintain-project --component plans (archives 5, deletes 2)
3. Or run /maintain-project to fix all issues

Estimated improvement: 82/100 → 95/100 (+13 points)

Time: 2 seconds
```

## Error Handling

### Missing Project Structure

```
❌ Error: Invalid project structure

Missing required components:
- .claude/ directory not found
- CLAUDE.md not found

Please ensure this is a valid ai-dev project.
```

### No GitHub CLI Access

```
❌ Error: GitHub CLI not available

Plans cleanup requires GitHub CLI (gh) to check issue status.

Install: brew install gh
Login: gh auth login

Or skip plans cleanup: /maintain-project --component claude-md
```

### No Changes Needed

```
✅ Project is already healthy!

Current Health: 100/100 ✅

Component Status:
- CLAUDE.md: 100/100 ✅ (all skills documented)
- plans/: 100/100 ✅ (active/ directory clean)

No maintenance actions needed.
```

### Dry Run Mode

```
🔍 Dry Run Mode (no changes will be made)

Preview:
- Would add 2 skills to CLAUDE.md
- Would archive 5 plans
- Would delete 2 abandoned plans

Run without --dry-run to apply changes.
```

## Integration with /update-framework

**Clear separation of concerns:**

```bash
# 步骤 1: 更新框架组件（框架层）
/update-framework --from ~/dev/ai-dev
# → 同步 skills, rules, workflow, pillars

# 步骤 2: 维护项目内容（项目层）
/maintain-project
# → 更新 CLAUDE.md, 清理 plans/, 生成健康报告
```

**Recommended workflow:**

```bash
# Monthly routine
cd ~/projects/my-app

# 1. 拉取框架更新
/update-framework --from ~/dev/ai-dev --dry-run  # 预览
/update-framework --from ~/dev/ai-dev             # 执行

# 2. 维护项目内容
/maintain-project --report-only                   # 检查健康
/maintain-project                                 # 修复问题

# 3. 提交更新
git add CLAUDE.md .claude/plans/
git commit -m "chore: monthly framework update + project maintenance"
```

**No overlap:**
- `/update-framework` 修改：`.claude/skills/`, `.claude/rules/`, `.prot/pillars/`, `.claude/workflow/`
- `/maintain-project` 修改：`CLAUDE.md`, `.claude/plans/active/`, `.claude/plans/archived/`

## Performance

**Expected execution time:**

| Operation | Time | Notes |
|-----------|------|-------|
| Full maintenance | 5-10s | CLAUDE.md + plans + health |
| CLAUDE.md only | 2-3s | Scan + parse + update |
| Plans only | 3-5s | Check GitHub issues |
| Health report only | 1-2s | Calculate scores |
| Dry run | 3-5s | No modifications |

**Scalability:**

| Project Size | Skills Count | Plans Count | Time |
|-------------|--------------|-------------|------|
| Small | 10 | 5 | 3s |
| Medium | 20 | 15 | 6s |
| Large | 30 | 30 | 10s |

**Optimization:**
- Parallel GitHub API calls for plan status checks
- Cache installed skills list during execution
- Skip unchanged files in CLAUDE.md sync

## Best Practices

1. **定期维护（推荐每月）：**
```bash
# Monthly routine
/maintain-project --report-only  # 先检查健康
/maintain-project                # 修复问题
```

2. **新增技能后立即同步：**
```bash
# 安装新技能
/update-skills --from ~/dev/ai-dev --skills maintain-project

# 同步到 CLAUDE.md
/maintain-project --component claude-md
```

3. **完成多个 issue 后清理：**
```bash
# 关闭多个 issue 后
/maintain-project --component plans
```

4. **大型变更前预览：**
```bash
/maintain-project --dry-run
# 确认无误后执行
/maintain-project
```

5. **与框架更新配合：**
```bash
# 框架更新后立即维护
/update-framework --from ~/dev/ai-dev
/maintain-project
```

## Task Management

**After each maintenance step**, update progress:

```
Project validated → Update Task #1
CLAUDE.md synced → Update Task #2
Plans cleaned → Update Task #3
Health calculated → Update Task #4
Summary reported → Update Task #5
```

Provides real-time visibility of maintenance progress.

## Final Verification

**Before declaring maintenance complete**, verify:

```
- [ ] All 5 tasks completed
- [ ] CLAUDE.md skills list accurate
- [ ] plans/active/ contains only active plans
- [ ] plans/archived/ contains completed plans
- [ ] Health score calculated
- [ ] No framework files modified (.claude/skills/, .claude/rules/)
- [ ] Recommendations provided
```

Missing items indicate incomplete maintenance.

## Related Skills

**Project Layer (complementary):**
- **/check-docs** - Validate docs/ structure
- **/init-docs** - Create initial docs/ structure
- **/adr** - Manage Architecture Decision Records

**Framework Layer (separate):**
- **/update-framework** - Sync framework components (meta-skill)
- **/update-skills** - Sync skills only
- **/update-rules** - Sync rules only
- **/update-workflow** - Sync workflow docs only
- **/update-pillars** - Sync pillars only

**Workflow Integration:**
- **/work-issue** - Uses maintain-project after issue completion
- **/finish-issue** - May trigger maintain-project for cleanup

---

**Version:** 1.0.0
**Last Updated:** 2026-03-15
**Changelog:**
- v1.0.0 (2026-03-15): Initial release - project maintenance and cleanup skill
**Phase:** 1 (MVP - CLAUDE.md, plans/, health)
**Pattern:** Workflow Skill (project maintenance automation)
**Compliance:** ADR-001 ✅
