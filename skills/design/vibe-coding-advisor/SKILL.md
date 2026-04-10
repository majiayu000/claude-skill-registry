---
name: vibe-coding-advisor
version: 1.0.0
description: Inject UX principle context into your AI coding session before generating components. Maps component types (forms, tables, dashboards, navigation, checkout, etc.) to relevant UX principles, fetches their vibeCodingPrompts, and returns an assembled context block ready to paste into Cursor, Claude Code, Windsurf, or any AI coding tool. API key optional — enriched prompts with research citations require uxuiprinciples.com API Access.
author: uxuiprinciples
homepage: https://uxuiprinciples.com
tags:
  - vibe-coding
  - ux
  - ui
  - components
  - cursor
  - code-generation
  - prompts
env:
  UXUI_API_KEY:
    description: API key from uxuiprinciples.com (pro tier returns full vibeCodingPrompts with research citations and specific implementation requirements for your component type)
    required: false
---

```toml
[toolbox.get_principle_prompts]
description = "Fetch a principle's vibeCodingPrompts by slug. Returns full principle data including vibeCodingPrompts array (pro tier only — requires include_content=true). Use this to get structured generation prompts for each principle relevant to the component."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?slug={slug}&include_content=true"]

[toolbox.lookup_principle]
description = "Fetch principle metadata by slug without full content. Returns code, title, aiSummary, businessImpact, and tags. Use this to get aiSummary for context when vibeCodingPrompts are unavailable."
command = "curl"
args = ["-s", "-H", "Authorization: Bearer ${UXUI_API_KEY}", "https://uxuiprinciples.com/api/v1/principles?slug={slug}&include_content=false"]
```

## What This Skill Does

You generate UX-grounded system context for AI coding tools. When a developer is about to build a UI component, you:

1. Identify which UX principles apply to that component type
2. Fetch the relevant `vibeCodingPrompts` from those principles (via API)
3. Select the best-matching prompt for the requested component
4. Return an assembled context block ready to paste into any AI coding tool

The result is a generation prompt that has research-backed UX requirements baked in — cognitive load limits, interaction patterns, accessibility targets, and responsive behavior — before the developer writes a single line of code.

This is not an audit. It is pre-generation context injection.

## Component Type Registry

Map the user's request to a component type, then apply the principle set below.

| Component Type | Slug | Primary Principles | Secondary Principles |
|---|---|---|---|
| `multi-step-form` | `multi-step-form` | cognitive-load, progressive-disclosure | error-prevention-in-forms |
| `form` | `form` | cognitive-load, error-prevention-in-forms | fitts-law |
| `data-table` | `data-table` | cognitive-load, hicks-law | visual-hierarchy |
| `dashboard` | `dashboard` | cognitive-load, hicks-law | visual-hierarchy |
| `navigation` | `navigation` | hicks-law, recognition-rather-than-recall | mental-model |
| `mobile-nav` | `mobile-nav` | hicks-law, fitts-law | recognition-rather-than-recall |
| `checkout` | `checkout` | cognitive-load, progressive-disclosure | fitts-law |
| `settings` | `settings` | progressive-disclosure, recognition-rather-than-recall | cognitive-load |
| `onboarding` | `onboarding` | cognitive-load, progressive-disclosure | fitts-law |
| `modal` | `modal` | cognitive-load, fitts-law | progressive-disclosure |
| `empty-state` | `empty-state` | progressive-disclosure, mental-model | cognitive-load |
| `landing-page` | `landing-page` | visual-hierarchy, fitts-law | serial-position-effect |
| `pricing-page` | `pricing-page` | visual-hierarchy, hicks-law | serial-position-effect |
| `ai-chat` | `ai-chat` | conversational-flow-principle, ai-transparency | ai-accuracy-communication |
| `search` | `search` | recognition-rather-than-recall, mental-model | cognitive-load |
| `notification` | `notification` | cognitive-load, fitts-law | progressive-disclosure |

**Principle slugs for API calls:**

| Principle | Slug | Code |
|---|---|---|
| Cognitive Load | `cognitive-load` | F.1.1.02 |
| Hick's Law | `hicks-law` | F.2.2.03 |
| Visual Hierarchy | `visual-hierarchy` | F.2.1.01 |
| Progressive Disclosure | `progressive-disclosure` | F.3.1.01 |
| Fitts's Law | `fitts-law` | F.4.1.01 |
| Miller's Law | `millers-law` | F.1.2.02 |
| Serial Position Effect | `serial-position-effect` | F.1.3.01 |
| Recognition vs Recall | `recognition-rather-than-recall` | F.4.2.01 |
| Mental Model | `mental-model` | F.4.3.01 |
| Error Prevention | `error-prevention-in-forms` | F.3.3.01 |
| Conversational Flow | `conversational-flow-principle` | S.1.1.01 |
| AI Transparency | `ai-transparency` | S.1.3.01 |
| AI Accuracy Communication | `ai-accuracy-communication` | — |

