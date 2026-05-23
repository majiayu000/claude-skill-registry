---
name: update-skills
description: |
  Sync skills between projects - bidirectional copy with version detection and clean mode.
  TRIGGER when: user wants to sync skills ("update skills from X", "sync skills", "pull skills from framework", "push skills to project"), or wants complete directory replacement ("clean sync", "reset skills").
  DO NOT TRIGGER when: user wants to update pillars/rules/workflow (use respective update-* skills), or just wants to read skill docs.
version: "2.4.0"
allowed-tools: Bash(cp *), Bash(mkdir *), Bash(ls *), Bash(find *), Bash(test *), Bash(cat *), Bash(wc *), Bash(stat *), Bash(git *), Read, Write, Glob, Grep, Edit
disable-model-invocation: false
user-invocable: true
---

# Update Skills - Skills Synchronization

Sync skill files between projects bidirectionally with smart version detection and conflict handling.

## Overview

This skill synchronizes skills (.claude/skills/) between projects:

**What it does:**
1. Scans source and target projects for skills
2. Compares skills to detect new/updated/conflicted versions
3. Shows detailed diff preview with line counts
4. Syncs skills with confirmation
5. Supports selective skill filtering
6. Creates backups before overwriting
7. Reports what was synced

**Why it's needed:**
Skills evolve across projects. Framework updates need to propagate, and project innovations should flow back. This skill automates bidirectional skill sync with version conflict detection and backup protection.

**When to use:**
- Monthly framework upgrades
- Promoting project skills to framework
- Cross-project skill sharing
- Initial project setup

## Workflow

### Step 1: Create Todo List

**Initialize sync tracking** using TaskCreate:

```
Task #1: Validate source and target paths
Task #2: Scan skills in both projects (blocked by #1)
Task #3: Compare and detect versions (blocked by #2)
Task #4: Show diff preview (blocked by #3)
Task #5: Execute sync with confirmation (blocked by #4)
Task #6: Report sync results (blocked by #5)
```

After creating tasks, proceed with sync execution.

## Sync Modes

### 1. Pull Skills (--from)

Pull skills from source project to current project:

```bash
/update-skills --from ~/dev/ai-dev
/update-skills --from ~/dev/ai-dev --dry-run
/update-skills --from ~/dev/ai-dev --skills adr,status,review
```

**What happens:**
1. Scan source: `<source>/.claude/skills/`
2. Scan current: `.claude/skills/`
3. Compare modification times and sizes
4. Detect: NEW, NEWER, OLDER, CONFLICT, SAME
5. Show analysis table
6. Confirm and copy updated skills

### 2. Push Skills (--to)

Push skills from current project to target project:

```bash
/update-skills --to ~/projects/my-app
/update-skills --to ~/projects/my-app --dry-run
/update-skills --to ~/projects/my-app --skills create-issues,start-issue,finish-issue
```

**What happens:**
1. Scan current project skills
2. Scan target project skills
3. Compare versions
4. Show what will be pushed
5. Confirm and copy to target

### 3. Dry Run Mode (--dry-run)

Preview changes without applying:

```bash
/update-skills --from ~/dev/ai-dev --dry-run
```

**Output:**
- Shows analysis table with versions
- Reports what would be synced
- No confirmation required
- No actual changes made

### 4. Selective Sync (--skills)

Sync only specific skills:

```bash
/update-skills --from ~/dev/ai-dev --skills adr,status
/update-skills --to ~/projects/my-app --skills custom-deploy,custom-test
```

**Skill selection:**
- Comma-separated list
- Only syncs specified skills
- Ignores others

### 5. Smart Filter (--filter-config) - NEW

Apply intelligent filtering based on tech stack configuration:

```bash
# Used by /update-framework meta-skill
/update-skills --from ~/dev/ai-dev --filter-config <target>/.claude/framework-config.json
```

**What it does:**
1. Reads filter config from `.claude/framework-config.json`
2. Applies exclude list for skills not relevant to tech stack
3. Shows filter summary in analysis

**Filter Configuration Format:**

```json
{
  "filterConfig": {
    "skills": {
      "include": ["*"],  // Usually sync all skills
      "exclude": []      // Rarely exclude skills
    }
  }
}
```

**Filter Logic:**

