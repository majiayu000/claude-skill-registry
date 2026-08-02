---
name: domain-modeling
description: 'Build and sharpen a project''s ubiquitous language as you design: challenge terms against the glossary, sharpen fuzzy ones, and write CONTEXT.md the moment a term resolves. Use when pinning down domain terminology or maintaining the domain model. Not the `contexts` skill, which routes pre-implementation context gathering.'
---

# Domain modeling

This skill maintains a project's domain glossary. It has nothing to do with the `contexts` skill, which routes pre-implementation context gathering.

Use this skill to change the model, not merely to read it.

## File layout

- For one context, keep `CONTEXT.md` at the repository root.
- For several contexts, keep `CONTEXT-MAP.md` at the root. Put each context's `CONTEXT.md` beside that context's source.

Create these files lazily. Do not create a file until there is something to record.

Load `references/CONTEXT-FORMAT.md` before creating or updating either format.

## Work during the session

1. **Challenge conflicting terms.** Compare each term with the glossary and call out a conflict at once. Example: "The glossary defines cancellation as ending an Order, but this use changes one Line Item. Which meaning is correct?"
2. **Sharpen fuzzy terms.** Replace vague or overloaded language with one canonical term. Example: "Does account mean Customer or User? Pick the domain term that owns this rule."
3. **Stress-test relationships.** Invent an edge case that forces boundaries into view. Example: "If Fulfillment splits one Order across two shipments, when may Billing issue the invoice?"
4. **Check claims against code.** Read the implementation and surface contradictions. Example: "The code cancels the full Order, but the model allows partial cancellation. Which one is authoritative?"
5. **Update the glossary inline.** Write the resolved term to `CONTEXT.md` immediately. Example: after choosing Customer over account, add Customer and its rejected synonyms before continuing.

`CONTEXT.md` is a glossary and nothing else. Keep implementation details, specification content, and scratch notes out of it.

## Architecture decisions

Use `docs-and-adrs/references/adrs.md` for the ADR gate and format. Keep the decision criteria in that one place.
