---
name: claude-code-auto-improve
description: Fetch latest Claude Code updates, validate plugin, and apply improvements
allowed-tools: [Read, Write, Edit, Glob, Grep, Task, WebFetch, AskUserQuestion, Bash]
---

# Auto-Improve

Automatically improve bluera-base by fetching latest Claude Code updates and validating against best practices.

## Modes

| Mode | Description |
|------|-------------|
| `check` | Analyze only, no changes (default) |
| `apply` | Apply improvements after confirmation |
| `config` | Show/edit auto-improve configuration |

## Workflow

```text
┌─────────────────┐
│ Gather Updates  │ ← CHANGELOG, GitHub issues, learnings, knowledge
└────────┬────────┘
         ▼
┌─────────────────┐
│ Analyze Changes │ ← Parse recent entries, extract relevant updates
└────────┬────────┘
         ▼
┌─────────────────┐
│ Validate Plugin │ ← Run audit, check patterns
└────────┬────────┘
         ▼
┌─────────────────┐
│ Propose Changes │ ← Present findings, get approval
└────────┬────────┘
         ▼
┌─────────────────┐
│ Apply & Commit  │ ← Make changes, version bump if needed
└─────────────────┘
```

---

## Phase 1: Gather Updates

Collect information from multiple sources. See [references/sources.md](references/sources.md) for details.

### 1.1 Read Pending Learnings

```bash
# Check for pending learnings
cat .bluera/bluera-base/state/pending-learnings.jsonl 2>/dev/null
```

Parse each line as JSON with fields: `type`, `pattern`, `learning`, `confidence`, `source`.

### 1.2 Fetch CHANGELOG

```yaml
webfetch:
  url: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
  prompt: |
    Extract the most recent 3 changelog entries (versions).
    For each entry, return:
    - Version and date
    - Added items (new features)
    - Changed items (behavior changes)
    - Deprecated items
    - Fixed items
    Focus on entries related to: hooks, plugins, skills, commands, frontmatter, agents
```

### 1.3 Search Knowledge Store (if available)

```yaml
mcp:
  tool: mcp__plugin_bluera-knowledge_bluera-knowledge__search
  params:
    query: "Claude Code hooks plugins skills recent changes"
    stores: ["claude-code-docs"]
    intent: find-documentation
    detail: contextual
    limit: 10
```

If store not found, skip this step.

### 1.4 Query GitHub Issues

```bash
gh api repos/anthropics/claude-code/issues \
  --paginate \
  -q '.[] | select(.labels[].name == "bug" or .labels[].name == "enhancement") | {number, title, labels: [.labels[].name], created_at}' \
  | head -20
```

Focus on issues labeled: `hooks`, `plugins`, `bug`, `enhancement`.

---

## Phase 2: Analyze & Compare

### 2.1 Parse CHANGELOG

Extract relevant changes from the last 30 days:

**Categories to extract:**

- Hook changes (new events, behavior changes, breaking changes)
- Plugin manifest changes (new fields, deprecated fields)
- Skill/command frontmatter changes
- Agent system changes
- MCP integration changes

**Parsing patterns:**

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- New hooks: `PreFoo`, `PostBar`
- New frontmatter field: `argument-hint`

### Changed
- Hook exit code 2 now blocks with message

### Deprecated
- `old_field` in plugin.json - use `new_field`

### Fixed
- Plugin loading order issue
```

### 2.2 Compare with Current Implementation

For each relevant change found:

1. **Search codebase** for affected patterns
2. **Check if already updated** (avoid redundant changes)
3. **Categorize priority**: breaking (high) > deprecation (medium) > enhancement (low)

```yaml
comparison_result:
  breaking_changes: []
  deprecated_patterns: []
  new_features: []
  improvements: []
```

---

## Phase 3: Validate Plugin

### 3.1 Run Audit

Spawn the `claude-code-guide` agent to audit the plugin:

```yaml
task:
  subagent_type: claude-code-guide
  prompt: |
    Run a comprehensive audit of the bluera-base plugin.
    Focus on:
    1. Hook patterns against latest best practices
    2. Skill frontmatter against current spec
    3. Plugin manifest completeness
    4. Deprecated patterns that should be updated

    Return findings as:
    - Critical: Must fix
    - Warning: Should fix
    - Info: Could improve
