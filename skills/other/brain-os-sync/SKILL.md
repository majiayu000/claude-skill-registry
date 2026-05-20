---
name: brain-os-sync
description: "Sync new or updated skills to the brain-os GitHub repository. Run this after creating or modifying any skill. Pushes SKILL.md files from .claude/skills/ to github.com/dgnernvsinjsbt/brain-os."
allowed-tools: Bash, Read, Glob
---

# Brain-OS Skill Sync

Pushes new and updated skills from the local `.claude/skills/` directory to the remote `dgnernvsinjsbt/brain-os` GitHub repository.

## When to Use

- After creating a new skill with `/skill-creator`
- After modifying an existing skill
- To verify which local skills are missing from brain-os

---

## Required Environment Variable

Token must exist in `.env` (never hardcode):

```
GIT_ACC_dgnernvsinjsbt_TOKEN=ghp_...
```

Read it with:
```bash
source .env 2>/dev/null || source /workspaces/ZeroKlik/.env
export GH_TOKEN=$GIT_ACC_dgnernvsinjsbt_TOKEN
```

---

## Workflow

```
Load Token → Discover Local Skills → Compare Remote → Push Diff → Report
```

### Phase 1: Load Token

```bash
# Find .env — check CWD first, then workspace root
ENV_FILE=".env"
[ ! -f "$ENV_FILE" ] && ENV_FILE="/workspaces/ZeroKlik/.env"
[ ! -f "$ENV_FILE" ] && { echo "ERROR: .env not found"; exit 1; }

export GH_TOKEN=$(grep 'GIT_ACC_dgnernvsinjsbt_TOKEN' "$ENV_FILE" | cut -d'=' -f2 | tr -d '\r\n')
[ -z "$GH_TOKEN" ] && { echo "ERROR: GIT_ACC_dgnernvsinjsbt_TOKEN not set in .env"; exit 1; }

REPO="dgnernvsinjsbt/brain-os"
REMOTE_BASE="skills"
```

### Phase 2: Discover Local Skills

```bash
# Find all local skills (directories with SKILL.md)
LOCAL_SKILLS=$(find .claude/skills -name "SKILL.md" -not -path "*/shared/*" | sort)

echo "Found $(echo "$LOCAL_SKILLS" | wc -l) local skills"
```

### Phase 3: Compare with Remote

```bash
# Get list of skills already in brain-os
REMOTE_SKILLS=$(GH_TOKEN=$GH_TOKEN gh api repos/$REPO/contents/$REMOTE_BASE --jq '.[].name' 2>/dev/null | sort)

# Find missing/new skills
for skill_path in $LOCAL_SKILLS; do
  skill_name=$(echo "$skill_path" | sed 's|.claude/skills/||' | sed 's|/SKILL.md||')
  if ! echo "$REMOTE_SKILLS" | grep -q "^${skill_name}$"; then
    echo "NEW: $skill_name"
  fi
done
```

### Phase 4: Push New/Updated Skills

For each skill to sync, use the GitHub Contents API:

```bash
push_skill() {
  local skill_name="$1"
  local local_path=".claude/skills/${skill_name}/SKILL.md"
  local remote_path="${REMOTE_BASE}/${skill_name}/SKILL.md"

  # Encode content
  CONTENT=$(base64 -w 0 < "$local_path")

  # Check if file already exists (need SHA for update)
  EXISTING=$(GH_TOKEN=$GH_TOKEN gh api repos/$REPO/contents/$remote_path 2>/dev/null)
  SHA=$(echo "$EXISTING" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sha',''))" 2>/dev/null)

  if [ -n "$SHA" ]; then
    # Update existing file
    GH_TOKEN=$GH_TOKEN gh api repos/$REPO/contents/$remote_path \
      --method PUT \
      --field message="feat: update skill ${skill_name}" \
      --field content="$CONTENT" \
      --field sha="$SHA" \
      --jq '.content.name' && echo "UPDATED: $skill_name"
  else
    # Create new file
    GH_TOKEN=$GH_TOKEN gh api repos/$REPO/contents/$remote_path \
      --method PUT \
      --field message="feat: add skill ${skill_name}" \
      --field content="$CONTENT" \
      --jq '.content.name' && echo "CREATED: $skill_name"
  fi
}
```

