---
name: bootstrap-project
description: Initializes the Claude Code configuration in a new or existing project using the dotforge template.
context: fork
---

# Bootstrap Project

Initialize a complete `.claude/` in the current project using the dotforge template.

## Step 0: Determine profile

Check if $ARGUMENTS contains `--profile minimal`, `--profile standard`, or `--profile full`.
If not specified, use `standard` as default.

**Profiles control what gets installed:**

| Component | minimal | standard | full |
|-----------|---------|----------|------|
| CLAUDE.md | yes | yes | yes |
| settings.json | yes | yes | yes |
| block-destructive hook | yes | yes | yes |
| lint-on-save hook | no | yes | yes |
| session-report hook | no | yes | yes |
| warn-missing-test hook | no | no | yes (strict profile) |
| rules/ (_common + stack) | yes | yes | yes |
| commands/ | no | yes | yes |
| agents/ + orchestration | no | yes | yes |
| agent-memory/ | no | no | yes |
| CLAUDE_ERRORS.md | no | yes | yes (pre-populated) |
| memory.md rule | no | yes | yes |

Save the profile in `.claude/settings.local.json` under `env.FORGE_BOOTSTRAP_PROFILE`.

## Step 1: Detect stack

Use detection rules from `$DOTFORGE_DIR/stacks/detect.md`.

## Step 2: Confirm with user

Show:
```
Profile: {{profile}}
Detected stack: {{stacks}}
Will create:
- CLAUDE.md (base template + stack rules)
- .claude/settings.json (base permissions + stack)
- .claude/rules/ (common rules + stack)
- .claude/hooks/ (block-destructive + lint + session-report)  [minimal: block-destructive only]
- .claude/commands/ (audit, health)                    [minimal: skipped]
- .claude/agents/ + orchestration                      [minimal: skipped]
- CLAUDE_ERRORS.md (empty, for error logging)          [minimal: skipped]

Proceed? (yes/no)
```

