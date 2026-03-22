---
name: vcp-pre-commit-review
description: >
  Review staged/changed files against all applicable VCP standards before committing.
  Produces a PASS/BLOCK verdict. Run this before every commit.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, WebFetch
argument-hint: ""
---

# VCP Pre-Commit Review

Review all staged or changed files against applicable VCP standards and produce a commit verdict.

## Changed Files

!`{ git diff --cached --name-only --diff-filter=d; git diff --name-only --diff-filter=d; git ls-files --others --exclude-standard; } | sort -u`

## Step 1: Resolve Config

1. Read `.vcp/config.json` from the project root. Extract the `pluginRoot` field.
2. **If `.vcp/config.json` does not exist or `pluginRoot` is missing:** Stop and tell the user: "No VCP configuration found. Run `/vcp-init` to configure VCP for this project."
3. **Validate `pluginRoot`:** The path must be absolute, contain `/.claude/` (or `\.claude\` on Windows) as a path segment, and contain only safe path characters (letters, digits, `/`, `\`, `-`, `_`, `.`, `:`, and spaces). Reject any path with shell metacharacters (`;`, `&`, `|`, `$`, `` ` ``, `(`, `)`, `{`, `}`, `<`, `>`, `!`, `~`, `#`, `*`, `?`, `[`, `]`, `'`, `"`). If validation fails, stop and tell the user: "Invalid pluginRoot — must be within ~/.claude/ and contain no shell metacharacters. Run `/vcp-init` to fix." Also verify the file `<pluginRoot>/lib/vcp-context-core.ts` exists using Glob. If it does not exist, stop and tell the user: "pluginRoot points to an invalid VCP installation. Run `/vcp-init` to fix."
4. Run the config resolution script via Bash:
   ```bash
   bun "<pluginRoot>/lib/resolve-config.ts" "<project-root>"
   ```
5. Parse the JSON output. It contains: `applicableStandards`, `ignoredRules`, `severity`, `exclude`.

## Step 2: Fetch Applicable Standards

**No tag filter for this skill** — load ALL entries from `applicableStandards`.

For each standard, use WebFetch to fetch its content from:
```
{entry.url}
```

Extract the **Rules** section from each fetched standard.

## Step 4: Review Changed Files

Only review the files listed in the "Changed Files" section above. Skip files that match `exclude` patterns from the resolved config.

For each changed file:
1. Read the file content.
2. Check it against ALL rules from ALL loaded standards that are relevant to that file type.
3. Note any violations with standard ID, rule number, and line number.

## Step 5: Produce Verdict

Output findings grouped per file, then by severity. Only include findings at or above the `severity` threshold from the resolved config.

Before outputting findings, remove any that match an entry in the `ignoredRules` array from the resolved config. If `"standard-id/rule-N"` is in the list, suppress that specific rule's findings. (Standard-level ignores are already applied by the config resolution script.) After filtering, if any findings were suppressed, append a line: `**Suppressed:** X finding(s) by ignore config.` If any suppressed findings came from security-scoped standards (tag `"security"`) or compliance standards, also add: `**WARNING: Critical security findings suppressed by ignore config. Review .vcp/config.json ignore list.**`

Use this format:

```
### VCP Pre-Commit Review

**Scopes:** core, web-backend
**Standards loaded:** N standards, M rules checked
**Files reviewed:** X files

#### src/routes/users.ts
- **[core-security] Rule 3** — SQL string concatenation at line 42
- **[web-backend-security] Rule 7** — Missing authorization check at line 15

#### src/utils/helpers.ts
- No issues found.

---

**Verdict: BLOCK — 2 issues must be fixed**
```

Or if clean:

```
### VCP Pre-Commit Review

**Files reviewed:** X files
**Standards loaded:** N standards

All files pass. No issues found.

**Verdict: PASS — safe to commit**
```

The verdict is:
- **PASS** — zero findings at or above the severity threshold
- **BLOCK** — one or more findings at or above the severity threshold. List all blocking issues.
