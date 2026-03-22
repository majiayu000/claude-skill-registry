---
name: accessibility-writing
description: Guide creating accessible documentation and content for everyone
category: Communication Writing
---

# Skill: accessibility-writing

## What I do

I help you create documentation that everyone can read and understand. I focus on making content accessible to users with visual impairments, cognitive disabilities, or those who use assistive technology like screen readers. I ensure your technical writing is clear, structured, and inclusive.

## When to use me

- When you're writing READMEs, guides, or API docs.
- When you're adding images or diagrams to your documentation.
- When you're structuring complex information in tables or lists.
- When you're choosing link text or headings.

## Core principles

1. **Clarity over cleverness**, use plain language and avoid unnecessary jargon.
2. **Logical structure**, use headings to create a clear hierarchy that reflects the content's importance.
3. **Redundancy for resilience**, don't rely on colour or shape alone to convey meaning.
4. **Descriptive context**, ensure all non-text elements have meaningful text alternatives.

## Patterns & examples

### Plain language and reading levels
Aim for a reading level that's easy to grasp. Use short sentences and active voice.
- **Good**, "Run this command to start the server."
- **Bad**, "The execution of the following command is required for the initiation of the server process."

### Meaningful link text
Links should tell the user where they're going without needing to read the surrounding text.
- **Good**, "Read the [installation guide](/docs/install) for more details."
- **Bad**, "[Click here](/docs/install) to read more about installation."

### Heading hierarchy
Always use headings in a linear order. Don't skip levels just for styling.
- **Correct**, H1 -> H2 -> H3 -> H2 -> H3
- **Incorrect**, H1 -> H3 -> H5

### Alt text for diagrams
Describe what the diagram shows and why it matters.
- **Example**, `![Architecture diagram showing the flow of data from the client to the API via an authentication proxy](images/arch.png)`

## Anti-patterns to avoid

- ❌ **"Click here" links**, screen reader users often navigate via links alone. "Click here" gives no context.
- ❌ **Empty alt text**, leaving alt tags empty makes images invisible to screen readers, unless they're purely decorative.
- ❌ **Skipping heading levels**, this breaks the document's outline for assistive technology.
- ❌ **Relying on colour**, don't say "the red button" without adding a text label or icon.

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Communication-Writing/Accessibility Writing.md`

## Related skills

- `documentation-writing`, for general documentation structure.
- `writing-style`, to keep a consistent voice.
- `ui-design`, for visual accessibility in interfaces.
- `ux-design`, for inclusive user journeys.
