---
name: notion-writer
description: 'Use when the user explicitly asks to create, update, query, or archive Notion pages, databases, or blocks. Not for bulk operations, recursive edits, or widening the workspace scope.'
disable-model-invocation: true
---

# Notion writer

## Contract

| Field | Bound contract |
|---|---|
| Trigger | The user explicitly asks to create, update, query, or archive Notion pages, databases, or blocks. |
| Authority | Act only on explicit human invocation; preview the exact Notion target and consequence before using an authenticated connection or making a remote mutation, and require confirmation before an archive or any update that removes or overwrites content. |
| Side effect | Read only the requested Notion objects and perform only the requested create, update, query, or archive operation; do not widen the workspace, object set, or operation. |
| Done | The requested Notion operation is confirmed by the service response, and the resulting object metadata is returned. |

## Inputs

- Required: one operation (`create`, `update`, `query`, or `archive`) and the target workspace object or parent identified by an unambiguous Notion ID or URL.
- Required for `create` or `update`: the exact properties, content, and parent or destination the user wants written.
- Required for `query`: the database ID and any requested filter, sort, page size, or pagination bound; omitted query options remain unset.
- Required for `archive`: the exact page, database, or block ID and explicit confirmation after the archive preview.
- Required for a destructive update: explicit confirmation after previewing the fields or content that will be removed or overwritten.
- Optional: a configured authenticated Notion connection. Never ask the user to paste a raw secret into output; if no usable connection exists, stop as blocked.

## Procedure

1. Parse the requested operation, target IDs, payload, and query bounds. Reject missing or ambiguous targets, malformed IDs or URLs, unsupported object types, and payloads that do not match the requested Notion object. Done when: the operation, target, payload, and bounds are parsed and validated.
2. Resolve only enough target metadata to identify the workspace object and its current state. Do not search unrelated pages or databases to guess a target. Done when: the target object is identified with its current state.
3. Present the exact target, operation, fields or content affected, and remote consequence before using the authenticated connection for a mutation. For archive or destructive update, proceed only after the user explicitly confirms that preview. Done when: the preview is presented and confirmed (for mutations) or skipped (for queries).
4. Execute one bounded Notion operation with the supplied payload or query options. Preserve unspecified properties and content; do not infer additional edits, recursive operations, or bulk scope. Done when: one bounded operation is executed with no scope widening.
5. If Notion rate-limits the request, honor its `Retry-After` delay when supplied and retry the same idempotent request at most three times. Do not retry a mutation when its outcome is unknown; retrieve the named object to determine whether it landed before deciding whether the original operation remains safe to retry. Done when: the request succeeds, rate-limit retries are exhausted, or the mutation outcome is determined.
6. Inspect the service response for success, object identity, and resulting metadata. For a mutation with an ambiguous response, retrieve only the named object and compare the requested state; never report success from the request attempt alone. Done when: the service response confirms success or the targeted follow-up read proves the end state.
7. Return the operation, object type and ID, URL when supplied by Notion, last-edited timestamp when supplied, and the confirmed result. For paginated queries, return the retrieved results plus the continuation cursor and `has_more` state rather than silently fetching beyond the requested bound. Done when: the result is returned with all applicable metadata and pagination state.

## Failure and recovery

- Invalid or ambiguous input: make no mutation and return `blocked` with the missing or conflicting field.
- Missing authentication, denied capability, inaccessible workspace, or insufficient permission: make no further request and return `blocked` with Notion's error class and the affected object ID.
- Validation or Notion API rejection: do not alter the payload or widen scope; return `failed` with the rejected operation, object ID, and service error.
- Rate limit after three safe attempts: stop and return `blocked` with the retry count and last `Retry-After` value.
- Unknown mutation outcome: retrieve only the named object. Return `succeeded` if its state proves the requested change, `failed` if it proves the change did not land, or `blocked` if the state cannot be established; never repeat a potentially applied mutation blindly.
- Partial query or multi-result response: return the confirmed results already received with the cursor and error, classified as `partial`; do not claim the query is complete.
- An archive or destructive update has no automatic rollback. If the user has not confirmed the preview, make no mutation; if Notion reports success, report the resulting archived or updated state without claiming restoration is available.

## Output

Terminal classification (`succeeded`, `partial`, `failed`, or `blocked`) with the requested operation, Notion object type and ID, confirmed resulting metadata, and when applicable the object URL, last-edited timestamp, query continuation state, retry details, or exact service error.