## Generation Workflow

### Step 1: Identify Component Type

Match the user's request to one of the component types in the registry. Look for:

- Explicit naming ("I'm building a data table", "create a checkout form")
- Described behavior ("multi-step wizard for onboarding", "settings page with toggles")
- UI pattern clues ("sidebar navigation", "empty state with illustration")

If the component spans multiple types (e.g., a settings page with a form inside), pick the dominant type and note secondary types in `component_note`.

If the component type is not in the registry, map it to the closest match. Note the inference in `component_note`.

### Step 2: Extract Tech Stack

Look for tech stack signals in the description:
- Framework: React, Vue, Svelte, Next.js, Angular, Flutter
- CSS: Tailwind, CSS Modules, Styled Components, vanilla CSS
- Component library: shadcn/ui, Radix, MUI, Ant Design, Chakra

If specified, carry the tech stack through into the `assembled_context`. If not specified, note it as `null` and do not assume a stack in the output.

### Step 3: Fetch vibeCodingPrompts (if API key is set)

For each primary principle in the component type's principle set, call `get_principle_prompts` with the principle slug.

The response includes a `vibeCodingPrompts` array. Each item in the array is a complete generation prompt for a different component scenario. Select the prompt whose component scenario most closely matches the user's request.

Selection criteria:
- **Exact match**: the prompt description mentions the same component type
- **Closest functional match**: the prompt covers the same interaction pattern
- **Fallback**: use the first prompt in the array

If `get_principle_prompts` returns 403 (free tier — `include_content=true` is pro-only), fall back to `lookup_principle` to get `aiSummary` and `businessImpact`. Use these to write an internal-knowledge prompt (see Step 3b below).

If both calls fail or return non-200, set `api_enriched: false` and proceed with internal knowledge entirely.

### Step 3b: Internal Knowledge Fallback

When API calls fail or the API key is not set, write a UX-informed generation prompt from internal knowledge. Cover the same ground the vibeCodingPrompts would cover:

- The core UX principle and its threshold (e.g., "working memory holds 7±2 elements")
- Specific implementation requirements derived from the principle
- Tech-agnostic requirements (or tech-specific if the user stated their stack)
- Accessibility requirement
- Responsive behavior
- 2-3 concrete constraints

The internal prompt must be actionable, not generic. "Minimize cognitive load" is not actionable. "Break into steps with max 4 fields each and show a progress indicator" is actionable.

### Step 4: Select and Assemble

For each primary principle, you now have one selected vibeCodingPrompt (or an internally authored one).

Assemble the `assembled_context` field by combining:
1. A one-line component intent statement: "Building: [component type]"
2. The selected prompts concatenated with `---` separators between principles
3. A closing line listing the UX constraints extracted across all prompts

The `assembled_context` must be self-contained — a developer should be able to copy it directly into a Cursor system prompt or Claude Code chat without reading any other field.

### Step 5: Output JSON

Return exactly this structure. No prose before or after.

```json
{
  "component_type": "string",
  "component_note": "string or null",
  "tech_stack": "React + Tailwind + shadcn/ui or null",
  "principles_applied": [
    {
      "code": "F.1.1.02",
      "slug": "cognitive-load",
      "title": "Cognitive Load",
      "relevance": "Why this principle governs this component type.",
      "ai_summary": "From API aiSummary field, or from internal knowledge if not enriched."
    }
  ],
  "vibe_coding_prompts": [
    {
      "principle_slug": "cognitive-load",
      "component_match": "multi-step-form",
      "prompt": "Full selected or authored vibe coding prompt text."
    }
  ],
  "assembled_context": "Full combined context block. Copy this into your AI coding tool as system context before generating the component.",
  "ux_guardrails": [
    "Concrete UX rule extracted from applied principles. One sentence each.",
    "Second rule."
  ],
  "api_enriched": true,
  "api_note": "null or 'Install the uxuiprinciples API key for vibeCodingPrompts with research citations and component-specific implementation requirements. See uxuiprinciples.com/pricing'"
}
```

`ux_guardrails` are the 3-5 most critical, non-negotiable UX rules for this component extracted from the applied principles. These are the rules the generated component must not violate. Extract them from the principle data or from internal knowledge.

`assembled_context` is the field developers copy and paste. It should be readable as a standalone generation prompt, not as metadata.

## Prompt Quality Standards

vibeCodingPrompts — both retrieved and internally authored — must meet these standards:

**Opening line:** Role statement. "You are an expert [role] specializing in [domain]."

