---
name: create-issue
description: Create a GitHub issue following the project's issue templates. Classifies the issue type, fills required fields per template, and creates it via gh CLI. Use when the user wants to file a bug, request a feature, report a pass bug, or create any GitHub issue.
---

# Create GitHub Issue

Create issues that follow `.github/ISSUE_TEMPLATE/` templates exactly.

## Step 0: Determine Input Source

Check how the issue was triggered:

**A) From `KNOWN_ISSUES.md`** — If user says "create issue from known issues", "/create-issue known", or similar:

1. Read `KNOWN_ISSUES.md` from project root
2. If file doesn't exist or has no entries, tell user "No known issues found" and **stop**
3. List all entries with their title, severity, and brief description
4. Present the list and ask the user which issue they want to file
5. **Verify the selected issue is still real and unresolved:**
   - If `Location` is present and not `N/A`:
     - Read the file(s) mentioned and check if the problem still exists in the current code
     - If **resolved**: remove the entry from `KNOWN_ISSUES.md`, inform user, and **stop**
     - If **still present**: proceed to Step 1 using the issue's description as input
   - If `Location` is missing or `N/A`:
     - Ask the user to confirm whether the issue is still valid based on the description
     - If **no longer valid**: remove the entry from `KNOWN_ISSUES.md`, inform user, and **stop**
     - If **still valid**: proceed to Step 1 using the issue's description as input
6. After the GitHub issue is created, **remove the entry** from `KNOWN_ISSUES.md` (the issue is now tracked on GitHub)

**B) Direct user input** — Normal flow, proceed to Step 1 with user-provided description.

## Step 1: Authenticate

```bash
gh auth status
```

If not authenticated, tell the user to run `gh auth login` and **stop**.

## Step 2: Check for Existing Issues

**Launch a `general-purpose` agent** (via `Task` tool, **model: haiku**) to perform the dedup check. This keeps the main context clean and fast.

**Agent prompt must include:** the issue summary/keywords, and these exact instructions:

> **IMPORTANT: ONLY use `gh` CLI commands. Do NOT read source code, test files, or explore the repository. Your sole job is to check GitHub issues for duplicates.**
>
> Follow the two-step process below, then return EXACTLY one of: `DUPLICATE #N`, `RELATED #N1 #N2 ...`, or `NO_MATCH`. Keep your response to 1-3 sentences plus the verdict.

### Two-Step Search Process (for the agent)

**Step A — Scan all open issue titles:**

```bash
gh issue list --state open --limit 200 --search "updated:>=YYYY-MM-DD" --json number,title,labels \
  --jq '.[] | "\(.number)\t\(.title)\t\(.labels | map(.name) | join(","))"'
```

Compute the date 6 months ago for the `updated:>=` filter. Scan output for keywords related to the new issue.

**Step B — Deep-read candidates only (max 3):**

For each title that looks related (up to 3), fetch context:

```bash
gh issue view NUMBER
```

Only read body — skip `--comments` unless the body is ambiguous. Determine if it's truly the same issue or just superficially similar.

### Decision rules (agent returns)

- **Exact match** (same root cause/request) → return `DUPLICATE #N`
- **Related but different** → return `RELATED #N1 #N2 ...`
- **No matches** → return `NO_MATCH`

### How to act on the result

- `DUPLICATE #N` → Do NOT create. Tell the user the existing issue. **Stop here.**
- `RELATED #N1 ...` → Proceed, reference in body: `Related: #N1, #N2`
- `NO_MATCH` → Proceed normally.

## Step 3: Classify the Issue

Read `.github/ISSUE_TEMPLATE/` to get the current templates, then match the user's description to the correct template:

| Template | Use When | Labels |
| -------- | -------- | ------ |
| `bug_report.yml` | General bug (parser, printer, bindings, codegen, build) | `bug` |
| `pass_bug.yml` | Bug in an IR pass or transformation | `bug`, `ir-pass` |
| `feature_request.yml` | New feature or enhancement | `enhancement` |
| `new_operation.yml` | New tensor/block-level operation | `enhancement`, `new-operation` |
| `performance_issue.yml` | Performance regression or optimization | `performance` |
| `documentation.yml` | Missing, incorrect, or unclear docs | `documentation` |

