---
name: repo-cleanup-emberwildgamebible-the-emberwi
description: '- Scan all .md/.lua and list: path, H1 title, category guess, link targets.'
---

# Repo Cleanup Skill

---
name: repo-cleanup
description: Repo-wide cleanup: normalize filenames/titles, relocate by intent, rebuild indexes, fix links, produce audits.
---

## Steps
1) Inventory
- Scan all .md/.lua and list: path, H1 title, category guess, link targets.

2) Fix naming + headers
- Ensure H1 is first non-empty line.
- Filename matches H1 *after* hygiene rules (no ":" and no Windows-invalid chars).
- Replace unicode dashes in filenames with "-".

3) Refile by intent
- Move docs into correct folder. Avoid duplicate canon.
- GameBible stays “design drafts”; systems/specs move to 06_Systems or 10_Documentation.

4) Repair links
- Update markdown links repo-wide to new paths.
- Ensure “See also” targets exist.

5) Rebuild indexes + audits
- Update 00_MASTER_INDEX/* indexes and MASTER_NAV.
- Update BROKEN_LINKS.md with a fresh scan result and date.

## Output
- Summary + counts (moved/renamed/links fixed)
- Touched files list
- Any remaining debt (should be minimal)

## The exact “DO THE BIG CLEANUP” prompt to paste into Codex
This is tuned to what’s in your current repo (especially GameBible/Future/Features):

```
Use $repo-cleanup. Follow AGENTS.md strictly.

TASK: Full repo cleanup for professional structure, clarity, and manageability.

Hard requirements:
1) Cross-platform filenames:
   - Remove ":" from filenames and H1 titles (replace with " - ").
   - Replace Unicode dashes (– —) with ASCII "-" in filenames.
   - Remove any Windows-invalid filename characters.
   - Remove double spaces in filenames.

2) Header ordering:
   - The first non-empty line must be the H1 "# ...".
   - If a doc starts with "Links: ...", move that Links line directly under the H1.

3) GameBible normalization:
   - In GameBible/Future/Features:
     - Rename files to be Windows-safe (especially the ones with ":" and Unicode dashes).
     - Fix all internal links that reference old names.
   - Any real code/prototype modules currently in GameBible (e.g., .lua) must be moved to:
     - 06_Systems/Prototypes/ (or a more specific 06_Systems subfolder),
     - and leave behind a short .md stub in GameBible linking to the new location.

4) Documentation exports cleanup:
   - Clean up 10_Documentation/Indexes/ “Emberwild Game Bible <hash>.md” style files:
     - Rename to a human-readable name,
     - remove junk columns like “nan”,
     - turn them into a clean, linkable index pointing at the actual chapter files.

5) Indexes + nav:
   - Update 00_MASTER_INDEX/MASTER_NAV.md so GameBible and any moved prototype/system docs are discoverable.
   - Update any category indexes impacted by moves/renames.

Deliverables:
- Summary with counts of files renamed/moved and links repaired
- Full list of touched files
- Updated 00_MASTER_INDEX/BROKEN_LINKS.md with a fresh scan date and results
- Update 00_MASTER_INDEX/MOVED_RENAMED_LOG.md with full old→new paths (no truncation)

Do not ask follow-up questions. Make best-effort decisions using folder intent rules; log any uncertainty in 00_MASTER_INDEX/Lore_Debt.md.
```
