---
name: meeting-prep-cc
description: Generate a pre-meeting prep brief in Claude Code. Researches participants, pulls vault context, builds agenda, surfaces sharp questions. Use when user says "prep for this meeting," "I have a call with," "meeting tomorrow with," or "prep brief for [name/company]."
---

# Meeting Prep (Claude Code Edition)

Generate a meeting prep brief from your Obsidian vault. Researches participants, surfaces vault history, builds a prioritized agenda, and generates sharp questions. No autonomy — you run it, you get your brief.

---

## How to Use

Open Claude Code in your vault directory and say:

```
Run the Meeting Prep skill. Meeting with [name] from [company]. Type: [sales/WRS/strategy/partnership/interview]. Time: [date/time].
```

---

## INTAKE

Check that the user has provided:
- Participant name(s) and company
- Meeting type (WRS / Sales / Strategy / Partnership / Interview / Other)
- Meeting time/date
- Optional: prior notes, last meeting summary

If meeting type is missing, ask:
```
What type of meeting is this?
WRS client / Sales / Strategy / Partnership / Interview / Other
```

---

## ANALYZE

Run these steps in order. Capture all output before formatting the brief.

### Step 1 — Vault Search

```bash
VAULT="${VAULT_PATH:-/root/obsidian-vault}"
NAME="[PARTICIPANT_NAME]"
COMPANY="[COMPANY_NAME]"

echo "=== VAULT CONTEXT ==="
grep -rl "$NAME\|$COMPANY" "$VAULT" \
  --include="*.md" \
  -not -path "*/.git/*" \
  -not -path "*/.obsidian/*" \
  | head -10 | while read f; do
    echo "--- ${f##$VAULT/} ---"
    grep -n "$NAME\|$COMPANY" "$f" | head -5
  done
```

### Step 2 — Prior Meeting Notes

```bash
VAULT="${VAULT_PATH:-/root/obsidian-vault}"
find "$VAULT/bambf/meeting-prep" -name "*.md" 2>/dev/null \
  | xargs grep -l "$NAME\|$COMPANY" 2>/dev/null \
  | sort -r | head -3 | while read f; do
    echo "--- Prior brief: ${f##$VAULT/} ---"
    head -30 "$f"
  done
```

### Step 3 — Open Commitments Check

```bash
VAULT="${VAULT_PATH:-/root/obsidian-vault}"
grep -rn "TODO\|action item\|follow up\|promised" "$VAULT" \
  --include="*.md" \
  -l 2>/dev/null \
  | xargs grep -l "$NAME\|$COMPANY" 2>/dev/null \
  | head -5 | while read f; do
    echo "--- ${f##$VAULT/} ---"
    grep -n "TODO\|action item\|follow up\|promised" "$f" | grep -i "$NAME\|$COMPANY" | head -5
  done
```

---

## OUTPUT

Format the brief using this structure (see `references/brief-template.md`):

```
# Meeting Prep: [Name] | [Date] [Time]

Meeting type: [type]
Their role: [role at company]
Relationship stage: [new / existing / lapsed]

---

WHY THIS MEETING MATTERS
[1-2 sentences on stakes, objective, desired outcome]

3 PRIORITIES FOR THIS CALL
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

CONTEXT FROM VAULT
[Pulled notes, open items, prior commitments — or "No prior history found"]

QUESTIONS TO ASK
1. [Question referencing research]
2. [Question]
3. [Question]
4. [Question]
5. [Question]

WATCH FOR
[Known objections, sensitivities, open loops]

DESIRED OUTCOME
[What does success look like in one sentence?]

NEXT STEP TO PROPOSE
[Specific: "schedule X," "send Y," "agree on Z"]
```

**Then:** Save brief to `bambf/meeting-prep/YYYY-MM-DD-[lastname]-prep.md`

**Then:** Print 3-line summary:
```
WHO: [Name], [role] at [company]
WHY IT MATTERS: [1 sentence]
TOP QUESTION: [The single sharpest question to ask]
```

---

## Reference Files

- `references/brief-template.md` — full brief format
- `references/meeting-types.md` — agenda by meeting type
- `references/question-banks.md` — question sets by context

---

## Requirements

- Claude Code with bash tool access
- Vault with bambf/ structure
- No external APIs required
