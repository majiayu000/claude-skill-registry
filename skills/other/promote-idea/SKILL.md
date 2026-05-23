---
name: promote-idea
description: Converts an album idea from IDEAS.md into an actual album project in one step. Use when the user says "promote [idea title]", "turn idea into album", or "start working on [idea]".
argument-hint: <"idea title"> [album-slug-override]
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - bitwize-music-mcp
---

## Your Task

**Input**: $ARGUMENTS

Convert a `Pending` idea from `IDEAS.md` into a full album project in one
call. Replaces the manual 3-step workflow (`get_ideas` → `new-album` →
`update_idea`) with a single entry point.

---

# Promote Idea Skill

## Step 1: Parse Arguments

Expected formats:

- `"<idea title>"` — auto-derive slug from the title
- `"<idea title>" <album-slug>` — override the auto-derived slug
- `"<idea title>" documentary` — standard slug, documentary flag on
- `"<idea title>" <album-slug> documentary` — explicit slug + documentary

Examples:

- `"Kleine Welt"` → slug auto-derived to `kleine-welt`
- `"The Great Molasses Flood" molasses-flood documentary`
- `"Ängstliche Kätzchen"` → slug `angstliche-katzchen` (diacritics stripped)

**If no arguments are supplied, or the title is empty**, list the available
pending ideas first and ask which one to promote:

```
Which idea should I promote?

Pending ideas:
1. Kleine Welt (electronic, Thematic)
2. The Great Molasses Flood (folk, Documentary)
3. Linux Kernel Wars (electronic, Character Study)

Reply with the exact title.
```

Use `get_ideas(status_filter="Pending")` to fetch the list.

## Step 2: Confirm the Derived Slug

Call `get_ideas(status_filter="Pending")` (or `search(query=idea_title, scope="ideas")`)
to confirm the idea exists and show the user what's about to happen.

Compute the slug locally for display only (lowercase, strip diacritics,
non-alphanumeric → hyphen). If the result looks odd, offer to override:

```
About to promote:
  Idea:  Kleine Welt
  Slug:  kleine-welt
  Genre: electronic
  Type:  Thematic

Proceed? (Or supply a different slug.)
```

Skip the confirmation step if the user has already provided an explicit slug
— that's the signal they've already thought about it.

## Step 3: Ask About Documentary Flag (if not already supplied)

The `documentary` flag decides whether `RESEARCH.md` and `SOURCES.md` are
created. This is **not** derivable from idea metadata — the idea's "Type"
field can say "Documentary" but that's a separate concept (narrative shape).
Ask once:

> Is this a documentary/true-story album? (Adds research + sources
> templates. Answer 'yes' for real-world events, 'no' for fiction.)

Skip this step if `documentary` is already in the arguments.

## Step 4: Promote via MCP

Call `promote_idea(idea_title, album_slug=<slug or "">, documentary=<bool>)`.

The tool performs all of:

1. Find the idea in state (error if missing or already promoted)
2. Create the album directory via `create_album_structure`
3. Inject the idea's concept into the new `README.md` under a `## Concept`
   section
4. Advance idea status `Pending` → `In Progress`
5. Add `**Promoted To**: <slug>` back-link to the idea in `IDEAS.md`

The tool returns `{promoted: true, slug, album_path, files, ...}` on
success or `{error: ...}` on failure.

## Step 5: Confirm and Suggest Next Step

On success, report:

```
Promoted "Kleine Welt" → album "kleine-welt"

Location: ~/bitwize-music/artists/bitwize/albums/electronic/kleine-welt/
Files:    README.md, tracks/

Concept block injected into README.md from idea.
Idea status: Pending → In Progress

Next step:
  /bitwize-music:album-conceptualizer

  This walks through the 7 Planning Phases (Vision, Identity, Sonic
  Direction, Structure, Tracks, Content, Approval) to develop the concept
  you just carried over into the album.
```

For documentary albums, add:

```
  Research files also created: RESEARCH.md, SOURCES.md
  Don't forget human source verification before generation.
```

---

## Error Handling

**Idea not found:**

```
Error: Idea "Nonexistent" not found in IDEAS.md.

Check available ideas: /bitwize-music:album-ideas list
```

**Idea already promoted:**

```
Error: Idea "Already Active" is already promoted (status: In Progress).

If you want to rename or re-scaffold, use /bitwize-music:rename on the
existing album instead.
```

**Idea has no genre:**

```
Error: Idea "No Genre" has no **Genre** field in IDEAS.md.

Set the genre first: /bitwize-music:album-ideas edit "No Genre"
```

**Invalid genre:**

```
Error: Invalid genre "xyz" on idea. Not in genres/.

Fix the genre in IDEAS.md, then retry.
```

**Duplicate album slug:**

```
Error: Album "kleine-welt" already exists.

Options:
1. Supply a different slug: /bitwize-music:promote-idea "Kleine Welt" kleine-welt-2
2. Resume the existing album: /bitwize-music:resume kleine-welt
```

---

## Examples

### Simple title

```
/bitwize-music:promote-idea "Kleine Welt"
```

Auto-derives slug `kleine-welt`, asks about documentary flag, calls
`promote_idea`, reports outcome.

### Explicit slug override

```
/bitwize-music:promote-idea "The Great Molasses Flood" molasses-1919
```

Uses `molasses-1919` instead of the auto-derived `the-great-molasses-flood`.

### Documentary album

```
/bitwize-music:promote-idea "The Great Molasses Flood" documentary
```

Creates `RESEARCH.md` and `SOURCES.md` in addition to the standard README
and tracks directory.

---

## Why a Dedicated Skill

The manual workflow required three steps in sequence:

1. `get_ideas` to find the idea's genre
2. `/bitwize-music:new-album <slug> <genre>` with a slug the user invented
3. `update_idea("<title>", "status", "In Progress")`

Problems this skill solves:

- **Concept transfer** — The idea's concept text is now merged into the new
  album README automatically (manual copy/paste used to be skipped often).
- **Status discipline** — Ideas no longer linger as `Pending` after being
  worked on; the transition is automatic and bidirectional (`Promoted To`
  back-link).
- **Slug derivation** — No more re-inventing the slug; diacritics and
  punctuation are normalized consistently.
- **Single entry point** — Newcomers learn one command instead of three.

---

## Remember

1. **Pending-only** — Only `Pending` ideas can be promoted. `In Progress`
   and `Complete` ideas return an error.
2. **One-way operation** — Promotion creates files and updates state. There
   is no "unpromote"; use `/bitwize-music:rename` or manual cleanup if you
   need to redo.
3. **Concept is preserved** — The idea's concept survives in two places
   after promotion: the idea's entry in `IDEAS.md` (historical record) and
   the new album's `README.md` (working document).
4. **Next step is always album-conceptualizer** — Promotion only scaffolds;
   the actual planning happens in the 7 Planning Phases.