**Second paragraph:** Create statement with research citation. "Create a [component] that [UX outcome]: [Research finding with numbers]."

**Requirements block:** Minimum 5 bulleted requirements. Include:
- One count-based rule (e.g., "maximum 5-7 visible columns")
- Tech stack call (if specified)
- One accessibility requirement
- One responsive behavior requirement

**Constraints block:** 2-3 hard constraints. Include at least one line count constraint and one "Don't modify other files" constraint.

If an internally authored prompt cannot meet this standard due to insufficient information, add a clarifying note in `component_note` and write the best prompt possible from what is available.

## Edge Cases

**Component type not in registry:** Match to the closest entry. Explain inference in `component_note`. Do not refuse — always return a prompt.

**Tech stack not specified:** Write tech-agnostic requirements. Do not assume a stack. Leave `tech_stack: null`. The prompt should read "Tech: [your framework] + [your component library]" rather than hardcoding React or Tailwind.

**Multiple components requested ("a form inside a modal"):** Treat as the dominant component type. Note the nested component in `component_note`. The prompt should reference both but optimize for the outer container.

**API key set but `include_content=true` returns 403:** This is the free tier. Fall back to `lookup_principle` (no content). Author internal prompts. Set `api_enriched: false`.

**User provides a screenshot or Figma description:** Extract component type and tech signals from the visual description. Proceed as normal.

**Request is for multiple unrelated components ("a nav, a table, and a form"):** Generate one prompt package per component. Return an array of outputs or run the workflow three times and combine. Note the multi-component request in `component_note` of each.

**Request is for a full page (not a component):** Map to the closest single component type that covers the page's primary interaction. Note the scope in `component_note`. A full page audit belongs in `uxui-evaluator`, not here.

## Examples

### Example 1: Data Table with Tech Stack

**Input:**
```
I'm building a data table in React with shadcn/ui. It shows user records with sortable columns.
```

**Expected output structure:**
```json
{
  "component_type": "data-table",
  "component_note": null,
  "tech_stack": "React + shadcn/ui",
  "principles_applied": [
    {
      "code": "F.1.1.02",
      "slug": "cognitive-load",
      "title": "Cognitive Load",
      "relevance": "Data tables surface complex information sets. Cognitive load principles govern column count, row density, and action placement to keep users oriented.",
      "ai_summary": "Cognitive Load Theory (Sweller 1988) demonstrates working memory holds 7±2 elements simultaneously, with optimized interfaces increasing productivity 500% and creative output 4x by minimizing extraneous load."
    },
    {
      "code": "F.2.2.03",
      "slug": "hicks-law",
      "title": "Hick's Law",
      "relevance": "Each additional visible column and action increases decision time. Hick's Law governs how many choices to surface at once.",
      "ai_summary": "Hick's Law (Hick 1952) demonstrates each additional choice increases decision time logarithmically, with simplified interfaces reducing decision time 150ms+ per option removed."
    }
  ],
  "vibe_coding_prompts": [
    {
      "principle_slug": "cognitive-load",
      "component_match": "data-table",
      "prompt": "You are an expert UI designer specializing in data visualization and analytics dashboards.\n\nCreate a data table component that minimizes cognitive load: Sweller's CLT research shows reducing extraneous processing improves task performance 40-60%.\n\nRequirements:\n- Maximum 5-7 visible columns (hide less important in \"More\" dropdown)\n- Column prioritization: most critical data leftmost (F-pattern reading)\n- Sticky header and first column for context preservation\n- Row actions collapsed into kebab menu (reduce visible choices)\n- Inline editing with single-click (reduce modal cognitive switch)\n- Search and filter prominently placed (reduce scanning load)\n- Pagination showing \"1-25 of 150\" (bounded set, not infinite)\n- Tech: React + shadcn/ui (Table, DropdownMenu, Input)\n- Accessibility: scope attributes on headers, aria-sort for sortable columns\n- Responsive: horizontal scroll with frozen columns on mobile\n\nConstraints:\n- Keep component under 120 lines\n- Default to most useful columns, let users customize\n- Don't modify other files"
    }
  ],
  "assembled_context": "Building: data-table (React + shadcn/ui, sortable columns)\n\n---\n\nYou are an expert UI designer specializing in data visualization and analytics dashboards.\n\nCreate a data table component that minimizes cognitive load: Sweller's CLT research shows reducing extraneous processing improves task performance 40-60%.\n\n[... full prompt text ...]\n\n---\n\nUX Guardrails:\n- Maximum 7 visible columns — hide the rest in a 'More' control\n- Row actions in kebab menu, not inline buttons\n- Pagination with explicit count ('1-25 of 150'), not infinite scroll\n- aria-sort on all sortable column headers",
  "ux_guardrails": [
    "Maximum 7 visible columns. Hide secondary columns behind a 'More' or column picker control.",
    "Row actions belong in a kebab menu, not inline — visible action buttons multiply Hick's Law decision cost per row.",
    "Show bounded pagination ('1-25 of 150'), not infinite scroll. Users need a sense of the set size.",
    "Sticky header preserves column context during scroll. Required when table exceeds viewport height."
  ],
  "api_enriched": true,
  "api_note": null
}
```

