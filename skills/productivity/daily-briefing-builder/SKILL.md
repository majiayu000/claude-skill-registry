---
name: daily-briefing-builder
description: Generate a clean morning brief in Claude Code — pulls today's priorities, unposted content, and weather from your vault.
---

# Daily Briefing Builder

Generates a morning brief from your Obsidian vault. Reads today's action file, scans for unposted content, and fetches weather — all inside a Claude Code session.

No APIs. No paid services. No agent autonomy required. You run it, you get your brief.

---

## How to Use

Open Claude Code in your vault directory and say:

```
Run the Daily Briefing Builder skill.
```

Or with context upfront:

```
Run the Daily Briefing Builder skill. My vault is at /path/to/vault and my city is Ann+Arbor.
```

---

## Skill Instructions (for Claude Code)

When this skill is invoked, follow these phases exactly.

---

### PHASE 1: INTAKE

Check whether the user has provided:
- `vault_path` — absolute path to their Obsidian vault
- `city` — city name for weather (wttr.in format, spaces as `+`)

**If either is missing, ask before proceeding:**

```
To run your morning brief, I need two things:
1. Your vault path (e.g. /root/obsidian-vault)
2. Your city for weather (e.g. Ann+Arbor or London)
```

Do not proceed to PHASE 2 until both values are confirmed.

---

### PHASE 2: ANALYZE

Run these shell commands in sequence. Capture all output before formatting.

**Step 1 — Today's actions:**

```bash
TODAY=$(date +%Y-%m-%d)
VAULT="VAULT_PATH_HERE"
ACTIONS_FILE="$VAULT/bambf/tracking/daily-actions/${TODAY}.md"

if [ -f "$ACTIONS_FILE" ]; then
  echo "FILE_FOUND"
  awk '/## Today.s 3 Actions/{found=1; next} found && /^[0-9]/{print} found && /^##/{exit}' "$ACTIONS_FILE"
else
  echo "FILE_MISSING:$ACTIONS_FILE"
fi
```

**Step 2 — Unposted content scan:**

```bash
VAULT="VAULT_PATH_HERE"
READY_DIR="$VAULT/content/ready-to-post"

if [ -d "$READY_DIR" ]; then
  find "$READY_DIR" -name "*.md" -printf "%T@ %p\n" 2>/dev/null \
    | sort -rn | awk '{print $2}' \
    | while read f; do
        if grep -q '\*\*Posted:\*\* ❌' "$f" 2>/dev/null; then
          platform=$(echo "$f" | sed "s|.*/ready-to-post/||" | cut -d'/' -f1)
          title=$(grep -m1 '^[^#\-\*>|` ]' "$f" 2>/dev/null | head -c 100)
          rel="${f##$VAULT/}"
          echo "ITEM|$platform|$rel|$title"
        fi
      done
else
  echo "DIR_MISSING:$READY_DIR"
fi
```

**Step 3 — Weather:**

```bash
curl -s --max-time 5 "wttr.in/CITY_HERE?format=3" || echo "WEATHER_UNAVAILABLE"
```

---

### PHASE 3: OUTPUT

Format and print the brief to the terminal:

```
☀️ Morning Brief — [Weekday, Month Day]

TODAY'S 3 ACTIONS
[numbered actions, or fallback message if file missing]

READY TO POST ([shown] of [total])
[platform] [title] — [relative file path]
...and X more in the pipeline   ← only if total > 5

WEATHER
[wttr.in output or fallback]
```

**Formatting rules:**
- Cap ready-to-post display at **5 items** (newest-modified first)
- If `content/ready-to-post/` doesn't exist: `No ready-to-post folder found`
- If no unposted files: `Content queue is empty`
- If actions file missing: `No actions file for today — create one at bambf/tracking/daily-actions/YYYY-MM-DD.md`
- If weather fails: `Weather unavailable (offline)` — do not abort the brief

---

### PHASE 4: SELF-CRITIQUE

Before delivering, run this internal check. Fix anything that fails — do not deliver until all 4 pass.

1. **Actions accuracy** — Was the actions file found? Did numbered items extract correctly? If the file exists but no items were found, note the potential heading mismatch.
2. **Content completeness** — Count the `ITEM|` lines in Step 2 output. Does the number shown in the brief match? Were any files skipped?
3. **Weather result** — Did curl return valid output? Is the fallback shown if it failed?
4. **Format cleanliness** — No raw bash output. No placeholder text. All three sections present.

---

## Example Output

```
☀️ Morning Brief — Friday, February 28

TODAY'S 3 ACTIONS
1. Finish Q1 content calendar
2. Send invoice to BAMBF client
3. Publish LinkedIn post on AI ops

READY TO POST (5 of 9)
[linkedin] Nobody talks about what happens when your AI system fails... — content/ready-to-post/linkedin/ai-ops-failure.md
[twitter] The overnight ops shift is real. We run Scribe at 2am... — content/ready-to-post/twitter/async-ops.md
[newsletter] AI marketing systems that actually work — content/ready-to-post/newsletter/systems-post.md
[linkedin] Three things I stopped doing after deploying agents — content/ready-to-post/linkedin/stopped-doing.md
[twitter] Founders who ignore async AI ops are about to find out why — content/ready-to-post/twitter/ignore-ops.md
...and 4 more in the pipeline

WEATHER
Ann Arbor: ☀️  +42°F
```

---

## Daily Actions File Format

Expected path: `<vault>/bambf/tracking/daily-actions/YYYY-MM-DD.md`

Expected structure:
```markdown
# Daily Actions — 2026-03-01

## Today's 3 Actions
1. First priority
2. Second priority
3. Third priority
```

If you use a different path or heading, tell Claude Code when invoking the skill.

---

## Requirements

- Claude Code with bash tool access
- Vault with `content/ready-to-post/` folder (files must contain `**Posted:** ❌` to register as unposted)
- `curl` installed (weather fails gracefully without it)
- Daily actions file optional — brief still runs without it
