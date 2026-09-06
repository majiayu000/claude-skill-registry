---
name: map-corpus
description: 'Use when the user points to a study-material folder and asks to make it teachable. Not for remote, credential, publish, deploy, or irreversible changes.'
---

# Map corpus

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user explicitly points to a folder of their study material and asks to make that material teachable. |
| Authority | Reversible local: writes only `CORPUS.md` at the workspace root; rollback is restoring the prior file or deleting a newly created one. No remote mutation. Do not change files under the corpus root. |
| Side effect | Create or wholly replace the workspace-root `CORPUS.md`; rollback is deletion of a newly created file or restoration of the prior file. |
| Done | `CORPUS.md` inventories every readable file, marks every unreadable file, names the concepts taught, cites their source locations, and orders concepts so each prerequisite precedes its dependent or any cycle is disclosed on the dependent's line. |

## Inputs

- Required: the corpus folder path and the workspace root where `CORPUS.md` will be written. If the corpus path is missing, request it once and stop as blocked if it remains unavailable.
- Optional: an existing `CORPUS.md`, which may be replaced only after the new map is complete. No other prior artifact is required.

## Procedure

1. Expand `~`, resolve the corpus folder to an absolute path, and verify that it exists and is a directory. Fix the corpus root and workspace-root output path before reading or writing. Done when: the corpus root and output path are resolved and verified.
2. Recursively enumerate every file under the corpus root. Attempt to read each without converting it or modifying it. Classify each file as readable or unreadable and retain the reason for every unreadable result. Done when: every file is enumerated and classified with its readability reason.
3. For every readable file, record one source row containing its path relative to the corpus root, its material kind, and either the headings worth citing or `reference only`. The number of source rows must equal the number of readable files. Done when: source row count equals readable file count.
4. Derive the concepts the readable corpus teaches. For each concept, use the source's term where available and record a one-sentence definition, its prerequisites, and at least one citation anchor. Every readable file must contribute a concept or be marked `reference only` in its source row. Done when: every readable file is accounted for as a concept or `reference only`.
5. Form heading citations as `<path-relative-to-corpus-root>#<heading-slug>`. When a source has no headings, use `<path-relative-to-corpus-root>:<start>-<end>`. Do not place absolute paths in source rows or citations. Done when: every citation uses the relative-path form.
6. Order the concepts as one flat numbered list. Put every prerequisite before its dependents. If two concepts depend on each other, place first the one introduced first by the corpus and disclose the cycle on the other concept's line. Merge concepts that the corpus always teaches together when the list would otherwise exceed roughly forty entries. Done when: every prerequisite precedes its dependents and every cycle is disclosed.
7. Build `CORPUS.md` with, in order: `# Corpus: <name>`; `corpus_root: <absolute path>`; `mapped: <YYYY-MM-DD>`; a `## Sources` table with `File`, `Kind`, and `Cite from` columns; a `## Concepts` numbered list whose entries contain the term, definition, `Needs:`, and `Source:`; and a `## Unreadable` list containing each unreadable relative path and reason. Use `Needs: none` for concepts without prerequisites and state `None` when there are no unreadable files. Done when: the file content is assembled in the specified section order.
8. Verify file accounting, concept coverage, citation form, and prerequisite order against the enumerated corpus. Only then write the completed content by wholly replacing workspace-root `CORPUS.md`; never write inside the corpus root. Done when: the verification passes and `CORPUS.md` is written.

## Failure and recovery

- Invalid corpus: if the path is missing, does not exist, or is not a directory, do not write anything; return `blocked` with the failed validation.
- Unreadable members: list each unreadable file and its observed reason, make no conversion attempt or converter recommendation, and complete the map from readable files. This is a valid partial corpus map only when every unreadable file is disclosed.
- Unsafe output boundary: if the resolved output is not exactly workspace-root `CORPUS.md`, or writing it would modify the corpus root, do not write and return `blocked` with both resolved paths.
- Unprovable map: if source accounting, concept coverage, citation anchors, or prerequisite ordering cannot be established from the material, preserve any existing `CORPUS.md`, write no partial replacement, and return `blocked` naming the unmet condition without inventing evidence.
- Write failure: report the write error and do not claim completion. If replacement began but did not complete, restore the prior `CORPUS.md` when available; otherwise remove the incomplete new file.

## Output

On success, return the path to workspace-root `CORPUS.md` and counts for readable sources, unreadable sources, and concepts. The file is the sole artifact and contains the complete source inventory, citation anchors, prerequisite-ordered concept list, and unreadable-file disclosures.
