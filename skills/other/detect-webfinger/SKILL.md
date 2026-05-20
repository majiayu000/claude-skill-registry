---
name: detect-webfinger
description: >
  Detects whether a codebase implements the WebFinger protocol endpoint
  (RFC 7033). Use this skill whenever the user asks whether a repo, project,
  or codebase supports WebFinger, has a /.well-known/webfinger endpoint,
  implements the JRD response format, or handles acct: URI lookups. Also
  trigger when the user is auditing a codebase for ActivityPub or federated
  identity support, since WebFinger is a common dependency.
---

# Detect WebFinger Endpoint

WebFinger (RFC 7033) is a protocol that allows discovery of information about
people or resources using a standard URL pattern: `/.well-known/webfinger`.
It is commonly used by ActivityPub implementations (Mastodon, etc.) and
federated identity systems.

## Step 1 — Fast Signal Search

Search the codebase for the string `webfinger` (case-insensitive) across all
source files. This single search catches the vast majority of implementations.

```
Search query: webfinger
Case: insensitive
Scope: all source files (exclude: node_modules, vendor, .git, dist, build)
```

If **no matches** are found, proceed to Step 2 (fallback search).
If **matches are found**, proceed to Step 3 (classify results).

## Step 2 — Fallback Search (if Step 1 found nothing)

Some implementations register WebFinger indirectly under a generic
well-known handler. Search for:

- `/.well-known/` (route registration)
- `well_known` (snake_case variant common in Python/Ruby)
- `jrd+json` (the WebFinger response MIME type — very specific signal)
- `acct:` (the URI scheme WebFinger uses for user lookups)

If any of these match, include the files in Step 3 classification.
If still nothing — report: **WebFinger not detected**.

## Step 3 — Classify Each Match

For each file containing a match, determine which category it falls into:

### Category A — Implementation (confirmed)
The file contains executable code that:
- Registers a route or handler at `/.well-known/webfinger`
- Processes a `resource` query parameter
- Returns a JSON response (JRD format) with a `subject` field

### Category B — Library/Framework delegation
The file imports or references a WebFinger library (e.g. `node-webfinger`,
`ostatus`, `activitypub`, `webfinger-rack`, `go-webfinger`) without directly
defining the handler. The endpoint likely exists but is provided by the
dependency.

### Category C — Reference only (not an implementation)
The match appears in:
- Comments or documentation strings
- Test fixtures or mock data
- Configuration files referencing an external WebFinger server
- README or markdown files

### Category D — Ambiguous
The file handles `/.well-known/` generically and may or may not route
WebFinger requests. Read the surrounding logic to determine.

## Step 4 — Check for Framework-Specific Patterns

If the codebase language/framework is identifiable, also look for these
common patterns:

| Framework | Pattern to look for |
|---|---|
| Express / Node | `app.get('/.well-known/webfinger'` |
| Rails | `get '/.well-known/webfinger'` in routes.rb |
| Django | `path('.well-known/webfinger'` in urls.py |
| Spring Boot | `@GetMapping("/.well-known/webfinger")` |
| Mastodon / ActivityPub | Check for `webfinger_controller` or `webfinger_resource` |
| PHP | `$_GET['resource']` near a `well-known` path check |

## Step 5 — Report Results

Provide a clear summary with:

1. **Verdict**: WebFinger detected / Not detected / Possibly delegated to library
2. **Evidence**: List the specific files and line numbers (if available) that
   contain the implementation
3. **Implementation style**: Direct route handler / Library delegation /
   Framework built-in
4. **Completeness notes** (if applicable): e.g. "Handler found but no `rel`
   parameter filtering detected" or "Missing `application/jrd+json` content
   type header"
5. **Caveats**: e.g. "WebFinger may be handled upstream by a reverse proxy
   (nginx/caddy) and never reach the application code"

## What a Complete WebFinger Implementation Looks Like

For reference, a complete implementation handles:
- Route: `GET /.well-known/webfinger`
- Required query param: `resource` (e.g. `acct:user@example.com`)
- Optional query param: `rel` (filters which link types to return)
- Response Content-Type: `application/jrd+json`
- Response body: JSON with at minimum a `subject` field, typically also
  `links` and/or `aliases`
- HTTP 404 if the resource is not found
- HTTP 400 if the `resource` param is missing
