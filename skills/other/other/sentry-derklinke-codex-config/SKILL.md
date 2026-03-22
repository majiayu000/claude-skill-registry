---
name: "sentry"
description: "Use when the user asks to inspect Sentry issues or events, summarize recent production errors, or pull basic Sentry health data through the Sentry MCP tools."
---


# Sentry MCP Observability

## Quick start

- Use Sentry MCP tools only. Do not call local Python helpers, direct REST scripts, or `SENTRY_AUTH_TOKEN` workflows for issue/event inspection.
- Prefer issue URL input when the user provides it; MCP can extract org, project, and issue identifiers directly.
- Defaults: time range `24h`, environment `prod`, limit 20 unless the user specifies otherwise.
- Use MCP-native issue IDs, event IDs, trace IDs, and org/project slugs when present; do not invent fallbacks.

## Core tasks

### 1) Specific issue or URL

- Use `mcp__sentry__get_issue_details` for a known issue ID, event ID, or full Sentry issue URL.
- Use `mcp__sentry__search_issue_events` to filter events within that issue by time, environment, release, user, or trace.
- Use `mcp__sentry__get_issue_tag_values` for aggregate distributions such as affected URLs, browsers, environments, or releases.

### 2) Search across issues

- Use `mcp__sentry__search_issues` when the user wants a list of grouped issues or user feedback.
- Use `mcp__sentry__search_events` for counts, aggregates, or raw event/log/span search.
- Use `mcp__sentry__find_organizations`, `mcp__sentry__find_projects`, and `mcp__sentry__find_teams` only to discover identifiers that are missing.

### 3) Deeper analysis

- Use `mcp__sentry__analyze_issue_with_seer` only when the user explicitly asks for Seer analysis or the root cause is not recoverable from issue details alone.
- Use `mcp__sentry__get_trace_details` for trace overview by trace ID.
- Use `mcp__sentry__find_releases` when the user asks about recent releases or release deployment timing.

## Output rules

- State which MCP tool path was used when the distinction matters, especially `search_issues` versus `search_events`.
- For issue summaries: include title, issue ID, status, impact counters, last seen, and the strongest culprit evidence available.
- For event summaries: include timestamp, environment, release, culprit, and relevant tags.
- Redact PII in responses. Avoid dumping raw stack traces unless the user explicitly asks.
- If identifiers are ambiguous, say what is missing and use the narrowest discovery tool needed.
- If the user supplies a Sentry URL, preserve the full URL and pass it through unchanged.

## Local Cross-References

- `ios-testflight-triage` - Use to align external crash trends with TestFlight crash investigation workflows.
- `ios-app-store-connect-ref` - Use when comparing Sentry data against App Store Connect crash reports.
