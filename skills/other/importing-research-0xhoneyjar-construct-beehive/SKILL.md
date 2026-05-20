---
name: importing-research
description: Bulk convert legacy user research profiles to UTC (User Truth Canvas) format. Use when migrating existing research from grimoires/pub/research/users/ to laboratory.
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Edit
---

# Importing Research

Bulk migrate legacy user research profiles to the User Truth Canvas (UTC) format with automatic JTBD classification and learning status inference.

---

## Trigger

```
/import-research
/import-research --user {username}
/import-research --dry-run
```

**Examples:**
```bash
/import-research                    # Migrate all pending users
/import-research --user ncs         # Migrate single user
/import-research --dry-run          # Preview without writing
```

---

## Workflow

### Step 1: Scan Source Directory

Find all legacy user profiles:
```bash
grimoires/pub/research/users/*.md
```

Compare against existing UTCs:
```bash
grimoires/observer/canvas/*.md
```

Build list of pending migrations.

### Step 2: Parse Legacy Format

For each legacy file, extract:

**1. User Profile:**
- Username (from filename)
- Type (if documented)
- Status
- Community/segment

**2. Key Quotes:**
- Direct quotes with `> "..."` syntax
- Source (Discord, survey, DM) if noted
- Dates if available

**3. Goals/Pain Points:**
- Validated Behaviors section
- Insights Contributed

**4. Notes:**
- Any additional context

### Step 3: Infer JTBD

Map extracted data to JTBD taxonomy based on signal patterns:

| Signal Pattern | JTBD Label |
|----------------|------------|
| "checking", "verifying", "confirm" | `[J] Reassure Me This Is Safe` |
| "understand", "how does", "explain" | `[J] Find Information` |
| "confused", "unclear", "don't know" | `[J] Help Me Feel Smart` |
| "set and forget", "automatic", "passive" | `[J] Give Me Peace of Mind` |
| "waiting", "anxious", "stressed" | `[J] Reduce My Anxiety` |
| "deposit", "claim", "stake", "withdraw" | `[J] Make Transaction` |
| "organize", "manage", "sort" | `[J] Organize Assets` |
| "show off", "status", "badge" | `[J] Help Me Look Smart, Cool` |
| "insider", "exclusive", "alpha" | `[J] Help Me Feel Like An Insider` |
| "express", "identity", "customize" | `[J] Let Me Express My Identity` |

Select primary JTBD from strongest signal. Secondary if multiple strong signals.

### Step 4: Determine Learning Status

Based on evidence strength:

| Evidence Level | Learning Status |
|----------------|-----------------|
| Single quote, one user | `smol-evidence` |
| Multiple quotes, same theme | `directionally-correct` |
| 5+ users expressing same need | `strongly-validated` |
| Insight marked as "Validated" in tracker | `strongly-validated` |

Cross-reference with `grimoires/observer/tracker.md` for validated insights.

### Step 5: Generate UTC File

Create file at `grimoires/observer/canvas/{username}.md`:

```markdown
---
type: user-truth-canvas
user: {username}
created: "{ISO-8601}"
updated: "{ISO-8601}"
learning_status: {smol-evidence|directionally-correct|strongly-validated}
source: {team-internal|dm-to-team|analytics|discord-support}
jtbd_primary: "[J] {label}"
jtbd_secondary: "[J] {label}" | null
linked_journeys: []
linked_issues: []
migrated_from: "grimoires/pub/research/users/{username}.md"
---

# {username} — User Truth Canvas

## 1. Qualitative Evidence

> "{quote 1}"
> — {source}, {date}

> "{quote 2}"
> — {source}, {date}

---

## 2. Quantitative Evidence

| Metric | Value | Source |
|--------|-------|--------|
| Insights contributed | {N} | tracker.md |

*Additional quantitative data if available*

---

## 3. The User Story

**Who**: {User type, segment, community}

**Where**: {Part of product/journey - inferred from quotes}

**When**: {Trigger moment - inferred from quotes}

---

## 4. Inferred Job-To-Be-Done

**Primary**: `[J] {label}` — {One sentence explanation}

**Secondary**: `[J] {label}` — {One sentence explanation} *(if applicable)*

---

## 5. Expectation Gap

| Expected (User Reality) | Actual (Code Reality) | Gap Type | File:Line | Resolution |
|-------------------------|----------------------|----------|-----------|------------|
| {From quotes if evident} | *pending /ground* | TBD | — | pending |

---

## Linked Artifacts

- Legacy Profile: `grimoires/pub/research/users/{username}.md`
- Tracker Insights: {list insight numbers if referenced}
```

### Step 6: Update State

Update `grimoires/observer/state.yaml`:

```yaml
canvases:
  {username}:
    format: utc
    created: "{timestamp}"
    updated: "{timestamp}"
    quotes_count: {n}
    jtbd_primary: "[J] {label}"
    learning_status: {status}
    linked_journeys: []
    migrated_from: "grimoires/pub/research/users/{username}.md"

migration:
  completed:
    - {username}
  pending: []  # Remove migrated users
  last_run: "{timestamp}"
```

### Step 7: Report Output

```
Import Research Complete

Source: grimoires/pub/research/users/
Users Found: {N}
Already Migrated: {N}
New Imports: {N}

Migration Summary:
┌────────────────┬─────────────────────┬──────────────────┬────────────────┐
│ User           │ Status              │ JTBD (Primary)   │ Learning Status│
├────────────────┼─────────────────────┼──────────────────┼────────────────┤
│ ncs            │ ✓ Imported          │ [J] Find Info    │ validated      │
│ adeitasuna     │ ✓ Imported          │ [J] Reduce Anx   │ directional    │
│ turingog       │ ⊘ Already exists    │ -                │ -              │
│ ...            │ ...                 │ ...              │ ...            │
└────────────────┴─────────────────────┴──────────────────┴────────────────┘

UTCs created: grimoires/observer/canvas/

Next steps:
- Review migrated UTCs for accuracy
- Run /shape to update journeys
- Run /ground to populate Code Reality columns
```

---

## Dry Run Mode

With `--dry-run`, show what would be created without writing:

```
[DRY RUN] Would migrate 9 users:

1. ncs
   - JTBD: [J] Find Information
   - Status: strongly-validated (9 insights)
   - Quotes: 15

2. adeitasuna
   - JTBD: [J] Reduce My Anxiety
   - Status: directionally-correct
   - Quotes: 3

...

No files written. Remove --dry-run to execute.
```

---

## Migration Priority

From PRD, migrate in priority order:

| Priority | User | Insight Count | Reason |
|----------|------|---------------|--------|
| 1 | ncs | 9 | Highest insight contribution |
| 2 | adeitasuna | 2 | Multiple insights |
| 3 | satanelrudo | 1 | Insight contributor |
| 4 | madcopi79 | 1 | Insight contributor |
| 5+ | Others | 0-1 | Complete coverage |

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Legacy file not found | Skip with warning |
| UTC already exists | Skip (don't overwrite) unless `--force` |
| Parse error | Log error, continue with others |
| No quotes found | Create minimal UTC with note |
| JTBD unclear | Default to `[J] Find Information` |

---

## Validation

After migration:
- [ ] All UTC files have valid YAML frontmatter
- [ ] Quotes preserved exactly from source
- [ ] JTBD assigned with rationale
- [ ] Learning status matches evidence level
- [ ] state.yaml updated with all canvases
- [ ] No data lost from legacy files

---

## Related

- `/observe` - Create/update individual canvases
- `/shape` - Extract journeys from canvases
- `tracker.md` - Insight validation reference