### Phase 5: Report

Print summary table:

```
Brain-OS Sync Complete
======================
CREATED : youtube-transcript
UPDATED : brain-os-sync
SKIPPED : 142 skills (already up to date)

Repo: https://github.com/dgnernvsinjsbt/brain-os/tree/main/skills
```

---

## Full Script (copy-paste ready)

```bash
#!/bin/bash
set -e

ENV_FILE=".env"
[ ! -f "$ENV_FILE" ] && ENV_FILE="/workspaces/ZeroKlik/.env"
[ ! -f "$ENV_FILE" ] && { echo "ERROR: .env not found"; exit 1; }

export GH_TOKEN=$(grep 'GIT_ACC_dgnernvsinjsbt_TOKEN' "$ENV_FILE" | cut -d'=' -f2 | tr -d '\r\n')
[ -z "$GH_TOKEN" ] && { echo "ERROR: GIT_ACC_dgnernvsinjsbt_TOKEN not set in .env"; exit 1; }

REPO="dgnernvsinjsbt/brain-os"
REMOTE_BASE="skills"
CREATED=0
UPDATED=0
SKIPPED=0

for skill_dir in .claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  local_path="${skill_dir}SKILL.md"

  [ ! -f "$local_path" ] && continue
  [ "$skill_name" = "shared" ] && continue

  CONTENT=$(base64 -w 0 < "$local_path")
  remote_path="${REMOTE_BASE}/${skill_name}/SKILL.md"

  EXISTING=$(gh api repos/$REPO/contents/$remote_path 2>/dev/null || echo "")
  SHA=$(echo "$EXISTING" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sha',''))" 2>/dev/null || echo "")

  if [ -n "$SHA" ]; then
    # Check if content differs
    REMOTE_CONTENT=$(echo "$EXISTING" | python3 -c "import sys,json; print(json.load(sys.stdin).get('content',''))" 2>/dev/null | tr -d '\n')
    LOCAL_B64=$(base64 -w 76 < "$local_path" | tr -d '\n')

    if [ "$REMOTE_CONTENT" = "$LOCAL_B64" ]; then
      SKIPPED=$((SKIPPED + 1))
      continue
    fi

    gh api repos/$REPO/contents/$remote_path \
      --method PUT \
      --field message="feat: update skill ${skill_name}" \
      --field content="$CONTENT" \
      --field sha="$SHA" \
      --jq '.content.name' > /dev/null && echo "UPDATED: $skill_name"
    UPDATED=$((UPDATED + 1))
  else
    gh api repos/$REPO/contents/$remote_path \
      --method PUT \
      --field message="feat: add skill ${skill_name}" \
      --field content="$CONTENT" \
      --jq '.content.name' > /dev/null && echo "CREATED: $skill_name"
    CREATED=$((CREATED + 1))
  fi
done

echo ""
echo "Brain-OS Sync Complete"
echo "CREATED : $CREATED | UPDATED : $UPDATED | SKIPPED : $SKIPPED"
echo "https://github.com/$REPO/tree/main/$REMOTE_BASE"
```

---

## Modes

| Mode | When to use |
|------|-------------|
| Default (new only) | After creating one new skill — just push that skill via `push_skill skill-name` |
| Full sync | Run the full script to sync all skills including updates |
| Dry run | Add `echo` before each `gh api` call to preview without pushing |

---

## Notes

- `shared/` directory is always skipped (internal helpers, not standalone skills)
- The script compares base64 content to avoid unnecessary API calls
- Token scopes needed: `repo` (read + write contents)
- `gh` CLI must be available (`which gh`)
