---
name: licensing
description: MANDATORY - Check dependency licenses before importing. Write original code, don't copy.
---

# Licensing

This project is **MIT** licensed. This skill covers dependency license compatibility and ethical code practices.

---

## MIT: What It Means

| Allowed | Required | Prohibited |
|---------|----------|------------|
| Commercial use | Include copyright notice | None |
| Modification | Include license text | |
| Distribution | | |
| Private use | | |

**Key point:** MIT is maximally permissive. Users can do almost anything with the code as long as they include the copyright and license notice.

---

## Compatible Dependency Licenses

Before adding a dependency, check its license. These are compatible with MIT:

| License | Compatible | Notes |
|---------|------------|-------|
| **MIT** | Yes | Same license, no issues |
| **BSD-2-Clause** | Yes | Permissive |
| **BSD-3-Clause** | Yes | Permissive |
| **ISC** | Yes | Permissive (like MIT) |
| **Apache-2.0** | Yes | Permissive + patent grant |
| **0BSD** | Yes | Public domain equivalent |
| **Unlicense** | Yes | Public domain |
| **CC0** | Yes | Public domain |
| **MPL-2.0** | Yes | Weak copyleft, file-level (compatible but adds obligations) |

### Use With Caution

| License | Notes |
|---------|-------|
| **LGPL-2.1/3.0** | Technically compatible for Go (static linking debate), but prefer alternatives |
| **GPL-3.0 / AGPL-3.0** | Technically compatible (you can use GPL code in an MIT project, but the combined work's distribution terms get complicated). **Prefer MIT/Apache/BSD alternatives** to keep things simple. |

### Incompatible (DO NOT USE)

| License | Why |
|---------|-----|
| **SSPL** | Not OSI-approved, incompatible |
| **BSL** | Business Source License, time-delayed open source |
| **Proprietary** | Obviously incompatible |
| **CC-BY-NC** | Non-commercial restriction |
| **Commons Clause** | Commercial restriction |
| **No license** | Treat as proprietary — do not use |

---

## Checking Dependency Licenses

### Go Dependencies

```bash
# List all dependencies with licenses
go-licenses report ./... 2>/dev/null

# Or manually check go.mod imports
go list -m -json all | jq -r '.Path'
# Then check each on pkg.go.dev or GitHub
```

### Before Adding a Dependency

1. Check the LICENSE file in the repo
2. Verify it's in the compatible list above
3. If unclear, check SPDX identifier: https://spdx.org/licenses/

### Planned Dependencies

Key dependencies and their licenses:
- `github.com/yuin/goldmark` — MIT ✓
- `github.com/yuin/goldmark-highlighting` — MIT ✓
- `go.abhg.dev/goldmark/mermaid` — MIT ✓
- `github.com/alecthomas/chroma/v2` — MIT ✓

---

## Writing Original Code

### The Rule

**Learn from other projects. Write your own code.**

When studying how another project implements something:

1. **Understand the concept** — What problem does it solve? What's the approach?
2. **Close the source** — Don't have it open while writing
3. **Write from understanding** — Implement based on your mental model
4. **Make it better** — Your version should be at least as good, preferably superior

### What's NOT Allowed

```go
// WRONG: Copied from github.com/other/project
func ParseConfig(data []byte) (*Config, error) {
    // [copied code]
}

// WRONG: "Adapted" (minor variable renames)
func ParseConfiguration(input []byte) (*Configuration, error) {
    // [same logic, different names]
}
```

### What IS Allowed

```go
// RIGHT: Studied how X project handles URL rewriting,
// implemented our own version with better error messages
// and support for relative path resolution.
func RewriteRelativeURLs(doc []byte, baseURL string) []byte {
    // [original implementation]
}
```

### Gray Areas

| Situation | Guidance |
|-----------|----------|
| Standard patterns (middleware, handlers) | OK — these are universal idioms |
| Algorithm from a paper/spec | OK — implement the spec, not someone's code |
| Small utility (max, min, clamp) | OK — too simple to be copyrightable |
| Copied struct layout | Risky — restructure based on your needs |
| Copied test cases | Risky — write your own test scenarios |

### When In Doubt

1. Can you explain it without looking at the source?
2. Would your implementation differ if you'd never seen theirs?
3. Are you copying structure or just learning a concept?

If yes to all three, you're probably fine.

---

## Bundled Assets

Static assets embedded in the binary must have compatible licenses AND be documented:

**Location:** `embed/LICENSES.md`

Current bundled assets:
- mermaid.js — MIT ✓
- github-markdown-css — MIT ✓

When adding bundled assets:
1. Verify license compatibility
2. Add license text to `embed/LICENSES.md`
3. Note version in Makefile (pinned versions)

---

## License Headers

Go files don't require license headers (the root LICENSE file covers everything).

If you want to add headers for clarity in key files:

```go
// Copyright 2026 air-gapped
// SPDX-License-Identifier: MIT
```

---

## Quick Reference

```
Adding a dependency?
  → Check license is in compatible list
  → If not listed, investigate before using
  → Prefer MIT/Apache/BSD — avoid copyleft

Learning from another project?
  → Understand the concept
  → Write your own implementation
  → Make it better

Bundling static assets?
  → Check license compatibility
  → Document in embed/LICENSES.md
```