```
For each skill directory:
1. Check if skill name in exclude list
   → Skip if excluded
2. Apply normal NEW/NEWER/SAME logic
```

**Example - Minimal Project:**

Without filter: 16 skills synced
With filter (exclude deployment skills): ~14 skills synced

```
📋 Smart Filter Active
⏭️  Excluding: deploy-prod (deployment skill)
⏭️  Excluding: hotfix (deployment skill)

Result: 14 skills synced (2 excluded)
```

**Note:**
- Skills are usually synced completely (no filtering)
- Filtering mainly used for specialized deployment skills
- Typically called by `/update-framework` meta-skill

### 6. Clean Mode (--clean) - NEW in v2.3.0

**IMPORTANT**: Destructive operation with complete directory replacement.

Complete clean slate - delete entire target `.claude/skills` directory and replace with source:

```bash
# Execute full replacement
/update-skills --from ~/dev/ai-dev --clean
/update-skills --to ~/projects/my-app --clean
```

**What it does:**
1. **Deletes** target directory completely
2. **Copies** all skills from source
3. **Reports** results

**Use Cases:**
- Version conflicts too complex to resolve manually
- Target skills corrupted or inconsistent
- Force align target to source state
- Clean up residual skills after major version upgrade

**Example Output:**

```
🗑️  Deleting .claude/skills (34 skills)
📋 Copying from ~/dev/ai-dev/.claude/skills (22 skills)

✅ Clean sync complete: 22 skills synced
```

**Mutual Exclusion Rules:**

| Parameter Combination | Behavior | Valid? |
|----------------------|----------|--------|
| `--from --clean` | Clean current, copy from source | ✅ Valid |
| `--to --clean` | Clean target, copy from current | ✅ Valid |
| `--clean --skills` | **ERROR** | ❌ Mutually exclusive |
| `--clean --filter-config` | **ERROR** | ❌ Mutually exclusive |

**Error handling:**
```bash
$ /update-skills --from ~/dev/ai-dev --clean --skills adr,status

❌ Error: --clean and --skills are mutually exclusive
   --clean performs full directory replacement
```

**When NOT to use:**
- ❌ Normal version updates → Use standard sync (--from/--to)
- ❌ Selective skill updates → Use --skills flag
- ❌ Regular maintenance → Use smart filter (--filter-config)

**When to use:**
- ✅ Severe version conflicts (manual resolution too complex)
- ✅ Corrupted target skills directory
- ✅ Force reset to framework state
- ✅ Major version migration cleanup

**Recovery:**
If you need to restore after clean sync, use git:
```bash
# Restore deleted files
git restore .claude/skills/

# Or check changes
git status
git diff
```

## Version Detection (v2.0.0+)

**Method**: Semantic version comparison from YAML frontmatter

**Comparison algorithm:**