Adapt the list shown based on the profile (hide components that won't be installed).

## Step 3: Generate CLAUDE.md

Use `$DOTFORGE_DIR/template/CLAUDE.md.tmpl` as the base.
Replace markers:
- `{{PROJECT_NAME}}` → name of the current directory
- `<!-- forge:stack -->` → detected technologies
- `<!-- forge:commands -->` → detected build/test commands (package.json scripts, Makefile targets, etc.)

## Step 4: Generate settings.json

1. Load `$DOTFORGE_DIR/template/settings.json.tmpl` as the base
2. For **each** detected stack, read `$DOTFORGE_DIR/stacks/{stack}/settings.json.partial`
3. Merge: combine the `allow` arrays from **all** partials with the base (union of sets, no duplicates)
4. Merge: combine the `deny` arrays the same way
5. Write to `.claude/settings.json`

**Multi-stack:** If multiple stacks are detected (e.g.: python-fastapi + react-vite-ts + docker-deploy), merge ALL partials. Order does not matter — it is a union of sets.

## Step 4b: Validate JSON

Before writing `settings.json`, validate that the generated JSON is valid:

```bash
python3 -c 'import json; json.load(open(".claude/settings.json"))' 2>&1
```

Or if not yet written, validate the content in memory/string:
```bash
echo '<json_content>' | python3 -c 'import json,sys; json.load(sys.stdin)'
```

If validation fails, show the exact error and DO NOT write the file. Fix the JSON before continuing.

## Step 5: Copy hooks

1. Copy `$DOTFORGE_DIR/template/hooks/block-destructive.sh` → `.claude/hooks/` (ALL profiles)
2. If profile is `standard` or `full`: copy `$DOTFORGE_DIR/template/hooks/lint-on-save.sh`
3. If profile is `standard` or `full`: copy `$DOTFORGE_DIR/template/hooks/session-report.sh`
4. If profile is `standard` or `full`: copy `$DOTFORGE_DIR/template/hooks/detect-stack-drift.sh`
5. If profile is `full`: copy `$DOTFORGE_DIR/template/hooks/warn-missing-test.sh`
5. `chmod +x` all copied hooks
6. For each detected stack, if `$DOTFORGE_DIR/stacks/{stack}/hooks/` exists:
   - Copy the entire hooks directory to `.claude/hooks/{stack}/`
   - If a `core/` directory exists alongside hooks, copy it too (e.g., hookify needs core/ + hooks/)
   - Ensure Python scripts are executable

## Step 6: Copy rules

1. Copy `$DOTFORGE_DIR/template/rules/_common.md` → `.claude/rules/`
2. For each detected stack, copy rules from `$DOTFORGE_DIR/stacks/{stack}/rules/` → `.claude/rules/`

## Step 6b: Domain knowledge scaffolding

**Only if domain info was provided** (via `/forge init` Q4 or user explicitly requests it during bootstrap).

If any detected stack has a `domain:` field in its rules (e.g., `stacks/trading/rules/trading.md`):
1. Create `.claude/rules/domain/` directory
2. Copy domain-tagged rules from the stack into `.claude/rules/domain/` instead of `.claude/rules/`
3. Show: "Domain stack detected: {{domain}}. Domain rules copied to .claude/rules/domain/"

If the user provided domain description (from init Q4 context):
1. Create `.claude/rules/domain/` directory if not exists
2. Generate 1-3 seed domain rule files based on the described concepts:
   - Each file: frontmatter with `globs:` (domain-specific patterns), `domain:` tag, `last_verified:` (today)
   - Content: key facts, constraints, business rules — concise, imperative, <40 lines each
   - File names: kebab-case matching the domain area (e.g., `jira-api.md`, `agile-metrics.md`)
3. Show generated files to user for confirmation before writing

If neither condition is met, skip this step entirely — no noise for projects without domain context.

**Important:** Domain rules in `.claude/rules/domain/` are project-owned. They are NOT tracked in the forge manifest and are NOT updated by `/forge sync`.

## Step 7: Copy commands

**Skip if profile is `minimal`.**

Copy `$DOTFORGE_DIR/template/commands/` → `.claude/commands/`

## Step 8: Copy agents and orchestration rule

**Skip if profile is `minimal`.**

1. Copy `$DOTFORGE_DIR/agents/*.md` → `.claude/agents/`
2. Copy `$DOTFORGE_DIR/template/rules/agents.md` → `.claude/rules/agents.md`

This gives the project access to the 6 specialized subagents (researcher, architect, implementer, code-reviewer, security-auditor, test-runner) and the orchestration rule that defines when to delegate.

## Step 9: Create CLAUDE_ERRORS.md

**Skip if profile is `minimal`.**

For `full` profile: pre-populate with the Type column format and example entry.
For `standard` profile: create empty template.

```markdown
# Known errors — {{PROJECT_NAME}}

Evolving log of errors and lessons learned. Consult BEFORE working in areas with prior errors.

Truth hierarchy: source code > CLAUDE.md > CLAUDE_ERRORS.md > auto-memory

## Format
| Date | Area | Type | Error | Root cause | Fix | Derived rule |
|------|------|------|-------|------------|-----|--------------|

Valid types: `syntax`, `logic`, `integration`, `config`, `security`
```

## Step 9b: Create agent-memory/

**Only for `full` profile.** Standard creates the directory but not the seed files.

Create `.claude/agent-memory/` directory for agents with `memory: project` to persist learnings:

```bash
mkdir -p .claude/agent-memory
```

Create a seed file for each memory-enabled agent so the directory structure is ready:
```bash
for agent in implementer architect code-reviewer security-auditor; do
  touch ".claude/agent-memory/${agent}.md"
done
```

This enables implementer, architect, code-reviewer, and security-auditor to accumulate project-specific knowledge across sessions.

## Step 10: Suggest global hook

If the user does not have `detect-claude-changes.sh` installed in `~/.claude/settings.json`, show:

```
Tip: For automatic practice capture, install the global hook:
Copy hooks/detect-claude-changes.sh to ~/.claude/hooks/
Add in ~/.claude/settings.json under hooks → Stop
See docs for details.
```

## Step 11: Generate manifest

Create `.claude/.forge-manifest.json` with the SHA256 hash of each file created during bootstrap:

```bash
shasum -a 256 <file> | cut -d' ' -f1
```

Format:
```json
{
  "dotforge_version": "<version from $DOTFORGE_DIR/VERSION>",
  "synced_at": "<current date YYYY-MM-DD>",
  "stacks": ["<detected-stack-1>", "<detected-stack-2>"],
  "files": {
    ".claude/settings.json": {"hash": "sha256:<hash>", "source": "template+stacks"},
    ".claude/rules/_common.md": {"hash": "sha256:<hash>", "source": "template"},
    ".claude/hooks/block-destructive.sh": {"hash": "sha256:<hash>", "source": "template"},
    ".claude/hooks/lint-on-save.sh": {"hash": "sha256:<hash>", "source": "template"}
  }
}
```

- `source` indicates where the file came from: `"template"`, `"template+stacks"` (if merged from base + stacks), or `"stacks/<name>"`.
- Include ALL files created in `.claude/` (rules, hooks, commands, agents).
- Do NOT include CLAUDE.md or CLAUDE_ERRORS.md (they are in the root, not in `.claude/`).

## Step 12: Report

Show a summary of created files and suggest running `/audit-project` to verify.
