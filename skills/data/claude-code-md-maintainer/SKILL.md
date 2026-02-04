---
name: claude-code-md-maintainer
description: Validate/update/create CLAUDE.md memory files with progressive disclosure and context-optimized structure
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(find:*), Bash(git:*), Bash(ls:*), Bash(wc:*), Bash(head:*), Bash(tail:*)
---

# CLAUDE.md Maintainer

Audit and maintain `CLAUDE.md` files across any repository. Ensures they function as Claude Code memory (not user documentation).

## Core Principle

`CLAUDE.md` is **Claude's memory**, not a README. Every line loads into context, so keep it lean and actionable.

## Algorithm

### Phase 1: Plan (read-only)

1. **Discover** existing memory files:
   - `./CLAUDE.md` or `./.claude/CLAUDE.md`
   - `./CLAUDE.local.md`
   - Nested `**/CLAUDE.md`
   - `.claude/rules/**/*.md`

2. **Validate** each against invariants (see `docs/invariants.md`)

3. **Audit verbosity**:
   - Count total lines (warn if > 300, suggest if > 60)
   - Detect verbose patterns (see `docs/verbose-patterns.md`)
   - Flag linter-duplicating instructions
   - Identify content that should move to agent_docs/
   - Report actionable findings with line numbers

4. **Identify** module roots (see `docs/directory-heuristics.md`)

5. **Output** proposed changes:
   - Files to update (with change summary)
   - Files to create
   - Ambiguous cases requiring human decision

### Phase 2: Apply (with confirmation)

Only after user confirms:

1. Update existing files
2. Create missing files from templates
3. Report final state

---

## Init Algorithm

For `/bluera-base:claude-code-md init` - creates new CLAUDE.md from scratch.

### Detection Priority

Check files in order (stop at first match):

```text
package.json → JavaScript/TypeScript
Cargo.toml   → Rust
pyproject.toml → Python
go.mod       → Go
```

### Lockfile → Package Manager

| Lockfile | Manager |
|----------|---------|
| bun.lock / bun.lockb | bun |
| yarn.lock | yarn |
| pnpm-lock.yaml | pnpm |
| package-lock.json | npm |
| poetry.lock | poetry |
| uv.lock | uv |
| (none) | ask user |

### Script Extraction

**JavaScript/TypeScript:**

```bash
jq -r '.scripts | keys[]' package.json 2>/dev/null | head -10
```

**Python (pyproject.toml):**

```bash
grep -A 20 '^\[project.scripts\]' pyproject.toml | grep '=' | cut -d'=' -f1 | tr -d ' "'
```

**Rust/Go:** Use standard commands (cargo build/test, go build/test).

### Generated Structure

```markdown
includes/CLAUDE-BASE.md

---

## Package Manager

**Use `{PM}`** - All scripts: `{PM} run <script>`

---

## Scripts

{SCRIPTS - grouped by category if many}

---

## CI/CD

{Only if .github/workflows/ or .gitlab-ci.yml exists}

---
```

### Design Principles

1. **Auto-detect over ask** - Only interview when ambiguous
2. **< 60 lines target** - Start lean, user expands later
3. **Never overwrite** - Check for existing CLAUDE.md first
4. **@include always** - Start with CLAUDE-BASE.md reference

---

## Learn Algorithm

For `/bluera-base:claude-code-md learn` - adds learnings to marker-delimited regions.

### Marker Format

```markdown
## Auto-Learned (bluera-base)
<!-- AUTO:bluera-base:learned -->
- Learning 1
- Learning 2
<!-- END:bluera-base:learned -->
```

### Algorithm Steps

1. **Determine target file**:
   - Default: `CLAUDE.local.md` (personal, gitignored)
   - With `--shared`: `CLAUDE.md` (team-shared)

2. **Read target file** (or create if missing)

3. **Find markers**:
   - Start: `<!-- AUTO:bluera-base:learned -->`
   - End: `<!-- END:bluera-base:learned -->`

4. **If markers missing**: Insert at end of file:

   ```markdown

   ---

   ## Auto-Learned (bluera-base)
   <!-- AUTO:bluera-base:learned -->
   <!-- END:bluera-base:learned -->
   ```