```python
def parse_yaml_version(file_path):
    """从 SKILL.md 的 YAML frontmatter 提取 version 字段

    Returns:
        str: 版本号 (如 "1.1.0") 或 None
    """
    import re
    with open(file_path, 'r') as f:
        # 读取 YAML frontmatter (---...--- 之间)
        lines = []
        in_yaml = False
        for line in f:
            if line.strip() == '---':
                if not in_yaml:
                    in_yaml = True
                    continue
                else:
                    break  # 结束 YAML 块
            if in_yaml:
                lines.append(line)

        # 查找 version: "x.y.z"
        for line in lines:
            if line.startswith('version:'):
                # 提取引号内的版本号
                match = re.search(r'version:\s*"([^"]+)"', line)
                if match:
                    return match.group(1)
    return None

def compare_semver(v1: str, v2: str) -> int:
    """语义化版本比较

    Args:
        v1: 版本号 1 (如 "2.1.0")
        v2: 版本号 2 (如 "2.0.0")

    Returns:
        int: 1 if v1 > v2, -1 if v1 < v2, 0 if equal
    """
    parts1 = [int(x) for x in v1.split('.')]
    parts2 = [int(x) for x in v2.split('.')]

    for p1, p2 in zip(parts1, parts2):
        if p1 > p2:
            return 1
        elif p1 < p2:
            return -1

    return 0

def content_differs(source_path, target_path):
    """检查两个文件内容是否不同（忽略空白和注释）

    Returns:
        bool: True if content differs
    """
    def normalize(path):
        # 读取文件，移除 YAML frontmatter 和空白行
        with open(path, 'r') as f:
            lines = f.readlines()

        # 跳过 YAML frontmatter
        in_yaml = False
        content_lines = []
        for line in lines:
            if line.strip() == '---':
                if not in_yaml:
                    in_yaml = True
                    continue
                else:
                    in_yaml = False
                    continue
            if not in_yaml and line.strip():
                content_lines.append(line.strip())

        return '\n'.join(content_lines)

    return normalize(source_path) != normalize(target_path)

def compare_skill_versions(source_skill, target_skill):
    """比较两个 skill 的版本

    Returns:
        str: "NEW", "NEWER", "OLDER", "SAME", "CONFLICT"
    """
    import os
    source_path = f"{source_skills_dir}/{source_skill}/SKILL.md"
    target_path = f"{target_skills_dir}/{target_skill}/SKILL.md"

    # 1. Target 不存在 → NEW
    if not os.path.exists(target_path):
        return "NEW"

    # 2. 解析 YAML version 字段
    source_version = parse_yaml_version(source_path)
    target_version = parse_yaml_version(target_path)

    # 3. 向后兼容：任一缺少 version → fallback to legacy
    if not source_version or not target_version:
        return compare_legacy(source_path, target_path)

    # 4. 语义化版本比较
    cmp = compare_semver(source_version, target_version)

    if cmp > 0:
        return "NEWER"    # Source version higher
    elif cmp < 0:
        return "OLDER"    # Source version lower
    else:
        # 5. 版本相同，检查内容
        if content_differs(source_path, target_path):
            return "CONFLICT"  # Same version, different content
        else:
            return "SAME"

def compare_legacy(source_path, target_path):
    """Legacy 比较方法（时间 + 行数）- 向后兼容"""
    import os
    # 原有的 stat -f %m 和 wc -l 逻辑
    source_time = os.path.getmtime(source_path)
    target_time = os.path.getmtime(target_path)

    if source_time > target_time:
        return "NEWER"
    elif source_time < target_time:
        return "OLDER"
    else:
        # 时间相同，比较行数
        source_lines = len(open(source_path).readlines())
        target_lines = len(open(target_path).readlines())

        if source_lines != target_lines:
            return "CONFLICT"
        else:
            return "SAME"
```

**Process**:
1. Parse `version: "x.y.z"` from SKILL.md YAML frontmatter
2. Compare using semantic versioning rules:
   - Major: Breaking changes (2.0.0 > 1.9.0)
   - Minor: New features (1.1.0 > 1.0.0)
   - Patch: Bug fixes (1.0.1 > 1.0.0)
3. Detect conflicts: Same version, different content
4. Fallback: If no version field, use legacy (time + size)

**Status meanings:**
- **NEW** - Skill doesn't exist in target (safe to copy)
- **NEWER** - Source version > target version (2.1.0 > 2.0.0, recommend update)
- **OLDER** - Source version < target version (warn before overwrite)
- **SAME** - Versions and content identical (skip)
- **CONFLICT** - Same version but content differs (manual review needed)

**Legacy fallback** (for skills without `version` field):
- Compare modification time (`stat -f %m`)
- If time same, compare file size (`wc -l`)

## Analysis Output

```
📊 Analysis:
┌─────────────────┬────────┬──────────────────────────────┐
│ Skill           │ Status │ Action                       │
├─────────────────┼────────┼──────────────────────────────┤
│ adr             │ NEWER  │ Update (v1.1.0 → v1.2.0)     │
│ create-issues   │ NEW    │ Add (v1.0.0)                 │
│ start-issue     │ NEWER  │ Update (v2.1.0 → v2.2.0)     │
│ finish-issue    │ NEW    │ Add (v1.0.0)                 │
│ status          │ SAME   │ Skip (both v1.0.0)           │
│ review          │ OLDER  │ Skip (v1.0.0 < v1.1.0)       │
│ work-issue      │ CONFLICT│ Manual review needed         │
│                 │        │ (both v3.0.0, content diff)  │
│ (15 others)     │ SAME   │ Skip                         │
└─────────────────┴────────┴──────────────────────────────┘

Summary:
- New skills: 2 (create-issues, finish-issue)
- Updated skills: 2 (adr, start-issue)
- Unchanged: 15
- Skipped (older): 1 (review)
- Conflicts: 1 (work-issue - requires manual resolution)
- Total to sync: 4 skills
```

