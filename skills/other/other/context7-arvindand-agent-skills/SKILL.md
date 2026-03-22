---
name: context7
description: "Documentation lookup via Context7 REST API. Use when the user needs current library APIs, framework patterns, migration guidance, or official code examples for React, Next.js, Prisma, Express, Vue, Angular, Svelte, or other npm/PyPI packages. Use when the user says 'how do I use X library', 'what's the API for Y', or asks for official documentation."
allowed-tools: Bash(python:*)
---

# Context7 Documentation Lookup

Use `scripts/context7.py` to fetch current library documentation without MCP tool-schema overhead.

This is an execution skill. Decide whether to search or fetch directly, run the script, then use the returned docs to answer. Keep the main flow lean and load [REFERENCES.md](REFERENCES.md) only when you need example commands, common library IDs, or troubleshooting details.

## When to Use

Activate when the user asks for:

- current library or framework APIs
- official code examples or implementation patterns
- version-specific docs or migration guidance
- third-party tool setup that depends on vendor docs
- documentation for libraries in npm, PyPI, or similar ecosystems

## Core Workflow

1. If you already know the library ID, skip search and call:

   ```bash
   python3 scripts/context7.py docs <library-id> [topic] [mode]
   ```

2. If the library ID is unclear, search first:

   ```bash
   python3 scripts/context7.py search "<query>"
   ```

3. Pick the best matching library ID, then fetch docs.
4. Use the returned docs to answer with version-aware guidance and cite the source URL when the script provides one.

## Decision Rules

- Search only when the library ID is unclear or ambiguous.
- Use `code` mode (default) for API references, function signatures, and implementation examples.
- Use `info` mode for conceptual guides, architecture, and migration-heavy questions.
- Use a focused topic first; broaden it if results are empty or off-target.
- For version-specific docs, append the version to the library ID (for example `/vercel/next.js/14`) or include the version in the topic.

If syntax is unclear, run:

```bash
python3 scripts/context7.py --help
```

## Output Rules

- Prefer official patterns over generic recall when the docs provide a direct answer.
- Keep the answer tied to the user's requested library and version.
- Call out deprecations, caveats, or migration notes when the docs surface them.
- If the docs are incomplete, say so and fall back to the best available general knowledge instead of inventing specifics.

## Recovery

| Issue | Action |
|-------|--------|
| Library ID is unclear | Re-run search with an alternate name, org name, or broader query. |
| Results are empty or irrelevant | Broaden the topic, then retry with the other mode (`code` vs `info`). |
| User needs a specific version | Add the version to the library ID or mention it in the topic, then verify the returned docs match. |
| Rate limited | Tell the user about `CONTEXT7_API_KEY`, then use best-effort fallback guidance if needed. |
| Script usage is unclear | Run `python3 scripts/context7.py --help`. |
| Script or network failure | Say live docs lookup failed and continue with clearly-labeled fallback knowledge. |

---

> **License:** MIT
> **See also:** [REFERENCES.md](REFERENCES.md)