**Classification rules:**

- If about a specific pass producing wrong IR → `pass_bug.yml`
- If about a crash/error not in a pass → `bug_report.yml`
- If about slow execution or regression → `performance_issue.yml`
- If requesting a new op (tensor/block) → `new_operation.yml`
- If requesting any other new capability → `feature_request.yml`
- If about docs being wrong/missing → `documentation.yml`

**If ambiguous**, ask the user to clarify using `AskUserQuestion`.

## Step 4: Gather Required Fields

Each template has **required fields** (marked `required: true` in the YAML). You MUST fill every required field.

**Ask the user** for any required information you cannot infer. Use `AskUserQuestion` for dropdown selections (component, NPU kind, host platform, etc.).

**For fields you can auto-fill:**

- **Git Commit ID**: Run `git rev-parse HEAD` to get the current commit
- **Title prefix**: Use the template's title prefix (`[Bug]`, `[Pass Bug]`, etc.)
- **Host Platform**: Run `uname -s -m` to detect OS and arch. Map to: `Linux aarch64` → `Linux (aarch64)`, `Linux x86_64` → `Linux (x86_64)`, `Darwin arm64` → `macOS (aarch64)`, `Darwin x86_64` → `Other (please specify)` with note `macOS (x86_64)`. Fall back to `Other` if unrecognized. For pass bugs (`pass_bug.yml`), default to `N/A (not hardware-specific)` unless the bug is platform-specific.
- **NPU Kind**: Run `npu-smi info 2>/dev/null` to detect NPU. If command not found or no output, default to `N/A (not hardware-specific)` (or `N/A (CPU-only issue)` for `performance_issue.yml`). Parse model name to map to Ascend 910B/910C if present.

## Step 5: Format the Issue Body

Since `gh issue create` uses markdown body (not YAML form fields), format the body to match the template structure using markdown sections:

```markdown
### Field Label

Field content here

### Another Field

More content
```

**For dropdown fields**, state the selected value as plain text.

## Step 6: Create the Issue

```bash
gh issue create \
  --title "[Prefix] Short description" \
  --label "label1" --label "label2" \
  --body "$(cat <<'EOF'
### Field 1
content

### Field 2
content
EOF
)"
```

**After creation**, display the issue URL to the user.

## Template Field Reference

### Bug Report (`[Bug]`)

Required: Component (dropdown), Description, Steps to Reproduce, Expected Behavior, Actual Behavior, Git Commit ID, NPU Kind (dropdown), Host Platform (dropdown)

### Pass Bug (`[Pass Bug]`)

Required: Pass Name, Description, Git Commit ID, Before IR (`@pl.program`), Expected IR, Actual IR or Error
Optional: NPU Kind (dropdown), Host Platform (dropdown)

### Feature Request (`[Feature]`)

Required: Summary, Motivation / Use Case

### New Operation (`[New Op]`)

Required: Operation Level (dropdown), Proposed Name & Signature, Semantics Description, Example Usage, Motivation / Use Case

### Performance Issue (`[Performance]`)

Required: Summary, Git Commit ID, NPU Kind (dropdown), Host Platform (dropdown), Reproduction Script, Expected Performance, Actual Performance

### Documentation (`[Docs]`)

Required: Documentation Location, What's Wrong or Missing?

## Checklist

- [ ] Input source determined (KNOWN_ISSUES.md or direct)
- [ ] If from KNOWN_ISSUES.md: issue verified as still real and unresolved
- [ ] gh CLI authenticated
- [ ] Searched for existing issues (no exact duplicate found)
- [ ] Related issues referenced in body (if any)
- [ ] Issue classified to correct template
- [ ] All required fields filled
- [ ] Title uses correct prefix from template
- [ ] Labels match template
- [ ] Body formatted with markdown sections matching template fields
- [ ] Issue created and URL displayed
- [ ] If from KNOWN_ISSUES.md: entry removed from file
