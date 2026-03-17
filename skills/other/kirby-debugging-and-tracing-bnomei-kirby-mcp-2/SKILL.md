---
name: kirby-debugging-and-tracing
description: Diagnoses Kirby rendering/runtime issues using MCP runtime rendering, dump traces, and template/snippet/controller indexes. Use when outputs are wrong, errors occur, or tracing execution paths is required.
---

# Kirby Debugging and Tracing

## Quick start

- Follow the workflow below to reproduce and trace render issues.

## KB entry points

- `kirby://kb/scenarios/68-snippet-controllers`
- `kirby://kb/scenarios/03-shared-controllers`
- `kirby://kb/scenarios/13-custom-routes`
- `kirby://kb/scenarios/02-json-content-representation-ajax-load-more`
- `kirby://kb/scenarios/14-escaping-and-safe-markdown`

## Required inputs

- Page id/uuid or URL path.
- Expected vs actual output and content type.
- Auth/session requirements and steps to reproduce.

## Repro checklist

- Capture page id/uuid or URL, content type, and expected vs actual output.
- Note auth/session state and request parameters.
- Record cache state and the render `traceId`.

## Stop condition

- Stop once output matches expected behavior and temporary dumps are removed.

## Dump placement example

```php
mcp_dump([
  'page' => $page->id(),
  'template' => $page->intendedTemplate()->name(),
]);
```

- Remove dumps after the issue is resolved.

## Common pitfalls

- Leaving `mcp_dump()` in production code.
- Debugging cached output or the wrong content type.

## Workflow

1. Ask for page id/uuid or URL path, expected vs actual output, content type, and any session/login requirements.
2. Call `kirby:kirby_init`, then ensure runtime availability with `kirby:kirby_runtime_status` and `kirby:kirby_runtime_install` if needed.
3. Reproduce with `kirby:kirby_render_page(noCache=true, contentType=...)` and capture `traceId` plus errors.
4. Locate relevant code paths:
   - `kirby:kirby_templates_index`
   - `kirby:kirby_snippets_index`
   - `kirby:kirby_controllers_index`
   - `kirby:kirby_models_index`
   - `kirby:kirby_routes_index` when routing is involved
5. If the issue is unclear, add targeted `mcp_dump()` calls and read the trace with `kirby:kirby_dump_log_tail(traceId=...)`.
6. Apply the smallest fix, re-render to confirm, and remove temporary dumps.
7. Search the KB with `kirby:kirby_search` (examples: "custom routes", "snippet controllers", "shared controllers", "content representations").
