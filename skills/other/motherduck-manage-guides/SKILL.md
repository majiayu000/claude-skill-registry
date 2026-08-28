---
name: motherduck-manage-guides
description: Create, organize, read, update, and govern MotherDuck Guides. Use when an agent needs business definitions, join rules, data pitfalls, Dive or Flight conventions, or durable warehouse-native context attached to catalog objects.
license: MIT
---

# Manage MotherDuck Guides

Use this skill when context that is not visible from the schema should guide agents consistently: metric definitions, join rules, columns to avoid, business vocabulary, or Dive and Flight conventions. Guides are versioned Markdown documents stored in MotherDuck and surfaced through the MCP server.

## Source Of Truth

- Prefer the current MotherDuck Guides documentation and MCP tool descriptions.
- For analytical queries through MCP, call `get_query_guide` before writing SQL, then traverse only relevant topics and Guides.
- `get_dive_guide` and `get_flight_guide` automatically include summaries from the reserved `dives` and `flights` topics; do not load those topics separately unless deeper context is needed.

## Default Posture

- Keep one short root orientation Guide only when its guidance applies broadly. Put domain-specific knowledge under shallow, descriptive topics.
- Default new Guides to `access = 'user'`. Organization visibility requires an explicit request and the required admin permission.
- Write one coherent subject per Guide, with a discriminating title and description. Lead with rules, tested SQL, and named pitfalls.
- Attach references to the databases, shares, schemas, tables, columns, Dives, Flights, or Guides the content governs so agents discover it at the right time.
- Validate referenced objects and executable SQL against the live workspace before presenting a Guide as trustworthy.
- Use version comments to explain why guidance changed. Read before update and avoid overwriting concurrent work.

## Workflow

1. Inspect `get_query_guide` or `list_guides` to understand the visible topic tree and avoid duplication.
2. Read the relevant Guide versions and referenced objects before drafting a change.
3. Choose the narrowest useful topic; leave the topic empty only for organization-wide orientation.
4. Draft concise Markdown that maps business language to exact catalog objects and validated SQL.
5. For a create or update request, apply the change through MCP or the documented SQL function and read it back.
6. Verify metadata, access, references, current version, and change comment. For query work, follow the Guide and still validate the resulting SQL against the live schema.

For answer, review, or planning requests, inspect and draft without creating or modifying Guides. For explicit create/update requests, perform the in-scope mutation and verify it; ask before organization-wide publication, deletion, or unrelated context changes.

## Open Next

- Read `references/GUIDES_PLAYBOOK.md` for topic design, access governance, references, MCP/SQL operations, versioning, and quality checks.

## Related Skills

- `motherduck-explore` for validating referenced catalog objects
- `motherduck-query` for testing SQL and applying Guide-aware analysis
- `motherduck-create-dive` and `motherduck-create-flight` for reserved-topic conventions
- `motherduck-security-governance` for organization visibility and permission boundaries