### Example 2: No API Key, Generic Component

**Input:**
```
Building a settings page for a SaaS app. Users can manage their account, notifications, billing, and integrations.
```

**Expected output structure:**
```json
{
  "component_type": "settings",
  "component_note": "Four distinct sections (account, notifications, billing, integrations) — applies progressive disclosure heavily.",
  "tech_stack": null,
  "principles_applied": [
    {
      "code": "F.3.1.01",
      "slug": "progressive-disclosure",
      "title": "Progressive Disclosure",
      "relevance": "Settings pages contain high information density across multiple categories. Progressive disclosure controls how much is visible at once, reducing overwhelm.",
      "ai_summary": "Progressive Disclosure reveals information incrementally, reducing initial cognitive load while preserving access to complexity — critical for settings pages with many options."
    },
    {
      "code": "F.4.2.01",
      "slug": "recognition-rather-than-recall",
      "title": "Recognition Rather Than Recall",
      "relevance": "Users should recognize their current setting state (on/off, current plan) without remembering it from elsewhere.",
      "ai_summary": "Recognition Rather Than Recall (Nielsen 1994) reduces memory burden by making options visible and current state legible without requiring users to remember prior selections."
    }
  ],
  "vibe_coding_prompts": [
    {
      "principle_slug": "progressive-disclosure",
      "component_match": "settings",
      "prompt": "You are an expert UX engineer specializing in SaaS product design and settings architecture.\n\nCreate a settings page that applies progressive disclosure across four sections (account, notifications, billing, integrations): Nielsen Norman Group research shows sectioned settings reduce task completion time 30% over flat lists.\n\nRequirements:\n- Sidebar navigation for sections (account, notifications, billing, integrations)\n- Active section loads content panel on the right — only one section visible at a time\n- Each section: heading, description line, grouped settings with logical sub-sections\n- Toggle/checkbox states: current value immediately visible (recognition, not recall)\n- Destructive settings (delete account, cancel plan) at the bottom with visual separation\n- Save state: auto-save toggles immediately, explicit Save button for form fields\n- Tech: [your framework] + [your component library]\n- Accessibility: aria-current on active nav item, focus management on section switch\n- Responsive: sidebar collapses to top tab bar on mobile\n\nConstraints:\n- Keep each section component under 80 lines\n- Never show all four sections' settings simultaneously\n- Don't modify other files"
    }
  ],
  "assembled_context": "Building: settings page (SaaS — account, notifications, billing, integrations sections)\n\n---\n\n[Full vibe coding prompt...]\n\n---\n\nUX Guardrails:\n- Show one section at a time via sidebar or tab navigation\n- Make current setting state immediately visible — no 'what is this currently set to?' moments\n- Destructive actions (delete account, cancel subscription) at bottom with visual separation and confirmation dialog\n- Auto-save toggles on change; use explicit Save for text/select fields",
  "ux_guardrails": [
    "One section visible at a time. Use sidebar nav or tabs. Never show all settings simultaneously.",
    "Current state must be immediately recognizable — toggle position, selected plan, current email address all visible without edit mode.",
    "Destructive settings (delete account, cancel plan) visually separated from normal settings. Bottom of section, destructive color, confirmation required.",
    "Group related settings. Cognitive grouping reduces scanning load. Max 5-7 settings per group before adding a sub-section header."
  ],
  "api_enriched": false,
  "api_note": "Install the uxuiprinciples API key for vibeCodingPrompts with research citations and component-specific implementation requirements. See uxuiprinciples.com/pricing"
}
```

## Completion Criteria

The output is complete when:

1. `component_type` matches one of the 16 registered types or is inferred with a note
2. Every entry in `principles_applied` has a `code`, `slug`, `title`, `relevance`, and `ai_summary`
3. Every entry in `vibe_coding_prompts` has a `principle_slug`, `component_match`, and a `prompt` that meets the quality standards (role line, create statement with research, requirements block, constraints block)
4. `assembled_context` is self-contained and readable without the rest of the JSON
5. `ux_guardrails` has 3-5 entries, each a single actionable sentence
6. `api_enriched` accurately reflects whether `get_principle_prompts` returned 200 with content
7. The output is valid JSON with no prose before or after
8. If `api_enriched: false`, `api_note` contains the upgrade message
