---
name: openwebf-app-webf-go
description: 'Run and debug a WebF app specifically in WebF Go (desktop/iOS/Android):
  load dev URLs, connect via devtools://, collect WEBF_NATIVE_LOG logs, clear WebF
  Go cache, and handle WebF Go limitations. Use w'
---

---
name: openwebf-app-webf-go
description: Run and debug a WebF app specifically in WebF Go (desktop/iOS/Android): load dev URLs, connect via devtools://, collect WEBF_NATIVE_LOG logs, clear WebF Go cache, and handle WebF Go limitations. Use when the user explicitly mentions WebF Go, devtools://, WEBF_NATIVE_LOG, the WebF Go debug button, or WebF Go settings (Clear Cache).
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, mcp__openwebf__docs_search, mcp__openwebf__docs_get_section, mcp__openwebf__docs_related, mcp__openwebf__docs_get_page
---

# OpenWebF App: WebF Go Dev Loop

## Instructions

1. Establish the dev loop: dev server → WebF Go URL → DevTools → logs.
2. If a device can’t reach the dev server, prioritize LAN/IP/`--host` and firewall checks.
3. Use the bundled OpenWebF docs via MCP to confirm exact steps and platform details.
4. Keep fixes minimal and reversible; prefer checklist-driven debugging.

More:
- [reference.md](reference.md)
- [doc-queries.md](doc-queries.md)
- [examples.md](examples.md)
