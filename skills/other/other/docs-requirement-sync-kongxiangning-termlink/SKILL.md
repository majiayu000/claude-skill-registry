---
name: docs-requirement-sync
description: Drive implementation from requirement docs (REQ) and enforce compact change records (CR) for every implementation/commit. Use when developing a new requirement and keeping REQ, Backlog, Product, Roadmap, Changelog, and records in sync.
---

# Docs Requirement Sync

Use this skill when implementing a requirement from `docs/product/requirements/REQ-*.md`.

Run commands from repository root:
`E:\coding\TermLink`

## Workflow

1. Validate the REQ before coding:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/docs-requirement-sync/scripts/validate-req.ps1 -ReqPath ./docs/product/requirements/REQ-YYYYMMDD-slug.md -Strict
```

2. Create a draft change record (CR) before or during implementation:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/docs-requirement-sync/scripts/new-change-record.ps1 -ReqId REQ-YYYYMMDD-slug -Slug short-topic
```

3. After implementation, update the CR to `active` and set `commit_ref`.

4. Validate CR format:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/docs-requirement-sync/scripts/validate-change-record.ps1 -RecordPath ./docs/changes/records/CR-YYYYMMDD-HHMM-short-topic.md -Strict
```

5. Check full doc sync before marking requirement done:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/docs-requirement-sync/scripts/check-doc-sync.ps1 -ReqId REQ-YYYYMMDD-slug
```

## Mandatory Rules

1. One implementation/commit must have one CR file.
2. CR must include `req_id + commit_ref` for traceability.
3. Requirement status cannot move to `done` unless there is at least one `active` CR.
4. `CHANGELOG_PROJECT.md` is summary only. Detailed rollback/restore info lives in CR files.

## References

1. `docs/changes/records/TEMPLATE_CHANGE_RECORD.md`
2. `docs/changes/records/INDEX.md`
3. `docs/product/requirements/REQ-TEMPLATE.md`