```

### 3.2 Check Specific Patterns

| Pattern | Check |
|---------|-------|
| Hook exit codes | Verify exit 2 for blocking, exit 0 for allow |
| Defensive stdin | All hooks should drain stdin |
| ${CLAUDE_PLUGIN_ROOT} | All paths should use this variable |
| Frontmatter | Check for deprecated or missing fields |
| async hooks | Verify appropriate use of async: true |

---

## Phase 4: Propose Improvements

### 4.1 Compile Findings

Organize findings into actionable groups:

```markdown
## Auto-Improve Findings

### From CHANGELOG (v1.2.3 - 2025-02-01)
- [ ] New `argument-hint` frontmatter available for commands
- [ ] Hook async pattern changed

### From Audit
- [ ] Hook `foo.sh` missing defensive stdin pattern
- [ ] Skill `bar` using deprecated field

### From Learnings
- [ ] User frequently runs `bun test` - consider adding to presets
```

### 4.2 Get User Approval

```yaml
question: "How would you like to proceed with improvements?"
header: "Action"
options:
  - label: "Apply all (Recommended)"
    description: "Apply all improvements and commit"
  - label: "Apply selected"
    description: "Let me choose which to apply"
  - label: "Check only"
    description: "Show findings without changes"
multiSelect: false
```

If "Apply selected", present each finding with:

```yaml
question: "Apply this improvement?"
header: "Change"
options:
  - label: "Yes"
    description: "<change description>"
  - label: "Skip"
    description: "Don't apply this change"
multiSelect: false
```

---

## Phase 5: Apply & Commit

### 5.1 Apply Changes

For each approved change:

1. **Backup** - Note original content for rollback
2. **Apply** - Make the change using Edit tool
3. **Verify** - Ensure change was applied correctly

### 5.2 Version Bump (if needed)

If changes warrant a release:

```yaml
version_bump_criteria:
  patch: Bug fixes, documentation updates
  minor: New features, improvements
  major: Breaking changes (rare for auto-improve)
```

Use release skill with appropriate bump type.

### 5.3 Commit Changes

```bash
git add -A
git commit -m "chore(auto-improve): apply latest best practices

- <list of changes applied>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
```

---

## Configuration

Configuration is stored in `.bluera/bluera-base/config.json`:

```json
{
  "autoImprove": {
    "enabled": false,
    "autoApply": false,
    "sources": ["changelog", "github", "knowledge", "learnings"],
    "changelogUrl": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
  }
}
```

| Field | Default | Description |
|-------|---------|-------------|
| `enabled` | false | Enable auto-improve checks |
| `autoApply` | false | Apply changes without confirmation |
| `sources` | all | Which sources to check |
| `changelogUrl` | GitHub raw | CHANGELOG location |

### Managing Configuration

```bash
# View current config
/bluera-base:claude-code-auto-improve config

# Enable auto-improve
/bluera-base:config set autoImprove.enabled true

# Set to auto-apply mode
/bluera-base:config set autoImprove.autoApply true

# Disable specific source
/bluera-base:config set autoImprove.sources '["changelog", "github"]'
```

---

## Error Handling

| Error | Action |
|-------|--------|
| CHANGELOG fetch fails | Log warning, continue with other sources |
| GitHub API rate limited | Skip GitHub issues, suggest `gh auth login` |
| Knowledge store not found | Skip knowledge search |
| No learnings file | Skip learnings, continue |

Always complete with available sources rather than failing entirely.

---

## Output

Final output summarizes actions taken:

```markdown
## Auto-Improve Complete

**Sources checked:** changelog, github, learnings
**Issues found:** 5
**Changes applied:** 3
**Skipped:** 2

### Applied Changes
1. Added argument-hint to 4 commands
2. Updated hook defensive stdin pattern
3. Fixed deprecated frontmatter field

### Skipped
1. Knowledge store search (not available)
2. Enhancement suggestion (user declined)
```
