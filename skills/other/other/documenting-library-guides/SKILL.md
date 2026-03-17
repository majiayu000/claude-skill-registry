---
name: documenting-library-guides
description: Create user-facing documentation for libraries — the kind of docs you'd find on a static documentation site. Guides readers through the library with an engaging, conversational tone, real code examples drawn from the actual codebase, and a navigable site-like structure. Use when (1) a library has no user-facing docs beyond inline code comments, (2) existing docs are API references with no narrative guidance, (3) users need task-oriented guides to accomplish common goals, or (4) a library's docs need restructuring into a browsable, site-ready format.
---

# Documenting Library Guides

Create user-facing documentation for libraries — the docs users actually read. Not API references (auto-generate those), not inline comments (those live in code), but the narrative layer that guides a reader from "what is this?" to "I'm productive with it."

## Core Principles

1. **Conversational, Not Corporate**: Write like a knowledgeable colleague explaining something over coffee. Have personality — be direct, occasionally witty, never dry. But clarity always wins over cleverness. Don't force jokes; a well-placed quip lands, a joke per section exhausts.
2. **Imperative for Doing, Declarative for Understanding**: When showing how to accomplish something, use imperative text: "Create a `Client`, pass it your config, and call `Connect()`." When explaining concepts, switch to declarative: "The connection pool manages up to N concurrent connections." Match voice to purpose.
3. **Connected to the Code**: Every example must come from the actual codebase — real types, real method signatures, real return values. Never write pseudocode or hypothetical examples. If the API changes, the docs should feel immediately stale so they get updated.
4. **Site-Ready Structure**: Organize docs as if they'll be served by a static site generator (Starlight, MkDocs, Docusaurus). Each page stands alone but fits a reading order. Sidebar-friendly hierarchy, clear page boundaries, cross-page linking.
5. **Adjacent, Not Redundant**: These docs complement inline code documentation — they don't replace it. Inline docs describe the API surface; library guides describe how to *use* it to get things done. Never duplicate what a godoc/rustdoc/typedoc already provides.

## Documentation Structure

```
docs/
  index.md              <- Overview: what this library does, why, where to go next
  getting-started.md    <- Install + first working example (fastest path to "it works")
  guides/
    <task>.md           <- Task-oriented walkthroughs ("How do I do X?")
  concepts/             <- Optional, only when needed
    <topic>.md          <- Mental models, design rationale for non-obvious choices
  recipes/
    <recipe>.md         <- Short, copy-paste-friendly snippets for common tasks
  troubleshooting.md    <- Pitfalls, anti-patterns, FAQs
```

### Page Purposes

- **Overview** (`index.md`): The entry point. What the library does, the core idea in one sentence, a taste of what using it looks like, and a "where to go next" section pointing readers to the right page for their goal. Not a README — no badges, no install instructions, no project governance.
- **Getting Started**: The fastest possible path from "I found this library" to "I have it working." Install, import, one meaningful example, done. Resist the urge to explain everything — just get the reader to a working state.
- **Guides**: Task-oriented. Each guide answers one question: "How do I do X with this library?" Walk the reader through step by step, explain the why along the way, and end with a complete working result. Guides are the backbone of good library docs.
- **Concepts**: Use sparingly. Only create a concept page when users would otherwise fight the library's grain or make a recurring mistake. A well-designed API shouldn't need much explaining — but when it does, this is where the "why" lives.
- **Recipes**: Short and focused. Each recipe is a self-contained snippet that solves one specific problem. Minimal prose — just enough context to understand when you'd use it. These are what people find through search engines.
- **Troubleshooting**: "You might be tempted to do X — here's why that won't work." Collects anti-patterns, common mistakes, and their fixes. Also a good place for FAQs that don't fit elsewhere.

## Workflow

### Step 1: Understand the Library

Before writing anything:

1. Read the library's public API surface — exported types, functions, interfaces
2. Look for existing documentation of any kind — READMEs, doc comments, wiki pages, examples directories
3. Identify the library's core abstraction — what's the one concept a user must understand to be productive?
4. Run the tests or examples to understand typical usage patterns
5. Note the library's opinion — what patterns does it encourage? What does it make easy vs. hard?

### Step 2: Write the Documentation

For each page:

1. **Start from the reader's goal**, not the library's structure. A guide called "Working with Connections" starts with what the user wants to do, not with `ConnectionPool`'s constructor signature.
2. **Pull real examples from the codebase.** Read source files to extract actual types and method signatures. If the library has an `examples/` directory or test files, use those as the basis for documentation examples.
3. **Build examples incrementally.** Start with the simplest possible usage, then layer in options and configuration. Don't front-load complexity.
4. **Link between pages.** When a guide mentions a concept, link to the concept page. When a recipe is a simplified version of a guide, link to the full guide. Cross-linking makes docs navigable.
5. **End guides with a complete example.** After walking through steps, show the final result assembled in one place. Readers often skip to this.

### Step 3: Review Against the Code

After writing:

1. Verify every code example compiles or runs against the current codebase
2. Check that type names, method signatures, and return values match the actual API
3. Confirm that the "getting started" path actually works end to end
4. Ensure cross-page links resolve correctly

## Writing Style

### Voice

- **Direct**: "Create a client" not "You may wish to consider creating a client"
- **Honest**: "This is verbose, but it gives you full control" not "This elegant API..."
- **Grounded**: "This returns an error if the connection drops" not "This might sometimes possibly fail"
- **Personality without performance**: It's fine to write "That's it — you're done" after a getting-started section. It's not fine to open every page with a pun.

### Code Examples

- Always use the library's actual types and methods — never invent simplified versions
- Include import paths when showing code for the first time on a page
- Show error handling in examples — don't hand-wave it with `// handle error`
- Keep examples minimal but complete — a reader should be able to copy-paste and run
- Use comments in code sparingly, only to highlight non-obvious steps

### Cross-Referencing

- Link to related guides, concepts, and recipes within the docs
- When mentioning an API type or function for the first time on a page, link to the auto-generated API reference if one exists
- Use reference-style links (`[text][ref]` with `[ref]: path` at the bottom of the file)

## Rules

- **Never write pseudocode** — every code example must use real types from the actual codebase
- **Never duplicate API reference docs** — link to auto-generated references instead of reproducing signatures
- **Never create concept pages preemptively** — only when there's a genuine source of confusion that guides alone can't address
- **Never document internals** — users don't need to know how the library works inside, only how to use it
- **One task per guide** — if a guide answers two questions, split it into two guides
- **Recipes are atomic** — each recipe solves one problem in one code block with minimal prose
- **Keep getting-started ruthlessly short** — the reader's patience is at its lowest here; get them to "it works" fast
- **Use reference-style links** — when linking between pages or to source files, use reference links for readability and maintainability
- **Match the library's terminology** — use the same names the API uses, don't invent synonyms
