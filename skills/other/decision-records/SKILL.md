---
name: decision-records
description: Creates, supersedes and validates decision records (ADRs) against the convention a collection already follows, instead of imposing a published one. Use when the user wants to record a decision, write an ADR, supersede an existing decision, audit or lint a decisions folder, check that an ADR index is in sync, or asks "why did we decide X". Deduces the filename scheme, section set and status vocabulary from the records already there; ships a validator with an exit code, so the audit is a check and not an opinion.
argument-hint: "[new | supersede <ref> | check [<dir>]]"
allowed-tools: Bash(ls:*), Bash(find:*), Bash(cat:*), Bash(grep:*), Bash(bash:*), Read, Write, Edit
---

# decision-records

Decision records are cheap to write and expensive to trust. The expensive part is the
collection: numbers that collide, an index that stopped matching the directory, a record
that says it was superseded and does not say by what. This skill writes records and,
mainly, **holds a collection to its own convention**.

## What this skill does not do

- **It does not ship a template file into the target repo.** The skeleton is in this file.
  A `template.md` next to the records is a second home for the convention, and two homes
  diverge in silence: the template keeps a section the records dropped a year ago and
  nothing says which one is the convention. The most-installed prior art
  (`affaan-m/ECC`, `skills/architecture-decision-records`) creates one; this is a
  deliberate departure, not an oversight.
- **It does not check for private tokens.** Hostnames, instance names, IP ranges and
  personal identity belong to the `privacy-guard` skill, whose denylist is gitignored on
  purpose. Duplicating that list here would put the same list in two places, which is the
  failure above with worse consequences. The `--portable` check covers only what breaks
  when a record is **copied**: absolute paths, and links that climb out of the collection.
- **It does not rewrite an accepted record to change its mind.** See *Superseding*.

## Step 0, always: read the collection before writing anything

Find the collection. The three defaults in the wild are all different, so look, do not
assume: `doc/adr` (adr-tools), `docs/adr` (the ECC skill), `docs/decisions` (MADR 4.0.0).

```sh
bash "${CLAUDE_PLUGIN_ROOT}/skills/decision-records/scripts/check-decisions.sh" <dir>
```

Its first block reports what the collection does: filename scheme, where the status lives,
the status vocabulary in use, the sections most records carry, and the index. **That report
is the convention.** Everything you write next matches it, including the parts you would
have written differently.

If the collection is empty or does not exist, ask once, and offer both schemes:

