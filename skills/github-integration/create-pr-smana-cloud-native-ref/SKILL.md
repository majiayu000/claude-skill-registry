---
name: create-pr
description: Create or update Pull Requests with AI-generated descriptions, mermaid diagrams, and file walkthroughs. Integrates with SDD specs. Use --update flag to modify existing PRs.
allowed-tools: Bash(git:*), Bash(gh:*)
---

# Create PR Skill

Generate and create/update a comprehensive PR with description, diagram, and file walkthrough.

## Usage

```
/create-pr [base-branch]       # Create new PR (default: main)
/create-pr --update <number>   # Update existing PR description
```

## Mode Detection

Parse arguments to determine mode:
- If `--update` or `-u` followed by a number → **Update Mode**
- Otherwise → **Create Mode** (argument is base branch, default: main)

## Workflow

### Create Mode

#### Step 1: Gather Information

Run in parallel:
```bash
git log origin/$BASE..HEAD --oneline
git diff origin/$BASE...HEAD --stat
git diff origin/$BASE...HEAD
```

#### Step 2: Detect Spec (SDD Integration)

Check for spec-requiring changes:
```bash
CHANGED_PATHS=$(git diff origin/$BASE...HEAD --name-only)
```

| Pattern | Spec Type |
|---------|-----------|
| `kcl/**/*.k`, `*-composition.yaml` | composition |
| `opentofu/**/*.tf`, `terramate.tm.hcl` | infrastructure |
| `*networkpolicy*`, `*rbac*`, `openbao/**` | security |
| Multiple directories + HelmRelease | platform |

Search for existing spec:
```bash
SPEC_FILE=$(ls -1 docs/specs/active/*.md 2>/dev/null | head -1)
```

#### Step 3: Generate Description

Include:
- **Type**: feat/fix/docs/refactor/perf/test/chore/ci/security
- **Summary**: 1-2 sentences
- **Key changes**: 3 bullet points (max 10 words each)
- **Mermaid flowchart**: LR format, 5-7 nodes max
- **File table**: Max 10 files, grouped
- **Detailed changes**: Collapsible section
- **Labels**: Suggested labels

#### Step 4: Create PR

```bash
git push -u origin $(git branch --show-current)
gh pr create --base ${BASE:-main} --title "..." --body "..."
```

#### Step 5: Output

Return PR URL only.

---

### Update Mode

#### Step 1: Fetch PR Information

Run in parallel:
```bash
gh pr view $PR_NUMBER --json number,title,files,additions,deletions,baseRefName
gh pr diff $PR_NUMBER
```

#### Step 2: Generate Description

Same format as create mode (see PR Template below).

#### Step 3: Update PR

```bash
gh pr edit $PR_NUMBER --body "..."
```

#### Step 4: Output

Return "Updated PR #X" with URL.

---

## PR Template

```markdown
## 🔍 [type]

## 📝 Summary
[1-2 sentences max]

## 📋 Specification
[If spec exists: link to spec file and issue]
[If no spec but recommended: warning with detected type]

## 🎯 Changes
- Change 1 (concise)
- Change 2 (concise)
- Change 3 (concise)

## 📊 Flow
```mermaid
flowchart LR
    comp1["Component"]
    comp2["Service"]:::new
    comp1 --> comp2
    classDef new fill:#1e3a8a,stroke:#3b82f6,stroke-width:3px,color:#fff
```

## 🗂️ Files
| File | Type | Summary |
|------|------|---------|
[max 10 rows]

<details><summary>Details</summary>

### file
- brief changes

</details>

## 🏷️ Labels
[labels]
```

## Spec Integration

### If Spec Exists

Add after Summary:
```markdown
## 📋 Specification

This PR implements: [docs/specs/active/XXXX-name.md](link)

**Spec Status**: [Draft|In Review|Approved]
```

### If No Spec But Recommended

Add warning after Summary:
```markdown
## ⚠️ Spec Recommendation

This PR contains changes that may benefit from a formal specification:
- **Detected type**: [composition|infrastructure|security|platform]
- **Affected paths**: [key paths]

Consider running `/specify [type]` before implementation to ensure thorough planning.
```

Skip warning for trivial changes (docs only, single config file, version bumps).

## Mermaid Styling

```mermaid
flowchart LR
    comp1["Component"]
    comp2["New"]:::new
    comp3["Modified"]:::modified
    comp1 --> comp2 --> comp3
    classDef new fill:#1e3a8a,stroke:#3b82f6,stroke-width:3px,color:#fff
    classDef modified fill:#c2410c,stroke:#f97316,stroke-width:3px,color:#fff
```

- **New**: `fill:#1e3a8a,stroke:#3b82f6,stroke-width:3px,color:#fff`
- **Modified**: `fill:#c2410c,stroke:#f97316,stroke-width:3px,color:#fff`
- **Removed**: `fill:#991b1b,stroke:#dc2626,stroke-width:3px,color:#fff,stroke-dasharray:5 5`

## Best Practices

- Keep diagrams simple (max 8-10 nodes)
- Use descriptive node IDs (camelCase)
- Always quote node descriptions
- Show data flow or component interaction
- Label all arrows clearly
- Group similar file changes in the table
