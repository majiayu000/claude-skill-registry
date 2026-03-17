---
name: detect-nodeinfo
description: >
  Detects whether a codebase implements the NodeInfo protocol endpoint.
  NodeInfo is a standard used by Fediverse and federated social network
  servers to expose metadata about the instance (software name, version,
  protocols supported, user counts, etc.). Use this skill whenever the user
  asks whether a repo or codebase supports NodeInfo, has a
  /.well-known/nodeinfo endpoint, exposes instance metadata, or implements
  Fediverse server discovery. Also trigger when auditing a codebase for
  ActivityPub, Diaspora, or federated social networking support, since
  NodeInfo is a common companion to those protocols.
---

# Detect NodeInfo Endpoint

NodeInfo is a protocol used by federated social network servers to expose
instance metadata in a standardized format. It is widely used in the
Fediverse (Mastodon, Misskey, Pleroma, Diaspora, etc.).

## How NodeInfo Works (Two-Part Architecture)

NodeInfo is **always two endpoints**, not one. This is important for
classification:

**Part 1 — Discovery endpoint** (required):
- URL: `GET /.well-known/nodeinfo`
- Returns a JSON object with a `links` array, each entry pointing to a
  versioned schema document
- Example response:
  ```json
  {
    "links": [
      {
        "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
        "href": "https://example.org/nodeinfo/2.1"
      }
    ]
  }
  ```

**Part 2 — Schema endpoint** (required):
- URL: typically `/nodeinfo/2.1` or `/nodeinfo/2.0` (path is not
  standardized, but this convention is near-universal)
- Returns the full instance metadata document
- Key fields: `version`, `software`, `protocols`, `usage`,
  `openRegistrations`, `metadata`

**Variant — NodeInfo2** (optional, separate spec):
- URL: `GET /.well-known/x-nodeinfo2`
- A different, simpler schema by a different author (jaywink/nodeinfo2)
- Less common; treat as a separate positive signal if found

---

## Step 1 — Fast Signal Search

Search the codebase for `nodeinfo` (case-insensitive) across all source
files, excluding: `node_modules`, `vendor`, `.git`, `dist`, `build`.

If **no matches** are found, proceed to Step 2 (fallback search).
If **matches are found**, proceed to Step 3 (classify results).

## Step 2 — Fallback Search (if Step 1 found nothing)

Some implementations use only generic well-known routing. Search for:

- `/.well-known/nodeinfo` (the discovery path literal)
- `diaspora.software/ns/schema` (the rel URL used in the links array —
  a very specific signal)
- `x-nodeinfo2` (NodeInfo2 variant path)
- `openRegistrations` (a distinctive field name in the schema response)
- `activeHalfyear` or `activeHalfYear` (unique usage stats field)

If still nothing — report: **NodeInfo not detected**.

## Step 3 — Classify Each Match

For each file containing a match, determine which category it falls into:

### Category A — Discovery endpoint (confirmed)
The file registers a route at `/.well-known/nodeinfo` that returns a
`links` array pointing to a versioned schema document.

### Category B — Schema endpoint (confirmed)
The file registers a route (commonly `/nodeinfo/2.0`, `/nodeinfo/2.1`,
`/nodeinfo/2.2`) that returns the full instance metadata document with
fields like `software`, `protocols`, `usage`, `openRegistrations`.

### Category C — Both endpoints present
The codebase implements both Part 1 and Part 2 — this is a complete
implementation.

### Category D — Library/Framework delegation
The file imports or references a NodeInfo library (e.g. `go-nodeinfo`,
`@semapps/nodeinfo`, `nodeinfo-rack`, ActivityPub frameworks like Fedify
which auto-register NodeInfo) without directly defining the handlers.

### Category E — Reference only (not an implementation)
The match appears in comments, test fixtures, README files, or configuration
pointing to an *external* NodeInfo server.

### Category F — NodeInfo2 variant
The file handles `/.well-known/x-nodeinfo2` — a valid but separate
implementation of the NodeInfo2 spec (jaywink/nodeinfo2). Report alongside
standard NodeInfo findings.

## Step 4 — Check for Framework-Specific Patterns

| Framework / Language | Pattern to look for |
|---|---|
| Rails | `get '/.well-known/nodeinfo'` in routes.rb; `nodeinfo_controller.rb` |
| Django | `path('.well-known/nodeinfo'` in urls.py |
| Express / Node | `app.get('/.well-known/nodeinfo'` |
| Spring Boot | `@GetMapping("/.well-known/nodeinfo")` |
| Go | `nodeinfo.NodeInfoPath` constant; `NodeInfoDiscover` handler |
| Mastodon | `WellKnown::NodeinfoController` |
| Misskey / Calckey | `nodeinfo` in route definitions |
| Fedify (TS/JS) | NodeInfo auto-registered — look for `setNodeInfoDispatcher` |
| PHP (ActivityPub) | `well-known/nodeinfo` near `json_encode` |

## Step 5 — Check Schema Version Support

If a schema endpoint is found, note which version(s) are supported:

- `1.0` — original, rarely seen today
- `1.1` — adds `services`
- `2.0` — adds `usage.localComments`; most common
- `2.1` — adds `software.repository` and `software.homepage`; current standard
- `2.2` — draft; uncommon

The `rel` URL in the discovery response encodes the version:
`http://nodeinfo.diaspora.software/ns/schema/2.1`

## Step 6 — Report Results

Provide a clear summary with:

1. **Verdict**: NodeInfo detected / Not detected / Possibly delegated to library
2. **Parts found**:
   - Discovery endpoint (`/.well-known/nodeinfo`): Yes / No / Via library
   - Schema endpoint (`/nodeinfo/x.y`): Yes / No / Via library
   - NodeInfo2 variant (`/.well-known/x-nodeinfo2`): Yes / No / N/A
3. **Schema versions supported** (if determinable)
4. **Evidence**: File names and line numbers containing the implementation
5. **Implementation style**: Direct / Library delegation / Framework built-in
6. **Completeness notes** (if applicable):
   - e.g. "Discovery endpoint found but no schema endpoint detected"
   - e.g. "Schema endpoint found but `usage` stats appear hardcoded rather
     than queried from a database"
   - e.g. "Missing `openRegistrations` field in schema response"
7. **Caveats**: e.g. "NodeInfo may be handled by a reverse proxy or
   middleware layer not visible in application code"

## What a Complete NodeInfo Implementation Looks Like

For reference, a complete implementation provides:

**Discovery** (`/.well-known/nodeinfo`):
```json
{
  "links": [
    {
      "rel": "http://nodeinfo.diaspora.software/ns/schema/2.1",
      "href": "https://example.org/nodeinfo/2.1"
    }
  ]
}
```

**Schema** (`/nodeinfo/2.1`):
```json
{
  "version": "2.1",
  "software": {
    "name": "myapp",
    "version": "1.0.0",
    "repository": "https://github.com/example/myapp",
    "homepage": "https://example.org"
  },
  "protocols": ["activitypub"],
  "usage": {
    "users": {
      "total": 100,
      "activeHalfyear": 50,
      "activeMonth": 20
    },
    "localPosts": 1000,
    "localComments": 500
  },
  "openRegistrations": true,
  "metadata": {}
}
```