| Scheme | Gains | Costs |
|---|---|---|
| `NNNN-slug.md` **(recommend this one)** | a short reference you can say out loud: "see 0007" | two parallel PRs both take the next number and both merge ([adr/madr#28](https://github.com/adr/madr/issues/28), open since 2020, no convention adopted); breaks on copy between repos and on reordering |
| `YYYY-MM-DD-slug.md` | no collision between parallel PRs, survives a copy into another repo, sorts correctly | no short reference: you cite a record by its whole filename |

Recommend the numbered scheme unless the repo takes decisions through parallel PRs, which
is the case the date scheme was invented for (`log4brains` adopted it in that thread for
exactly this reason). Nothing else about the record changes with the choice.

## Creating a record

1. **Draft, do not write.** Compose the record and show it in the conversation.
2. **Wait for explicit approval.** "Looks good", "yes, write it". Silence is not approval.
   If the user declines, discard it: write nothing, leave no file behind.
3. **Write** it to the collection, named for the deduced scheme, numbered `max + 1` when the
   scheme is numbered (never reuse a number, not even of a deleted record).
4. **Update the index** in the same turn, if the collection keeps one. A record written and
   not indexed is the defect the `INDEX` check exists to catch; do not create it and then
   report it.
5. **Re-run the validator.** It is the only thing that tells you the write landed inside the
   convention rather than beside it.

The skeleton, for a collection that has none to deduce. Sections adapt to the collection's
own set when there is one:

```markdown
# NNNN. <decision in a short noun phrase>

## Status

proposed

## Context

What forced a decision now. The constraints, the pressure, what was true at the time.
Not the solution.

## Decision

What we do, in the present tense: "We use X". One or two sentences.

## Consequences

What gets easier, what gets harder, what we now owe. Both directions, honestly: a record
with only benefits documents an advert, not a decision.
```

Two rules about content, from Nygard's original and worth keeping: write **why**, because
the what is already visible in the code; and record the alternative that was rejected and
the reason, because the next person will otherwise re-propose it.

## Superseding

An accepted record is a statement about a moment. **Never edit one to change its mind** —
that destroys the only evidence of why the old decision made sense, and the record's whole
value is that evidence.

1. Write a new record (the flow above), whose Status references the old one.
2. Change the **old** record's status to `superseded by <new ref>`, and nothing else in it.
3. Update the index for both.

Use the reference form the collection already uses. The validator resolves markdown links
(`[0009](0009-slug.md)`), `ADR-0009`, and a bare number, and reports one that resolves to
nothing. A bare number is only resolvable where the filename scheme carries one; under a
dated or free-form scheme records cite each other by filename, and the validator says it
left those references unchecked rather than calling them all dangling.

## Validating

```sh
check-decisions.sh [--require "A,B"] [--status "a,b"] [--portable] DIR
# 0 clean, 1 violations, 2 usage error or nothing to check
```

Eight checks, each printing a stable code so the reason is readable and greppable:

| Code | What it catches |
|---|---|
| `NAME` | a filename outside the scheme the other records use, or a collection that agrees on no scheme at all. Four schemes are recognised: `YYYY-MM-DD-slug.md`, `NNNN-slug.md`, `<prefix>-NNN-slug.md`, and free-form |
| `SECTION` | a section missing from a record that more than half the collection carries |
| `STATUS` | a record with no status, in a collection whose other records have one. Four forms are read: frontmatter `status:`, a `- Status:` bullet, `**Status**:`, a `## Status` section. When **no** record has one, that is not eight violations, it is one line in *checks that did not run* |
| `DRIFT` | one status spelled two ways: `Accepted` beside `accepted` |
| `SUPERSEDE` | a reference that resolves to nothing, or a status claiming supersession that names no replacement |
| `DUPLICATE` | two records claiming one identifier, where the scheme carries one (`NNNN-slug.md`, `ADR-031-slug.md`); under a dated or free-form scheme the whole filename is the identifier and cannot collide |
| `INDEX` | the index and the directory disagreeing, **in either direction** |
| `PORTABLE` | with `--portable`: absolute paths, and links that climb out of the collection |

Three deliberate properties:

- **A check that cannot apply says so.** Every run ends with *checks that did not run* on
  stderr, naming each check and why. Without it a reader sees `OK: no violations` and has
  no way to know how many of the eight were in a position to say anything, and silence
  reads as a pass. Two shipped defects came from exactly that gap.
- **Nothing is imposed.** The required sections are the ones most records already have, the
  filename scheme is the one most records already use. `--require` and `--status` are there
  for a collection that wants to be held to something stricter than its current habits, and
  they are the only way a rule enters that the collection is not already following.
- **An empty directory exits 2, not 0.** A clean verdict over zero records reads as "clean"
  to anyone checking the exit code, which is how a guard stops guarding while staying
  installed.

When the user asks "why did we decide X", read the index first, then the matching records,
and answer from Context and Decision. If nothing matches, say so and offer to record one.

## Auditing a collection for private tokens

Not this skill's job, and not duplicated here. If `privacy-guard` is set up in the repo, its
denylist is the list:

```sh
grep -n -i -E -f <(grep -vE '^[[:space:]]*(#|$)' .local/privacy-denylist.txt) <dir>/*.md
```

`check_privacy.sh` itself reads `git diff --cached`, so it covers a record on its way into a
commit but not one already sitting in the tree. Its own skill names that limit and says to
grep the tracked tree against the denylist by hand for an audit; the line above is one way
to do that, written here rather than there.

## Important rules

- **ALWAYS** run the validator and read its convention report before writing a record.
- **ALWAYS** get explicit approval before writing a record to disk, and write nothing when
  the user declines.
- **ALWAYS** update the index in the same turn as the record.
- **NEVER** create a `template.md` in the target repo.
- **NEVER** edit an accepted record to change the decision; supersede it.
- **NEVER** reuse an identifier, including one freed by deleting a record.
- **NEVER** report a collection as clean on an exit code you did not look at: the validator
  exits 2 when it had nothing to check, and 2 is not 0.
