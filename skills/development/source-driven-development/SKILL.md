---
name: source-driven-development
description: Grounds every implementation decision in official documentation. Use when you want authoritative, source-cited code free from outdated patterns. Use when building with any framework or library where correctness matters.
---

# Source-Driven Development

## Overview

Back every framework-specific decision with official documentation. Memory is not evidence. Training data ages: APIs deprecate and recommended patterns shift between versions, so code written from recall can look correct and break against the installed version. Verify the pattern, cite the source, and leave the user a link they can open. Every framework-specific pattern traces to an authoritative source the user can check.

## When to Use

- The user wants code that follows current best practices for a given framework
- Building boilerplate, starter code, or patterns that get copied across a project
- The user explicitly asks for documented, verified, or "correct" implementation
- Implementing features where the framework's recommended approach matters (forms, routing, data fetching, state management, auth)
- Reviewing or improving code that uses framework-specific patterns
- Any time you are about to write framework-specific code from memory

**When NOT to use:**

- Correctness does not depend on a specific version (renaming variables, fixing typos, moving files)
- Pure logic that behaves the same across all versions (loops, conditionals, data structures)
- The user explicitly wants speed over verification ("just do it quickly")

## The Process

```
DETECT ──→ FETCH ──→ IMPLEMENT ──→ CITE
  │          │           │            │
  ▼          ▼           ▼            ▼
 What       Get the    Follow the   Show your
 stack?     relevant   documented   sources
            docs       patterns
```

### Step 1: Detect Stack and Versions

Read the project's dependency file and pin the exact versions:

```
package.json    → Node/React/Vue/Angular/Svelte
composer.json   → PHP/Symfony/Laravel
requirements.txt / pyproject.toml → Python/Django/Flask
go.mod          → Go
Cargo.toml      → Rust
Gemfile         → Ruby/Rails
```

State the result before writing anything. The procedure is language-agnostic; the report shape is the same across families:

```
STACK DETECTED:
- React 19.1.0 (package.json)
- Vite 6.2.0
→ Fetch official docs for the patterns in scope.
```

```
STACK DETECTED:
- Django 5.1 (pyproject.toml)
- Python 3.13
→ Fetch official docs for the patterns in scope.
```

If versions are missing or ambiguous, **ask the user**. Do not guess: the version selects which patterns are correct.

### Step 2: Fetch Official Documentation

Fetch the documentation page for the exact feature you are implementing. Not the homepage, not the full docs tree — the page that covers the pattern.

**Source hierarchy (in order of authority):**

| Priority | Source | Example |
|----------|--------|---------|
| 1 | Official documentation | react.dev, docs.djangoproject.com, symfony.com/doc |
| 2 | Official blog / changelog | react.dev/blog, nextjs.org/blog |
| 3 | Web standards references | MDN, web.dev, html.spec.whatwg.org |
| 4 | Browser/runtime compatibility | caniuse.com, node.green |

**Not authoritative — never cite as a primary source:**

- Stack Overflow answers
- Blog posts or tutorials (even popular ones)
- AI-generated documentation or summaries
- Your own training data (verifying it is the entire point)

**Fetch precisely:**

```
BAD:  Fetch the React homepage
GOOD: Fetch react.dev/reference/react/useActionState

BAD:  Search "django authentication best practices"
GOOD: Fetch docs.djangoproject.com/en/6.0/topics/auth/
```

After fetching, extract the patterns that apply and record any deprecation warnings or migration guidance on the page.

When official sources contradict each other (a migration guide against the API reference, for instance), surface the discrepancy to the user and verify which pattern actually holds against the detected version.

### Step 3: Implement Following Documented Patterns

Write code that matches what the documentation shows:

- Use the API signatures from the docs, not from memory
- If the docs show a newer approach, use the newer approach
- If the docs deprecate a pattern, do not use the deprecated form
- If the docs do not cover something, flag it as unverified

