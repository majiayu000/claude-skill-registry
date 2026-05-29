---
name: update-practices
description: Process the practices inbox, evaluate, incorporate into dotforge, and suggest propagation to projects.
---

# Update Practices

3-phase pipeline to keep dotforge up to date with discovered practices.

**Practice sources:**
- Post-session hook (`detect-claude-changes.sh`) → automatic
- Manual capture (`/forge capture`) → user
- For manual web search: research and then use `/forge capture` with the findings

---

## Phase 1: EVALUATE — Process inbox

Read all files in `$DOTFORGE_DIR/practices/inbox/`.

For each practice:

### Acceptance criteria
1. **Is it actionable?** — Can be translated into a concrete change in dotforge
2. **Is it new?** — Does not duplicate something already in `practices/active/`
3. **Is it generalizable?** — Applies to >1 project (not project-specific)
4. **Does it prevent a specific error?** — If yes, annotate `error_type` and error description for tracking in metrics.yml

### Classify
- **Accept** → move to `practices/evaluating/`, note proposed concrete change
- **Reject** → remove from inbox with a note explaining why
- **Defer** → leave in inbox with tag `needs-more-info`

### Priority
1. Security (vulnerabilities, permissions)
2. Breaking changes (APIs that changed)
3. New features that simplify something existing
4. Patterns validated in >1 project
5. Minor optimizations

Show summary:
```
═══ INBOX EVALUATION ═══
{{N}} practices in inbox

✅ ACCEPT: {{title}} → {{proposed change}}
❌ REJECT: {{title}} → {{reason}}
⏸️ DEFER: {{title}} → {{what is missing}}

Proceed with accepted? (yes/no/select)
```

---

## Phase 2: INCORPORATE — Apply changes to dotforge

For each accepted practice in `evaluating/`:

### Determine impact
| Change type | Affected files | Version bump |
|-------------|----------------|--------------|
| New/modified rule | template/rules/, stacks/*/rules/ | minor |
| New/modified hook | template/hooks/, stacks/*/hooks/ | minor |
| Documentation | docs/*.md | patch |
| Modified template | template/*.tmpl | minor |
| Security fix | any | patch |

### Apply
1. Show proposed diff to the user and ask for confirmation
2. Modify the corresponding dotforge files
3. **If the practice warrants a new rule**: generate a `.md` file in `template/rules/` or `stacks/*/rules/` with proper `globs:` (eager) or `paths:` + `alwaysApply: false` (lazy) frontmatter. Only create a rule if the practice is a repeatable constraint (not a one-time fix). Use existing rules as format reference.
4. Move practice from `evaluating/` to `active/` with `incorporated_in:` updated
5. Set frontmatter fields: `effectiveness: monitoring` (or `not-applicable` if no error targeted), `error_type` matching CLAUDE_ERRORS.md types
6. Register in `$DOTFORGE_DIR/practices/metrics.yml`:
   - `error_targeted`: description of the error this practice prevents (null if not error-targeted)
   - `error_type`: syntax | logic | integration | config | security | null
   - `activated`: today's date
   - `status`: monitoring (or not-applicable)
   - `recurrence_checks`: 0
   - `recurrence_target`: 5
7. Update `docs/changelog.md`
8. Bump `VERSION` according to type

---

## Phase 3: PROPAGATE — Suggest project updates

1. Read `$DOTFORGE_DIR/registry/projects.yml`
2. For each project, show what changed since its last sync:

```
═══ SUGGESTED PROPAGATION ═══

project-a (last sync: {{date or "never"}})
  → {{N}} rules updated

project-b (last sync: {{date or "never"}})
  → {{N}} rules updated

To propagate: run /forge sync in each project.
```

DO NOT propagate automatically. Inform only.

---

## Phase 4: VERIFY — Recurrence check for active practices

For each entry in `$DOTFORGE_DIR/practices/metrics.yml` where `status: monitoring`:

1. Read `CLAUDE_ERRORS.md` from each project in registry where the practice is applied
2. Check if any error matching `error_type` + `error_targeted` description was logged AFTER the `activated` date
3. Increment `recurrence_checks` by 1, update `last_checked` to today
4. If error recurred: set `recurred: true`, `status: failed`
5. If `recurrence_checks >= recurrence_target` and `recurred: false`: set `status: validated`
6. Update `effectiveness` field in the practice's frontmatter file to match

Report:
```
═══ EFFECTIVENESS CHECK ═══
{{practice title}} — {{status}} ({{recurrence_checks}}/{{recurrence_target}} checks)
  {{if failed: "⚠ Error recurred — practice needs revision"}}
  {{if validated: "✅ No recurrence after {{N}} checks"}}
  {{if monitoring: "🔍 {{remaining}} checks remaining"}}
```

Skip practices with `status: not-applicable` or `status: validated`.

---

## Final report

```
═══ UPDATE REPORT ═══
Date: {{YYYY-MM-DD}}

Evaluated: {{N}} ({{accepted}} accepted, {{rejected}} rejected, {{deferred}} deferred)
Incorporated: {{N}} into dotforge
Propagation suggested: {{N}} projects

── EFFECTIVENESS ──
Monitoring: {{N}} practices
Validated: {{N}} (no recurrence after {{target}} checks)
Failed: {{N}} (need revision)

VERSION: {{old}} → {{new}}
```
