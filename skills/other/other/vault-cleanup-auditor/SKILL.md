---
name: vault-cleanup-auditor
description: Audit your Obsidian vault in Claude Code — finds stale drafts, empty folders, duplicate filenames, and incomplete files. Saves a dated report.
---

# Vault Cleanup Auditor

Runs 4 targeted checks against your Obsidian vault and saves a prioritized audit report to `vault-audit/YYYY-MM-DD-audit.md`. Takes under 30 seconds. No APIs, no paid services.

Run it monthly or whenever the vault starts feeling messy.

---

## How to Use

Open Claude Code and say:

```
Run the Vault Cleanup Auditor skill against my vault at /path/to/vault.
```

---

## Skill Instructions (for Claude Code)

When this skill is invoked, follow these phases exactly.

---

### PHASE 1: INTAKE

Check whether the user has provided:
- `vault_path` — absolute path to their Obsidian vault root

**If missing, ask:**

```
What's the absolute path to your Obsidian vault? (e.g. /root/obsidian-vault)
```

Do not proceed until confirmed.

---

### PHASE 2: ANALYZE

Run all 4 checks. Capture raw output from each before writing the report.

**Check 1 — Stale drafts (30+ days, unposted):**

```bash
VAULT="VAULT_PATH_HERE"
echo "=== CHECK 1: STALE DRAFTS ==="
find "$VAULT/content/ready-to-post" -name "*.md" -mtime +30 2>/dev/null | while read f; do
  if grep -q '\*\*Posted:\*\* ❌' "$f" 2>/dev/null; then
    days=$(( ($(date +%s) - $(stat -c %Y "$f")) / 86400 ))
    echo "${days}d|${f##$VAULT/}"
  fi
done
echo "=== END CHECK 1 ==="
```

**Check 2 — Incomplete files (no headings, 5+ lines):**

```bash
VAULT="VAULT_PATH_HERE"
echo "=== CHECK 2: INCOMPLETE FILES ==="
find "$VAULT" -name "*.md" \
  -not -path "*/.git/*" \
  -not -path "*/.obsidian/*" \
  -not -path "*/.openclaw/*" | while read f; do
  if ! grep -qE '^#{1,6} ' "$f" 2>/dev/null; then
    lines=$(wc -l < "$f")
    if [ "$lines" -gt 5 ]; then
      echo "${lines}lines|${f##$VAULT/}"
    fi
  fi
done
echo "=== END CHECK 2 ==="
```

**Check 3 — Duplicate filenames:**

```bash
VAULT="VAULT_PATH_HERE"
echo "=== CHECK 3: DUPLICATE FILENAMES ==="
find "$VAULT" -name "*.md" \
  -not -path "*/.git/*" \
  -not -path "*/.obsidian/*" \
  -not -path "*/.openclaw/*" \
  -printf "%f\n" | sort | uniq -d | while read name; do
  echo "DUPE:$name"
  find "$VAULT" -name "$name" \
    -not -path "*/.git/*" \
    -not -path "*/.obsidian/*" | while read f; do
    echo "  PATH:${f##$VAULT/}"
  done
done
echo "=== END CHECK 3 ==="
```

**Check 4 — Empty folders:**

```bash
VAULT="VAULT_PATH_HERE"
echo "=== CHECK 4: EMPTY FOLDERS ==="
find "$VAULT" -type d -empty \
  -not -path "*/.git/*" \
  -not -path "*/.obsidian/*" \
  -not -path "*/.openclaw/*" | while read d; do
  echo "${d##$VAULT/}/"
done
echo "=== END CHECK 4 ==="
```

---

### PHASE 3: OUTPUT

**3a. Create the report directory and file:**

```bash
VAULT="VAULT_PATH_HERE"
DATE=$(date +%Y-%m-%d)
mkdir -p "$VAULT/vault-audit"
REPORT="$VAULT/vault-audit/${DATE}-audit.md"
echo "Report path: $REPORT"
```

**3b. Write the report** using this exact structure:

```markdown
# Vault Cleanup Audit — YYYY-MM-DD

Generated: YYYY-MM-DD HH:MM

**Summary:** 🔴 [N] stale | 🟡 [N] incomplete | 🟡 [N] dupes | 🟢 [N] empty

---

## 🔴 Stale Drafts (30+ days, unposted)

- [Nd old] path/to/file.md
[cap at 15 items — add "...and N more" if over]

## 🟡 Incomplete Files (no headings, 5+ lines)

- path/to/file.md (N lines)
[cap at 15]

## 🟡 Duplicate Filenames

- **filename.md**
  - path/one/filename.md
  - path/two/filename.md
[cap at 15 duplicate names]

## 🟢 Empty Folders

- path/to/folder/
[cap at 15]

---

**What to do:**
- 🔴 Stale drafts: post them, delete them, or archive to `content/posted/`
- 🟡 Incomplete files: finish or trash
- 🟡 Duplicates: merge or rename the less important one
- 🟢 Empty folders: safe to delete (or keep if you're about to use them)
```

**3c. Print the summary to terminal:**

```
✅ Audit saved to: vault-audit/YYYY-MM-DD-audit.md

Summary:
🔴 [N] stale drafts
🟡 [N] incomplete files
🟡 [N] duplicate filenames
🟢 [N] empty folders
```

---

### PHASE 4: SELF-CRITIQUE

Before finalizing, check:

1. **All 4 checks ran** — Confirm output exists between each `=== CHECK N ===` / `=== END CHECK N ===` marker. If a check produced no output, note "0 issues found" in the report — do not skip the section.
2. **Counts are accurate** — The summary line counts must match the actual items listed in each section. Re-count if unsure.
3. **Report saved correctly** — Confirm the file exists at `vault-audit/YYYY-MM-DD-audit.md`. If the write failed, report the error and provide the report content inline.
4. **No blank sections** — Every section must either list items OR say "No issues found." Never leave a section header with nothing below it.

Fix any failures before delivering the final output.

---

## Example Report

```markdown
# Vault Cleanup Audit — 2026-03-01

Generated: 2026-03-01 08:14

**Summary:** 🔴 3 stale | 🟡 2 incomplete | 🟡 1 dupe | 🟢 2 empty

---

## 🔴 Stale Drafts (30+ days, unposted)

- [47d old] content/ready-to-post/linkedin/2026-01-12-ai-systems-post.md
- [38d old] content/ready-to-post/twitter/2026-01-21-founder-ops.md
- [31d old] content/ready-to-post/newsletter/2026-01-28-tools-roundup.md

## 🟡 Incomplete Files (no headings, 5+ lines)

- bambf/research/untitled-notes.md (23 lines)
- thinking/random-thoughts.md (11 lines)

## 🟡 Duplicate Filenames

- **README.md**
  - bambf/brand/README.md
  - bambf/tracking/README.md

## 🟢 Empty Folders

- content/queue/rejected/
- bambf/clients/archived/

---

**What to do:**
- 🔴 Stale drafts: post them, delete them, or archive to `content/posted/`
- 🟡 Incomplete files: finish or trash
- 🟡 Duplicates: merge or rename the less important one
- 🟢 Empty folders: safe to delete (or keep if you're about to use them)
```

---

## Requirements

- Claude Code with bash tool access
- Bash + standard Unix tools: `find`, `grep`, `wc`, `stat`, `date`, `awk`
- Read access to vault directory
- Write access to `vault-audit/` inside the vault (auto-created)
- No APIs, no paid services, no external dependencies