**When the docs conflict with existing project code:**

```
CONFLICT DETECTED:
The existing codebase uses useState for form loading state,
but React 19 docs recommend useActionState for this pattern.
(Source: react.dev/reference/react/useActionState)

Options:
A) Use the modern pattern (useActionState) — matches current docs
B) Match existing code (useState) — matches the codebase
→ Which do you prefer?
```

The same conflict shape applies in any stack:

```
CONFLICT DETECTED:
The codebase wraps ORM calls in sync_to_async, but Django 5.1
documents native async ORM methods (aget, acreate) for this path.
(Source: docs.djangoproject.com/en/5.1/topics/db/queries/#async-queries)

Options:
A) Use the documented pattern (native async ORM) — matches current docs
B) Match existing code (sync_to_async wrappers) — matches the codebase
→ Which do you prefer?
```

Surface the conflict. Do not silently pick one.

### Step 4: Cite Your Sources

Every framework-specific pattern gets a citation. The user must be able to verify each decision. Citations carry across languages:

```typescript
// React 19 form state via useActionState (replaces manual isPending/setIsPending)
// Source: https://react.dev/reference/react/useActionState#usage
const [state, formAction, isPending] = useActionState(submitOrder, initialState);
```

```go
// Go 1.22+ method-aware routing patterns in net/http ServeMux
// Source: https://pkg.go.dev/net/http#hdr-Patterns
mux.HandleFunc("GET /orders/{id}", getOrder)
```

**In conversation:**

```
I'm using useActionState instead of manual useState for the form
submission state. React 19 replaced the manual isPending/setIsPending
pattern with this hook.

Source: https://react.dev/blog/2024/12/05/react-19#actions
"useTransition now supports async functions [...] to handle
pending states automatically"
```

**Citation rules:**

- Full URLs, not shortened
- Prefer deep links with anchors (`/useActionState#usage` over `/useActionState`); anchors survive doc restructuring better than top-level pages
- Quote the relevant passage when it supports a non-obvious decision
- Include browser/runtime support data when recommending platform features
- If you cannot find documentation for a pattern, say so:

```
UNVERIFIED: I could not find official documentation for this
pattern. This is based on training data and may be outdated.
Verify before using in production.
```

Honesty about what you could not verify beats false confidence.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident about this API" | Confidence is not evidence. Training data carries outdated patterns that look correct and break against current versions. Verify. |
| "Fetching docs wastes tokens" | Hallucinating an API wastes more. The user debugs for an hour, then finds the signature changed. One fetch prevents the rework. |
| "The docs won't have what I need" | If the docs do not cover it, that is a signal: the pattern may not be officially recommended. |
| "I'll just mention it might be outdated" | A disclaimer does not help. Either verify and cite, or flag it as unverified. Hedging is the worst option. |
| "This is a simple task, no need to check" | Simple tasks with wrong patterns become templates. The user copies a deprecated handler into ten call sites before the modern approach surfaces. |

## Red Flags

- Writing framework-specific code without checking the docs for that version
- Saying "I believe" or "I think" about an API instead of citing the source
- Implementing a pattern without knowing which version it applies to
- Citing Stack Overflow or blog posts instead of official documentation
- Using deprecated APIs because they appear in training data
- Not reading `package.json` / the dependency file before implementing
- Delivering code with no source citations for framework-specific decisions
- Fetching an entire docs site when one page is relevant

## Verification

After implementing with source-driven development:

- [ ] Framework and library versions were identified from the dependency file
- [ ] Official documentation was fetched for framework-specific patterns
- [ ] All sources are official documentation, not blog posts or training data
- [ ] Code follows the patterns shown in the current version's documentation
- [ ] Non-trivial decisions include source citations with full URLs
- [ ] No deprecated APIs are used (checked against migration guides)
- [ ] Conflicts between docs and existing code were surfaced to the user
- [ ] Anything that could not be verified is explicitly flagged as unverified
