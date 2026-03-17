---
name: skills:validate
description: Validate skill files meet the standard format and naming conventions
---

# Validate Skill

## When to Use

- After creating or editing a skill
- Before committing skill changes
- When auditing all skills for consistency

## Validation Checks

### Required

- [ ] **Frontmatter**: Has `name:` and `description:` fields
- [ ] **Colon naming**: `name:` uses colon notation (e.g., `tdd:ci` not `tdd-ci`)
- [ ] **Directory match**: Directory name matches frontmatter `name:` field
- [ ] **Title**: Has `# Skill Name` as first heading
- [ ] **When to Use**: Has "When to Use" or "Overview" section
- [ ] **Related Skills**: Has "Related Skills" section at the end
- [ ] **Mermaid diagram**: Workflow/router skills have an embedded mermaid diagram
- [ ] **Diagram colors**: classDef colors match README color legend

### Command Format (Required)

- [ ] **Sandbox classification**: Skill is classified as sandbox or management (see below)
- [ ] **Single commands**: Sandbox skills use one command per code block (no `&&` chaining)
- [ ] **Auto-approve coverage**: All commands in sandbox skills match a pattern in `.claude/settings.json`
- [ ] **No multiline bash**: Sandbox skills avoid heredocs, multiline pipes, or `for` loops in commands

### Recommended

- [ ] **TOC**: Table of Contents present if skill > 50 lines
- [ ] **Placeholders**: All commands are copy-pasteable (no unexplained placeholders)
- [ ] **Task tracking**: TDD/RCA skills have "Task Tracking" section
- [ ] **Parent ref**: Parent category `SKILL.md` references this skill
- [ ] **Imperative voice**: Uses "Run X" not "You should run X"
- [ ] **Length**: Leaf skills are 80-200 lines (300 max)
- [ ] **Diagram-text match**: Diagram nodes correspond to textual flow steps

## Sandbox vs Management Classification

Skills operate on either **sandbox** (safe) or **management** (requires approval) targets:

| Type | Target | Auto-approve? | Command format |
|------|--------|---------------|----------------|
| **Sandbox** | Local Kind cluster, custom HyperShift hosted cluster | YES | Single commands, one per step |
| **Management** | Management cluster, AWS resources, git push, destructive ops | NO | Can chain commands (user approves anyway) |

### Sandbox skills (auto-approved)
Commands target `localtest.me`, `KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-*`, or Kind clusters.

**IMPORTANT**: Run each command separately — not chained with `&&`. Chained or multiline commands break Claude Code's auto-approve pattern matching.

```markdown
## GOOD (each command runs separately, matches auto-approve patterns)

Check pod status:
```bash
kubectl get pods -n kagenti-system
```

Check logs:
```bash
kubectl logs -n kagenti-system deployment/mlflow
```

## BAD (chained commands won't match auto-approve patterns)

```bash
kubectl get pods -n kagenti-system && kubectl logs -n kagenti-system deployment/mlflow
```
```

### Management skills (require approval)
Commands target management clusters, AWS APIs, or perform destructive operations. These can use any command format since the user must approve each one.

## How to Validate

### Single Skill

```bash
# Check frontmatter
head -5 .claude/skills/<skill>/SKILL.md

# Check name matches directory
DIR_NAME=$(basename $(dirname .claude/skills/<skill>/SKILL.md))
SKILL_NAME=$(grep '^name:' .claude/skills/<skill>/SKILL.md | sed 's/name: //')
[ "$DIR_NAME" = "$SKILL_NAME" ] && echo "OK" || echo "MISMATCH: dir=$DIR_NAME name=$SKILL_NAME"
```

### All Skills

```bash
# Check all frontmatter name-vs-directory
for f in .claude/skills/*/SKILL.md; do
  dir=$(basename $(dirname "$f"))
  name=$(grep '^name:' "$f" | sed 's/name: //' | tr -d ' ')
  [ "$dir" = "$name" ] || echo "MISMATCH: $dir != $name"
done
```

### Check Command Format (sandbox skills)

```bash
# Find chained commands in sandbox skills (potential auto-approve issues)
grep -n ' && ' .claude/skills/k8s:*/SKILL.md .claude/skills/kagenti:*/SKILL.md .claude/skills/kind:*/SKILL.md .claude/skills/local:*/SKILL.md .claude/skills/tdd:*/SKILL.md .claude/skills/rca:*/SKILL.md
```

### Check Mermaid Diagram Presence

```bash
for f in .claude/skills/*/SKILL.md; do
  dir=$(basename $(dirname "$f"))
  case "$dir" in git|k8s|auth|openshift|local|kind|helm|meta|genai|repo|testing) continue ;; esac
  if ! grep -q '```mermaid' "$f"; then
    echo "MISSING DIAGRAM: $dir"
  fi
done
```

### Verify settings.json Coverage

For each command in a sandbox skill, verify it matches a pattern in `.claude/settings.json`:

| Command prefix | settings.json pattern |
|----------------|----------------------|
| `kubectl get` | `Bash(kubectl get:*)` |
| `kubectl describe` | `Bash(kubectl describe:*)` |
| `kubectl logs` | `Bash(kubectl logs:*)` |
| `helm list` | `Bash(helm list:*)` |
| `KUBECONFIG=~/clusters/hcp/... kubectl` | `Bash(KUBECONFIG=*/clusters/hcp/kagenti-hypershift-custom-*/auth/kubeconfig kubectl:*)` |
| `uv run pytest` | `Bash(uv run pytest:*)` |

If a command is NOT covered, add the pattern to `.claude/settings.json` in the `allow` array.

## Task Tracking

When validating multiple skills:

```
TaskCreate: "kagenti | skills | <category> | Verify | Validate <skill-name>"
```

## Related Skills

- `skills:write` - Create new skills following the standard
- `skills:retrospective` - Review session to identify skill improvements
