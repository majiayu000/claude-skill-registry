---
name: vcp-root-cause-check
description: >
  Analyze a proposed bug fix against VCP root cause analysis standards.
  Determines whether a fix addresses the root cause or just patches a symptom.
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, WebFetch
argument-hint: "[bug description or file path]"
---

# VCP Root Cause Check

Analyze a proposed bug fix to determine whether it addresses the root cause or patches a symptom.

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

From the `applicableStandards` array in the resolved config, keep only the entry where:
- `id` is `core-root-cause-analysis`

Use WebFetch to fetch its content from:
```
{entry.url}
```

Extract the **Rules** section and the **Patterns** section from the fetched standard.

## Step 4: Gather Bug Context

**From `$ARGUMENTS`:** If provided, interpret as either a bug description or a file path.

- **If a file path:** Read the file and look for recent changes (use `git diff` or `git log -1 -p` on the file) to identify the proposed fix.
- **If a bug description:** Use it as context to locate the relevant code.
- **If no arguments:** Look at the current conversation for bug context. If none found, ask the user to describe the bug and point to the proposed fix.

Gather:
1. **Bug description** — What symptom was observed?
2. **Proposed fix** — What code was changed or is about to be changed? Use `git diff` (staged and unstaged), or read the files specified by the user.
3. **Surrounding context** — Read the files involved in the fix. Use Grep to trace how data flows through the affected code paths.

## Step 5: Trace Data Flow

Apply the root cause analysis standard's decision framework:

1. **Where does the symptom appear?** Identify the error, crash, or wrong output.
2. **Where does the incorrect data originate?** Trace the data flow backwards from the symptom — follow variables, function calls, and data transformations upstream.
3. **Are these the same location?** If the symptom location and origin are the same, a local fix is correct. If they differ, the fix should be at the origin.
4. **Does this data flow through other paths?** If yes, a fix only at the symptom site leaves other paths broken.
5. **Would this fix survive a refactor?** If the fix depends on execution order, specific call sites, or implementation details of other modules, it's a patch — not a root cause fix.

## Step 6: Produce Verdict

Output the analysis in this format:

```
### VCP Root Cause Check

**Bug:** [Brief description of the symptom]
**Proposed fix:** [Summary of what the fix changes]

#### Data Flow Trace

1. **Symptom:** [Where the error appears] — `file:line`
2. **Intermediate:** [Data transformation steps] — `file:line`
3. **Origin:** [Where correct data first becomes incorrect] — `file:line`

#### Decision Framework

- **Symptom location:** `file:line`
- **Origin location:** `file:line`
- **Same location?** Yes/No
- **Other data paths affected?** Yes/No — [list if yes]
- **Survives refactor?** Yes/No — [why]

---

**Verdict: ROOT-CAUSE FIX** — The fix addresses the origin of the defect.
```

Or:

```
**Verdict: SYMPTOM-PATCH** — The fix patches where the bug manifests, not where it originates.

**Recommended fix location:** `file:line` — [explanation of what should be fixed there instead]
```

If the analysis is inconclusive (e.g., insufficient context to trace the full data flow), say so and explain what additional information would be needed.