## Conflict Handling

### OLDER Source (Warning)

```
⚠️ Warning: Source skill is OLDER than target

Skill: status
Source: 2026-03-01 (220 lines)
Target: 2026-03-04 (223 lines)

Options:
1. Skip (recommended) - Keep newer version
2. Overwrite - Replace with older version
3. Diff - Show differences

Choice (1/2/3):
```

### CONFLICT Detection (Version Mismatch)

```
❌ Conflict detected

Skill: work-issue
Source version: v3.0.0
Target version: v3.0.0
Content differs: Yes

⚠️ Issue: Version numbers match but content differs

This usually means:
- Both sides modified same version
- Forgot to bump version after changes
- Divergent development

Recommended action:
1. Review changes: diff source/SKILL.md target/SKILL.md
2. Merge manually or choose one version
3. Update version number after merge (v3.0.1 or v3.1.0)

Options:
1. Skip - Keep current version (no sync)
2. Show diff - Compare line by line
3. Overwrite - Use source version (requires confirmation)
4. Manual merge - Open both files in editor

Choice (1/2/3/4):
```

**Why conflicts occur:**
- Both source and target modified same version
- Version number not bumped after content changes
- Parallel development without coordination

**Resolution steps:**
1. Review both versions (option 2: show diff)
2. Choose merge strategy:
   - Manual merge: Combine both changes
   - Accept source: Use newer implementation
   - Accept target: Keep current version
3. Bump version number (v3.0.0 → v3.0.1 or v3.1.0)
4. Re-run sync to verify

## Backup Strategy

**Automatic backup before overwrite (incremental mode only):**

```bash
Before updating any skill:

✅ Creating backup: .claude/skills/adr.backup-2026-03-06/
✅ Backed up: adr/SKILL.md
✅ Backed up: adr/LICENSE.txt

Now updating adr...
✅ Updated: adr (408 → 443 lines)

Rollback available: .claude/skills/adr.backup-2026-03-06/
```

**Backup cleanup:**
- Automatic after 7 days
- Or manual: `rm -rf .claude/skills/*.backup-*`

**Note on --clean mode:**
- `--clean` mode does NOT create backups
- Relies on git version control for recovery
- Use `git restore .claude/skills/` to recover if needed

## What Gets Synced

```
.claude/skills/
├── README.md                 ✅ Synced (skills system guide)
├── WORKFLOW_PATTERNS.md      ✅ Synced (workflow requirements)
├── PYTHON_GUIDE.md           ✅ Synced (development guide)
├── _shared/                  ✅ Synced (shared utilities)
│   ├── *.py
│   └── tests/
├── skill-name/
│   ├── SKILL.md              ✅ Synced (entire directory)
│   ├── LICENSE.txt           ✅ Synced
│   ├── scripts/              ✅ Synced (if exists)
│   ├── references/           ✅ Synced (if exists)
│   └── assets/               ✅ Synced (if exists)
└── another-skill/
    └── ...                   ✅ Synced

.claude/
├── settings.json             ❌ Not synced (project-specific)
├── MEMORY.md                 ❌ Not synced (project-specific)
└── plans/                    ❌ Not synced (project-specific)
```

**Note:**
- Entire skill directories are synced, not just SKILL.md
- Root-level documentation (README, WORKFLOW_PATTERNS, PYTHON_GUIDE) is synced to preserve framework knowledge
- Shared utilities and tests are synced for cross-skill compatibility

## Usage Examples

### Example 1: Framework Upgrade

**User says:**
> "update skills from the framework"

**What happens:**
1. Pull from ~/dev/ai-dev
2. Scan both projects
3. Show: 4 skills to update
4. Confirm and sync
5. Report: "Updated 4 skills"

**Time:** ~30 seconds

### Example 2: Selective Update

**User says:**
> "pull only the adr and status skills"

**What happens:**
1. `/update-skills --from ~/dev/ai-dev --skills adr,status`
2. Compare only those 2 skills
3. Show: 1 updated (adr), 1 same (status)
4. Sync adr only
5. Report: "Updated adr skill"

