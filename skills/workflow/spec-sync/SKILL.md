---
name: vibe-spec-sync
description: Bidirectional sync between specification documents and code. Detects spec drift from staged changes, updates spec to reflect approved decisions, and ensures every commit represents a reconciled snapshot of spec, tests, and code.
user-invocable: true
---

# vibe-spec-sync

Code changes. Specs don't update themselves. This skill closes the loop.

## When to Use This Skill

- Before committing — detect spec drift from staged changes
- After approving decisions (from `vibe-decision-journal`) — sync them back to spec
- When `vibe-spec-vs-code-audit` found gaps — fix them
- Periodically — ensure spec still reflects reality

## When NOT to Use This Skill

- No spec exists (write one first, or use `vibe-doc-quality-gate` to bootstrap)
- Prototype/spike code with no spec commitment
- Spec is explicitly labeled as aspirational/future-state

## Prerequisites

The project must have:
- A specification document (markdown) — configured in step 1
- Implementation code that the spec describes
- Optionally: a test suite with requirement traceability markers (`# req:[ID]`)

## Steps

### Step 1: Locate Spec and Code

1. **Find the spec** — Look for:
   - `spec.md`, `SPEC.md`, `*_spec.md` in project root or `docs/`
   - Design docs in `docs/design/`, `docs/architecture/`
   - Ask user if ambiguous: "Which document is the authoritative spec?"

2. **Find the implementation** — The code files the spec describes

3. **Find the decision log** — `docs/decisions/decisions.jsonl` (from `vibe-decision-journal`)

### Step 2: Extract Drift from Staged Changes

Run `git diff --cached` and analyze what changed relative to the spec:

1. **Categorize each change**:
   - **Spec-aligned**: Change matches what the spec says → no action
   - **Spec-extending**: Change adds behavior the spec doesn't mention → spec needs new section
   - **Spec-modifying**: Change alters behavior the spec describes differently → spec needs update
   - **Spec-contradicting**: Change violates what the spec explicitly forbids → flag for review

2. **For each drift item, produce**:
   ```
   DRIFT-[NNN]:
     Type: extending | modifying | contradicting
     Spec section: "## [Header]"
     Current spec says: "[quoted text]"
     Code now does: "[description of new behavior]"
     Suggested spec update: "[proposed new text]"
   ```

3. **Present drift items** to the user via `AskUserQuestion`:
   - **Approve update** — update the spec to match the code
   - **Approve with edits** — user refines the proposed spec text
   - **Reject** — the code is wrong; flag for fix (do NOT update spec)
   - **Defer** — not ready to decide; skip for now

### Step 3: Apply Spec Updates

For each approved drift item:

1. **Find the target section** in the spec:
   - Match by exact header first
   - Fall back to normalized match (case-insensitive, whitespace-collapsed)
   - If no matching section, determine correct placement by reading surrounding sections

2. **Apply the update**:
   - For **modifying**: Replace the relevant paragraph/sentence within the section. Use search-and-replace with the old text and new text. Preserve surrounding content.
   - For **extending**: Add new content to the appropriate existing section, or create a new section if the content doesn't fit anywhere.
   - For **contradicting** (approved): Same as modifying — replace the contradicted text.

3. **Preserve spec structure**:
   - Don't rewrite sections that weren't affected
   - Maintain existing formatting, header hierarchy, and ordering
   - Add a brief inline note if a section was significantly changed: `<!-- Updated: [date] per DEC-[NNNN] -->`

4. **Stage the spec changes**: `git add [spec file]`

### Step 4: Verify Consistency

After applying updates:

1. **Re-read the updated spec** — verify it reads coherently (no dangling references, no contradictions between sections)

2. **Cross-check with decision log** — ensure approved decisions from `vibe-decision-journal` are reflected in the spec

3. **Check test coverage** — identify any updated spec sections that now lack test coverage:
   - Scan tests for `# req:[ID]` markers matching affected requirements
   - Report uncovered requirements: "Spec updated but no test covers [requirement]. Consider running `vibe-adversarial-test-generation` in spec-driven mode."

### Step 5: Report

## Output Format

### Spec Sync Report

**Spec**: [path/to/spec.md]
**Staged Changes Analyzed**: [N files, M insertions, K deletions]

| # | Type | Spec Section | Action | Status |
|---|------|-------------|--------|--------|
| 1 | modifying | ## Authentication | Updated: "JWT tokens" → "JWT tokens with 1h expiry" | Approved |
| 2 | extending | (new) ## Rate Limiting | Added new section | Approved |
| 3 | contradicting | ## Data Retention | Flagged: spec says "never delete", code adds TTL | Rejected — code needs fix |
| 4 | extending | ## Error Handling | Deferred | — |

### Spec Changes Applied
- `docs/spec.md`: 2 sections updated, 1 section added
- Linked decisions: DEC-0045, DEC-0046

### Test Coverage After Sync
- Requirements with tests: X/N
- Newly uncovered: `## Rate Limiting` (no tests yet)

### Next Steps
- [ ] Fix rejected drift item #3 (code contradicts spec on data retention)
- [ ] Add tests for `## Rate Limiting` section
- [ ] Run `vibe-spec-vs-code-audit` to verify full alignment

## Integration with Other Skills

- **`vibe-decision-journal`**: Decisions feed into spec sync. When decisions are approved, this skill updates the spec to reflect them.
- **`vibe-spec-vs-code-audit`**: Run after sync to verify no remaining gaps.
- **`vibe-adversarial-test-generation`** (spec-driven mode): Generate tests for requirements that were updated or added during sync.
- **`vibe-coverage-enforcer`**: Verify that test coverage still meets tier targets after spec-driven test additions.
- **`vibe-pre-commit-audit`**: Complementary — that skill checks for secrets/debug code; this skill checks for spec alignment. Both belong in a pre-commit workflow.

## Rules

- **NEVER update the spec without user approval.** Every drift item must be presented and explicitly approved.
- **NEVER silently drop drift items.** If a change affects the spec, report it — even if you think it's minor.
- **Preserve spec authority.** The spec is the source of truth for *intended* behavior. If code contradicts spec and the user rejects the update, the code is wrong — not the spec.
- **Don't rewrite what you didn't change.** Only modify spec sections affected by the current drift. Leave everything else untouched.
- **Link to decisions.** When a spec update corresponds to a recorded decision, add the decision ID as an HTML comment: `<!-- DEC-NNNN -->`
