---
name: authoring-stitch-prompts
description: Converts natural-language descriptions or UI spec files into optimized Google Stitch prompts. Use when creating, refining, or validating design directives for Google Stitch. Use when user says "create a Stitch prompt", "optimize this for Stitch", "convert this spec to a Stitch prompt", "write a UI prompt", or mentions Google Stitch prompt authoring. Follows Stitch best practices with short, directive prompts focused on screens, structure, and visual hierarchy.
---

# Authoring Stitch Prompts

## Quick Start
1. **Collect context** – accept natural language, specs, or referenced files describing the screen/app.
1.5. **Discover design context** (optional) – check for `design-intent/`:
   - If exists: Extract Project Type, Design System from `design-intent/memory/constitution.md`
   - If not found: Scan codebase for framework hints (package.json)
   - Falls back gracefully to standalone mode
   - See [WORKFLOW.md](WORKFLOW.md#05-design-context-discovery-optional-enhancement) for details.
2. **Parse essentials** – identify app type, screen focus, layout elements, and visual cues.
3. **Detect split points** – analyze if input contains multiple screens or distinct intents (>2). Apply smart defaults: split if >2 screens/intents, else combine. Users can request regeneration with different approach.
4. **Filter aggressively** – strip ALL non-UI concerns (backend, auth, APIs, caching, error handling, performance metrics, code-level specs). Focus EXCLUSIVELY on visual layout, components, colors, typography, spacing, and interaction patterns.
5. **Condense** – rewrite into one atomic Stitch directive using "Design/Create/Add…" phrasing.
6. **Structure output** – follow the Stitch prompt template (directive sentence → bullet list → 3–6 style cues → constraints). If design context was discovered, inject project-appropriate style cues. Do NOT use multi-section headings.
7. **Validate** – ensure UI nouns are present, word count <250, NO technical implementation terms, and format matches EXAMPLES.md structure before returning the prompt.

Use this Skill whenever users need Stitch-ready wording, prompt refinements, or style-consistent rewrites.

---

## File Output

Prompts are saved to feature-based directories under `design-intent/google-stitch/{feature}/`:
- **Feature name** derived from screen/page purpose (kebab-case, semantic, concise)
- **Prompt files**: `prompt-v{version}.md` (auto-incremented from existing versions)
- **Pre-created subdirectories**: `exports/` (Stitch outputs) and `wireframes/` (reference mockups)
- **File composition**: `<!-- Layout: {Name} -->` header, then `---` separators between component sections (`<!-- Component: {Name} -->`)
- **6-prompt Stitch limit**: If >6 prompts, split into `prompt-v{version}-part{N}.md` files (max 6 per part)
- **Copy-paste ready**: Entire file works directly in Stitch interface

See [WORKFLOW.md](WORKFLOW.md#35-generate-layout-prompt-if-detected) for detailed file composition rules, [REFERENCE.md](REFERENCE.md) for Stitch best practices, and [EXAMPLES.md](EXAMPLES.md) for worked examples (Examples 14–16 cover multi-component and split scenarios).

---

## Input Types

**Accepted**
- Natural-language descriptions (single screen or short flows)
- Markdown/YAML/JSON specs (`/specs/dashboard.md`)
- Revision directives ("move KPI cards above chart", "convert to French", "change button to green")
- References to uploaded wireframes or images
- Language conversion requests ("switch to Spanish", "German version")
- Structured input from `/prompt` command (see below)

---

## Structured Input (from /prompt command)

When invoked via `/prompt`, the skill may receive pre-parsed preferences (`Brief`, `Components`, `Style`, `Structure`). Parse structured fields and apply style mappings before proceeding. See [WORKFLOW.md](WORKFLOW.md#08-parse-structured-input-if-present) for field handling and style mapping tables.

All input detail levels are valid — Stitch infers patterns from minimal descriptions. Use adjectives to convey vibe when details are sparse ("vibrant fitness app", "minimal meditation app").

---

## Workflow Overview

High-level loop: parse → condense → format → validate.
Detailed branching logic, including cue extraction and revision handling, lives in [WORKFLOW.md](WORKFLOW.md).

---

## Output Structure

Prompts must follow the Stitch-friendly template:
- One-sentence description of the app/screen + primary intent.
- Bullet list (3–6 items) covering layout, components, or flows.
- Visual style cues (palette, typography, density, tone).
- Optional behavior/constraint reminders (responsiveness, export format).

Reference [templates/authoring-stitch-prompts-template.md](templates/authoring-stitch-prompts-template.md) for wording patterns and [templates/layout-prompt-template.md](templates/layout-prompt-template.md) for layout/foundation prompts.

---

## Examples

Representative before/after samples (SaaS dashboard, banking app, iterative edits, spec conversions) are in [EXAMPLES.md](EXAMPLES.md). Use them to mirror tone and formatting; keep this file lean by not re-embedding the full transcripts here.

---

## Design Context Integration

When `design-intent/` exists in the project, the skill enhances style cues with project context:

- **Project Type** influences tone (e.g., "enterprise-grade" for Enterprise, "friendly, approachable" for Consumer)
- **Design System** names appear in style cues (e.g., "Fluent UI styling", "Material Design patterns")

The skill does NOT inject specific tokens (hex colors, spacing values)—only high-level descriptors that help Stitch generate contextually appropriate designs.

**Fallback behavior**: If `design-intent/` is not found, the skill works standalone using default style cues.

See [WORKFLOW.md](WORKFLOW.md#05-design-context-discovery-optional-enhancement) for discovery logic and [WORKFLOW.md](WORKFLOW.md#37-inject-design-context-into-style-cues) for injection rules.

---

## MCP Integration (Optional)

When `@_davideast/stitch-mcp` is configured, prompts can be sent directly to Stitch for generation after authoring.

**With MCP:** Author prompt -> Generate screens -> Fetch images/code
**Without MCP:** Author prompt -> Copy to Stitch manually

After authoring, offer: "Stitch MCP is available. Generate screens now? [Yes / No / Just save prompts]"

If accepted, invoke the `generating-stitch-screens` skill with the authored prompt file.

---

## Common Issues

- **Prompts too verbose** – Re-run formatting with the template and trim narration. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#prompts-are-too-verbose).
- **Missing style cues** – Derive palette/typography keywords from user input or prior session context before finalizing. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#missing-style-cues).
- **Multi-goal briefs** – Split into multiple prompts; re-emphasize Stitch's atomic focus. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md#multi-screen-prompts).

---

## Reference Files

For advanced usage:

* [REFERENCE.md](REFERENCE.md) — Overview of Stitch best practices
* [EXAMPLES.md](EXAMPLES.md) — Sample transformations
* [WORKFLOW.md](WORKFLOW.md) — Detailed processing loop
* [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Error-handling guidance
* [templates/authoring-stitch-prompts-template.md](templates/authoring-stitch-prompts-template.md) — Output format template