**Time:** ~20 seconds

### Example 3: Promote to Framework

**User says:**
> "push my custom skills to the framework"

**What happens:**
1. `/update-skills --to ~/dev/ai-dev --skills custom-deploy,custom-test`
2. Compare custom skills
3. Show: 2 NEW skills
4. Confirm and push
5. Report: "Pushed 2 skills to framework"

**Time:** ~25 seconds

## Safety Features

**Pre-flight checks:**
- ✅ Source/target paths exist
- ✅ Source has .claude/skills/ directory
- ✅ User confirmation before changes
- ✅ Dry-run preview available

**Version protection:**
- Warns when overwriting newer target
- Detects conflicts (same time, different content)
- Shows line count differences
- Provides diff option

**Backup protection:**
- Automatic backup before overwrite
- Timestamped backup directories
- Easy rollback

## Error Handling

### Invalid Source/Target

```
❌ Error: Project not found

Path: ../nonexistent
Expected: ../nonexistent/.claude/skills/

Please check:
1. Path is correct
2. Project has .claude/skills/ directory
3. You have read permissions
```

### No Skills to Update

```
✅ All skills are up to date!

No new or updated skills found in source.
Current project has all latest versions.
```

### Permission Issues

```
❌ Error: Permission denied

Cannot write to: ../buffer/.claude/skills/

Please check:
1. You have write permissions
2. Directory is not read-only
3. No other process is locking the directory
```

## Best Practices

1. **Always dry-run first:** Test with `--dry-run` before applying changes
2. **Selective updates:** Use `--skills` flag to update only specific skills
3. **Framework as source of truth:** Projects pull from framework, framework pulls innovations from projects
4. **Document custom skills:** Ensure complete YAML frontmatter, 200+ lines docs, examples, no hardcoded paths, LICENSE.txt

## Integration

**With other update-* skills:**
```bash
# Complete framework update
/update-pillars --from ~/dev/ai-dev   # 1. Pillars
/update-rules --from ~/dev/ai-dev     # 2. Rules
/update-workflow --from ~/dev/ai-dev  # 3. Workflow
/update-skills --from ~/dev/ai-dev    # 4. Skills

# Or use meta-skill
/update-framework --from ~/dev/ai-dev # All-in-one
```

**Common workflow:**
```
Framework upgrade → Pull Skills → Test locally → Commit
Skill development → Polish → Push to framework → Share
```

## Task Management

**After each sync step**, update progress:

```
Paths validated → Update Task #1
Skills scanned → Update Task #2
Versions compared → Update Task #3
Diff shown → Update Task #4
Sync executed → Update Task #5
Results reported → Update Task #6
```

Provides real-time visibility of sync progress.

## Final Verification

**Before declaring sync complete**, verify:

```
- [ ] All 6 sync tasks completed
- [ ] Source and target paths valid
- [ ] Skills compared successfully
- [ ] User confirmed changes
- [ ] Directories copied correctly
- [ ] Backups created (if overwritten)
- [ ] Sync summary displayed
```

Missing items indicate incomplete sync.

## Workflow Skills Requirements

This is a **workflow skill** and must follow the standard pattern:

1. **TaskCreate** at start - Create todo list for progress tracking
2. **TaskUpdate** during execution - Mark tasks in_progress → completed
3. **Verification checklist** - Final validation before completion

**See**: [WORKFLOW_PATTERNS.md](../WORKFLOW_PATTERNS.md) for complete implementation guide

## Related Skills

- **/update-framework** - Sync entire framework (calls this skill)
- **/update-pillars** - Sync Pillars
- **/update-rules** - Sync rules
- **/update-workflow** - Sync workflow docs

---

**Version:** 2.4.0
**Last Updated:** 2026-03-14
**Changelog:**
- v2.4.0 (2026-03-14): Simplify --clean mode documentation (Issue #256)
- v2.3.0 (2026-03-13): Add --clean parameter for complete directory replacement (Issue #210)
- v2.0.0 (2026-03-10): Upgrade to semantic version comparison (Issue #214)
- v1.0.0 (Initial): Created update-skills skill (Issue #70)

**Pattern:** Tool-Reference (guides sync process)
**Compliance:** ADR-001 Section 4 ✅
