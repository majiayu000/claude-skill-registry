---
name: uncertainty-verification
description: Use when providing exact commands, flags, config keys, file paths, API details, standards, or version-specific behavior - enforces verification via official docs (Context7/web fetch), explicit citations, and bans assumption-based specifics
---

# Uncertainty Verification

## Overview

This skill forces verification before stating any specific technical detail that could vary by version, environment, or specification.

## Use when...

- The request asks for **exact** command syntax, flags, or configuration keys
- The answer depends on **version-specific behavior**, deprecations, or recent changes
- The request involves **standards/specs** (RFCs, protocol behavior, i18n/timezone/locale rules)
- The user asks for **exact file paths**, naming conventions, or directory structures
- The answer requires **library-specific APIs** (class names, method signatures, constants)
- Any part of the response would otherwise be based on “typical patterns” or memory

## Symptoms / keywords

Use this skill when the prompt contains or implies keywords like:

- “exact”, “precise”, “verbatim”, “copy/paste”, “flags”, “CLI”, “config key”, “endpoint”, “params”
- “deprecated”, “since vX”, “in 2025”, “changed in”, “breaking change”, “migration”
- “RFC”, “spec”, “standard”, “format”, “timezone”, “locale”, “i18n”, “OAuth”, “HTTP”, “GraphQL”
- “directory structure”, “file path”, “naming convention”, “default location”
- Specific error codes/messages that must be accurate

## Technical Details Requiring Verification

**Don't provide these specific details without checking official documentation:**

- ❌ Exact file paths, directory structures, or naming conventions
- ❌ Specific API endpoints, parameter names, or response formats
- ❌ Exact command syntax, flags, or configuration keys
- ❌ Version-specific features or deprecations
- ❌ Specific error codes or messages
- ❌ Hostname patterns, URL formats, or connection string syntax
- ❌ Library-specific class names, method signatures, or constants

**Required response pattern when uncertain:**

```
"I need to verify this with official documentation. Let me check..."
→ Dispatch a research subagent to execute Context7 or Web fetch and return a Context Package with citations
→ Cite the source explicitly
```

**Enforcement:**

- Treat assumptions as errors requiring immediate correction
- Any specific technical detail = Verify first
- Any format/syntax example = Check documentation
- Any version-dependent behavior = Confirm with official docs

## Uncertainty detection criteria

**Web Fetch Strategy (via research subagent):** Ask the subagent to try `mcp_fetch_fetch` first (fast; good for SSR/static pages like MDN/Wikipedia). If insufficient (title-only, <100 chars, no meaningful content), ask the subagent to fallback to `fetch_webpage` (better for CSR/JavaScript-rendered docs). The subagent must return a cited Context Package.

When ANY of these apply, immediately dispatch a research subagent to perform verification (Context7/web fetch/etc.) and return a cited Context Package:

- Library/framework version-specific behavior or API changes
- Standard format specifications (phone, date, country codes, currency, regex)
- Protocol/RFC specifications (HTTP, OAuth, REST, GraphQL)
- Best practices for security, performance, scalability
- Algorithm implementations or mathematical formulas
- Time zone, locale, internationalization rules
- After Context7 returns incomplete docs (missing examples, types, error handling)

**Forbidden patterns:**

- “Based on my knowledge” without citing sources
- “This should work” without verification
- “I believe the format is...” without confirming the standard
- Implementing first, validating later
- Confidence-based verification skipping
- Providing examples with specific syntax without verification
- Stating “typical patterns” without confirming they apply
- Suggesting “common practices” without checking current standards

**Authoritative sources priority:**

1. Official docs (`docs.*.com`, `developer.mozilla.org`, `*.org/docs`)
2. Standards bodies (`ietf.org/rfc*`, `w3.org/TR/*`, `whatwg.org`)
3. Official repos (`github.com/org/repo` - README, issues, docs)
4. Specifications (Wikipedia for international standards)

## Procedure (minimal)

1. Identify which parts of the answer require exactness.
2. Fetch authoritative sources (Context7 for library docs; web fetch for standards/official docs).
3. Cite the source explicitly when stating specifics.
4. If sources are unavailable or unclear, say so and give a safe, general answer plus what to verify.
