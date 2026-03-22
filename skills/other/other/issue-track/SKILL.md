---
name: issue-track
description: Post a status comment on a GitHub issue (starting work, plan update, completed)
argument-hint: <issue-number> <status>
allowed-tools: Bash(gh *)
---

## Track Issue Progress via Comments

Post a status update comment on GitHub issue #$ARGUMENTS.

### Usage

The argument format is: `<issue-number> <status>` where status is one of:
- `start` — Post a "Work started" comment
- `plan` — Post the implementation plan as a comment
- `update <text>` — Post a custom progress update
- `done` — Post a completion comment

### Behavior

**For `start`:**
```bash
gh issue comment <number> --body "$(cat <<'EOF'
🔧 **Work started** on this issue.

Branch: `feature/<number>-<slug>` (will be created shortly)
EOF
)"
```

**For `plan`:**
Read `/tmp/plan-<number>.md` if it exists, and post it as a comment:
```bash
gh issue comment <number> --body "$(cat <<'EOF'
📋 **Implementation Plan**

<contents of /tmp/plan-<number>.md>
EOF
)"
```

**For `update <text>`:**
```bash
gh issue comment <number> --body "$(cat <<'EOF'
📝 **Progress Update**

<text>
EOF
)"
```

**For `done`:**
```bash
gh issue comment <number> --body "$(cat <<'EOF'
✅ **Implementation complete** — PR created and CI checks passing.
EOF
)"
```