5. **Parse existing learnings** between markers into list

6. **Dedupe check**:
   - Normalize: trim whitespace, lowercase
   - If learning already exists (fuzzy match), skip with message

7. **Secrets check** (CRITICAL):
   - Regex: `api[_-]?key|token|password|secret|-----BEGIN|AWS_|GITHUB_TOKEN|ANTHROPIC_API`
   - If match: REJECT with warning, do NOT write

8. **Hard cap check**:
   - Max 50 lines in auto-managed section
   - If exceeded: warn user, suggest pruning old learnings

9. **Insert learning** as new bullet point

10. **Write file** using Edit tool (replace marker region only)

### Secrets Denylist

```regex
api[_-]?key
token
password
secret
-----BEGIN
AWS_
GITHUB_TOKEN
ANTHROPIC_API_KEY
OPENAI_API_KEY
private[_-]?key
credential
```

### Example Implementation

```bash
# Pseudo-code for the Edit operation
OLD_CONTENT="<!-- AUTO:bluera-base:learned -->
- Old learning 1
<!-- END:bluera-base:learned -->"

NEW_CONTENT="<!-- AUTO:bluera-base:learned -->
- Old learning 1
- New learning here
<!-- END:bluera-base:learned -->"
```

---

## User Control Modes

Control auto-learning behavior via `/bluera-base:config` command:

```bash
/bluera-base:config enable auto-learn    # Opt-in to learning observation
/bluera-base:config set .autoLearn.mode auto  # Change mode
```

Configuration stored in `.bluera/bluera-base/config.json`:

```json
{
  "autoLearn": {
    "enabled": false,    // opt-in by default
    "mode": "suggest",   // suggest | auto
    "threshold": 3,      // occurrences before suggesting
    "target": "local"    // local | shared
  }
}
```

| Mode | Behavior |
|------|----------|
| `suggest` | Show learning suggestions at session end |
| `auto` | Automatically add learnings to marker regions |

**Session signals** are tracked in `.bluera/bluera-base/state/session-signals.json` (ephemeral, gitignored).
Commands with ≥threshold occurrences trigger learning suggestions.

---

## References

- **Audit Templates**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/templates/`
  - `root_CLAUDE.md` - Root project memory
  - `module_CLAUDE.md` - Directory-scoped memory
  - `local_CLAUDE.local.md` - Personal notes

- **Init Templates**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/templates/init/`
  - `js-ts.md` - JavaScript/TypeScript projects
  - `python.md` - Python projects
  - `rust.md` - Rust projects
  - `go.md` - Go projects
  - `ci-github.md` - GitHub Actions CI section
  - `ci-gitlab.md` - GitLab CI section

- **Validation rules**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/docs/invariants.md`

- **Directory detection**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/docs/directory-heuristics.md`

- **Reliability guidance**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/docs/reliability.md`

- **Scope decision guide**: `${CLAUDE_PLUGIN_ROOT}/skills/claude-code-md-maintainer/docs/scope-guide.md`

## Key Rules

1. **Never duplicate** - Module CLAUDE.md should not repeat root rules
2. **Prefer rules files** - Move topic-specific rules to `.claude/rules/<topic>.md`
3. **Use paths: scoping** - Rules files can use `paths:` frontmatter
4. **Hard cap** - If > 25 modules, summarize at bucket level, defer individuals

## Output Format

Report these sections:

- Memory files found
- Files to create
- Files to update (with diff summary)
- Rules files to create/update
- Verbosity report (if issues detected)
- Follow-ups (ambiguous items)

### Verbosity Report

When line count exceeds targets or verbose patterns detected, include:

**Line Count:**

- CLAUDE.md: 142 lines (target: < 60, hard limit: < 300)

**Verbose Patterns Detected:**

| Lines | Issue | Suggestion |
|-------|-------|------------|
| 45-60 | Tool explanation (npm) | Remove - Claude knows npm |
| 80-95 | Command output example | Remove or move to agent_docs/ |
| 110-125 | File enumeration | Summarize as "src/ - application code" |
