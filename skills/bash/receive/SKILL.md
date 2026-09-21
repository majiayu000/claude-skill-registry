---
name: receive
description: "Register received or authored project documents by confirmed coordinates, preserve their filenames and provenance, and find or verify registered documents. Use for filing a supplied file/package or locating documents by kind, date, source or revision."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:receive

Before acting, read the [host contract](../../docs/host-harness-contract.md), this component's [declaration](host-contract.json) (`skill:receive`), and applicable [workspace semantics](../../docs/workspace-model.md). Load only the required modes from the [shared catalog](../../corpus/host-contracts.json).

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Operation names identify the semantic work in the [workspace model](../../docs/workspace-model.md), not installed functions or a script API. Resolve canonical context before durable work. No Arch Studio runner, package installation or executable reconstruction is required. Existing exact authorization persists; ask only for material missing information or missing permission.

Own the semantic procedure that writes `DOCUMENTS.csv`; other authored-record skills apply the same specification directly without a nested skill invocation or installed library. Classification is harness judgment. Native tools compute and verify paths, identities, hashes, collisions and publication/recovery evidence under the workspace contract.

## Before changing records

Before persistent changes, follow the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence): **Inspect → Prepare → Verify preparation → Apply → Verify result → Complete**. Inspect pending work first. Finish and verify preparation before the first canonical write: separately reread every saved original and prepared file, check its complete actual bytes, establish durable saving, and inspect actual permissions, ownership and ACLs. Merely writing recovery files does not finish verification. Apply only that verified set. Mark complete only after fresh readback validates the entire affected result and its relationships. Read-only requests and inline drafts need no publication sequence.

The affected set for registration is the complete destination file/package plus DOCUMENTS.csv; retain source originals and destination absence as guards. A move includes the destination, original path, every referring file requiring a rewrite, and DOCUMENTS.csv. Metadata-only updates change only DOCUMENTS.csv. Include all affected originals/preparations before any member is published; referenced sources remain read guards, not additional write targets.

## Receive

1. Resolve one new-model project and, when applicable, its explicitly registered studio. Ask for missing phase, stage, scope, originator, document date and kind, proposing evidence-based defaults. Previously confirmed coordinates need no repeated question. Dates preserve known precision; never use arrival date as an unknown issue date.
2. For files, use the actual accessible source. For a mailbox attachment or expiring download, the host acquires the authorized original to scratch, preserving message/download identity and expiry in `source`; no mailbox capability is implied by this skill. If unavailable, give a bounded handoff or use a supplied disk file. A URL-only source is provenance, not a locally received file.
3. Resolve placement under `documents.resolve` using confirmed coordinates and kind. The firm template owns placement. With an empty template, ask for the intended project-relative folder. Never rename received files. A folder/package retains its internal tree, including empty directories; an archive may remain a registered archive or be safely extracted by the host and received as a package. Sidecars and a sheet index are separate registered documents only when actually produced from available evidence; parsing is not invented by registration.
4. Preview registration when its exact intent is not already authorized: source path, destination, coordinates, metadata, duplicate hashes and any explicit `supersedes` ID. Apply the receive-owned native registration procedure within existing authorization; a preview neither allocates an identity nor proves write access. Registration copies from the source; it does not erase the original. Differing content at the destination is a collision requiring a distinct explicit revision, never silent overwrite.
5. Read back the row and actual file. Report document ID, relative path, hash, provenance and any unperformed content/visual inspection.

## Find, move and inspect

- `documents.query` filters by ID/kind/coordinates, arrival date (`since`), change ID, source type or expiry. `latest` selects the latest unsuperseded match using document date; it does not certify substantive approval or current-code applicability. Report ambiguity in the selection scope before relying on one result.
- `documents.move` requires ID, current expected SHA-256 and confirmed new coordinates. It preserves ID and source filename, updates supported relative Markdown links and affected hashes/history, and never overwrites a target. A necessary rewrite of issued/accepted bytes refuses before mutation; do not reseal terms. Unrelated existing drift remains unresolved; a changed document that needs a link rewrite blocks the move. Preview first when the exact destination is not already authorized. Reopen moved outputs and inspect relevant links.
- `documents.update` changes explicit status/provenance/title/notes without changing identity, bytes or revision relationships. Revised content is received as a new document with `supersedes`.
- `documents.verify` reports unreceived files, missing files, changed hashes, duplicate hashes, expired sources and template/vocabulary findings. Findings remain explicit; do not repair by guessing.
- Before multi-file publication, preserve the exact prior/prepared set and discoverable pending recovery evidence. `documents.recover` inspects actual state and resumes or restores only with fresh conflict guards; never replay a backup blindly. Cooperating locks do not exclude external editors. Verify actual staged bytes and access metadata before complete-file publication, then reread the entire affected set.

A document spanning phases remains one row at its primary confirmed phase, with other phases in notes, unless the original is physically split. Received evidence does not silently promote project facts, decisions, tasks, time or commercial acceptance.
