---
name: glossary
description: Build or update a CONTEXT.md domain glossary for the current project. Establishes shared vocabulary with term definitions, avoid-aliases, and relationships so agents use consistent, concise language. This skill should be used when starting a new project, when domain terminology is inconsistent across sessions, when the user says "build a glossary", "define our terms", "shared vocabulary", or "domain language", or when an existing CONTEXT.md needs updating after new domain concepts emerge.
---

# Glossary — Domain Language Builder

Build or update a `CONTEXT.md` at the project root that captures the project's domain language. A shared vocabulary between user and agent reduces verbosity (agents stop using 20 words where 1 domain term suffices), enforces consistent naming in code, and prevents terminology drift across sessions.

## Creating a new CONTEXT.md

If no `CONTEXT.md` exists at the project root, run an elicitation session to discover domain terms:

1. Explore the codebase to identify domain-specific naming patterns—types, modules, key abstractions, recurring nouns in variable names and comments.
2. Present findings to the user: "I found these domain concepts in the code: [list]. Which are worth defining? Are any named inconsistently?"
3. For each confirmed term, resolve four fields: the canonical name, a one-sentence definition, aliases to avoid, and relationships to other terms. These four fields are the minimum needed for an agent to use the term correctly and consistently—fewer leads to ambiguity, more adds noise.
4. Ask about ambiguities: "Is [term] the same as [similar term], or are they distinct?" Surface these early because unresolved synonyms are the primary source of naming inconsistency in agent-generated code.
5. Write `CONTEXT.md` following the format in [references/context-format.md](references/context-format.md).

## Updating an existing CONTEXT.md

If `CONTEXT.md` already exists, read it first. Then:

1. Identify the new concept or ambiguity that triggered this invocation.
2. Check whether it fits an existing term (update the definition) or is genuinely new (add it).
3. If the new concept conflicts with an existing term, add it to "Flagged ambiguities" with a clear resolution.
4. Preserve all existing content—append, don't rewrite. Rewriting destroys cross-session term provenance and risks silently dropping terms other sessions depend on.

## Consuming CONTEXT.md during other work

When exploring or modifying code in a project that has a `CONTEXT.md`:

- Read `CONTEXT.md` before starting work. Use its terms exactly—not synonyms the glossary explicitly avoids. Consistent terminology reduces the cognitive translation cost between domain conversations and implementation.
- Note any concepts needed for the current task that are missing from the glossary. Flag them as candidates for the next `/glossary` session.
- Name variables, functions, types, and files using the glossary's vocabulary.
