---
name: shadcn-component-discovery
description: Discover existing shadcn components from registries before building custom. Use PROACTIVELY when about to build any UI component, page section, or layout. Use when user explicitly asks to find/search components. Searches 1,500+ components across official and community registries including @shadcn, @blocks, @reui, @animate-ui, @diceui, Magic UI, and 30+ specialty registries. Provides install commands and code examples. Works best with shadcn MCP configured, but provides manual guidance without it.
---

# shadcn Component Discovery

Stop reinventing the wheel. Search 1,500+ existing shadcn components before building custom.

## Core Principle

**ALWAYS search before building.** The shadcn ecosystem has components for almost everything. A 5-second search can save hours of development.

## When to Use This Skill

### Proactive Triggers (Search Automatically)

Activate this skill BEFORE writing component code when:

- Building any UI component (tables, forms, modals, etc.)
- Creating page layouts or sections
- Adding animations or interactions
- Implementing common patterns (auth, dashboards, settings)

### Explicit Triggers (User Requests)

Activate when user says things like:

- "Find a component for..."
- "Is there a shadcn component for..."
- "Search registries for..."
- "What components exist for..."
- `/find-component`, `/discover`, `/search-shadcn`

## Discovery Workflow

### Step 1: Identify What's Needed

Before searching, clarify:
- What functionality is needed?
- What style/aesthetic? (animated, minimal, accessible, etc.)
- Any specific requirements? (drag-drop, keyboard nav, etc.)

### Step 2: Search Registries

**With shadcn MCP configured (recommended):**

```
1. mcp__shadcn__search_items_in_registries
   - registries: ["@shadcn", "@animate-ui", "@diceui", "@blocks", "@reui"]
   - query: [search term]
   - limit: 10

2. For promising results, get details:
   mcp__shadcn__view_items_in_registries
   - items: ["@registry/component-name"]

3. For code examples:
   mcp__shadcn__get_item_examples_from_registries
   - query: "component-demo"

4. Get install command:
   mcp__shadcn__get_add_command_for_items
   - items: ["@registry/component-name"]
```

**Without MCP:**
- Consult [references/registries.md](references/registries.md) for registry recommendations
- Provide links to browse manually
- Suggest adding shadcn MCP for full search capabilities

### Step 3: Present Findings (Adaptive Format)

Choose response format based on context:

#### Quick Check (During Build)

Use when proactively checking before building. Minimal interruption.

```markdown
Before building a custom [component], I found existing options:

1. **@registry/component-name** - [brief description]
2. **@registry/other-option** - [brief description]

→ Install one of these, or build custom?
```

#### Standard Discovery (Explicit Search)

Use when user explicitly asks to find components.

```markdown
## Component Discovery: "[search term]"

Found **[N] matches** across [N] registries. Top recommendations:

### 1. @registry/component-name ⭐ Recommended
[Description of what it does]
- **Why it fits:** [reason this matches the need]
- **Features:** [key capabilities]
```bash
npx shadcn@latest add @registry/component-name
```

### 2. @registry/alternative
[Description]
- **Why it fits:** [reason]
```bash
npx shadcn@latest add @registry/alternative
```

### 3. @registry/another-option
[Description]
```bash
npx shadcn@latest add @registry/another-option
```

---
**Options:** [1] Install recommended | [2-3] Install alternative | [More] See all results | [Custom] Build from scratch
```

#### Detailed Comparison (Complex Choices)

Use when multiple good options exist and choice matters.

```markdown
## Component Discovery: "[search term]"

| Component | Registry | Best For | Complexity |
|-----------|----------|----------|------------|
| **option-1** | @registry | [use case] | Low/Med/High |
| **option-2** | @registry | [use case] | Low/Med/High |
| **option-3** | @registry | [use case] | Low/Med/High |

### Recommendation: @registry/option-1

[Explain why this is the best fit for their specific needs]

**Key features:**
- ✅ [feature 1]
- ✅ [feature 2]
- ✅ [feature 3]

**Install:**
```bash
npx shadcn@latest add @registry/option-1
```

Want to see a code example before deciding?
```

#### No MCP Fallback

Use when shadcn MCP is not configured.

```markdown
## Component Discovery: "[search term]"

⚡ **Pro tip:** Configure the [shadcn MCP](https://github.com/nicholasoxford/shadcn-mcp) for instant search across 1,500+ components with code examples and one-click installs.

Based on your needs, check these registries:

| Registry | Why | Browse |
|----------|-----|--------|
| **@reui** | [has relevant components] | [reui.dev](https://reui.dev) |
| **@animate-ui** | [has relevant components] | [animate-ui.com](https://animate-ui.com) |

**To enable full discovery:**
```bash
# Install shadcn MCP for your AI coding tool
# See: https://github.com/nicholasoxford/shadcn-mcp
```

Or browse all registries: [registry.directory](https://registry.directory)

---
Should I build custom, or check these registries first?
```

### Step 4: Execute User Choice

Based on user selection:

- **Install component:** Run the add command, then customize as needed
- **See more results:** Show additional matches with pagination
- **View example:** Fetch and display code example
- **Build custom:** Proceed with custom implementation (still reference the existing component for patterns)

## Search Strategy

### Effective Search Terms

| Looking for... | Try searching... |
|----------------|------------------|
| Data display | `table`, `data-grid`, `list` |
| User input | `form`, `input`, `field`, `select` |
| Navigation | `sidebar`, `nav`, `menu`, `tabs` |
| Feedback | `toast`, `alert`, `notification` |
| Overlays | `modal`, `dialog`, `sheet`, `popover` |
| Media | `carousel`, `gallery`, `image` |
| Animation | `animate`, `motion`, `transition` |
| Layout | `card`, `section`, `hero`, `grid` |

### Registry Specialties

Quick reference for which registries to prioritize:

| Need | Check First |
|------|-------------|
| Basic UI primitives | @shadcn |
| Page sections/blocks | @blocks |
| Data tables/grids | @reui |
| Animations | @animate-ui, Magic UI |
| AI/Chat interfaces | AI Elements, assistant-ui |
| Accessibility | @diceui, JollyUI |

See [references/registries.md](references/registries.md) for complete catalog.

## Response Requirements

Every discovery response MUST include:

1. **Search term used** - What was searched
2. **Match count** - How many results found
3. **Top 3 recommendations** - Best matches with:
   - Component name and registry
   - Brief description
   - Why it fits the need
   - Install command
4. **Clear options** - What user can do next
5. **Recommendation** - Which one to use (when clear winner exists)

## Examples

### Example 1: Proactive Check

**Situation:** User asks "Add a data table to show user accounts"

**Agent response:**
```markdown
Before building a custom data table, I found these existing options:

1. **@reui/data-grid-table** - Full-featured grid with sorting, filtering, pagination
2. **@blocks/table-05** - Pre-styled data table block
3. **@shadcn/table** - Basic table primitives

→ The @reui/data-grid-table looks perfect for user accounts. Install it?
```

### Example 2: Explicit Search

**Situation:** User asks "Find me an animated accordion"

**Agent response:**
```markdown
## Component Discovery: "animated accordion"

Found **8 matches** across 5 registries. Top recommendations:

### 1. @animate-ui/components-base-accordion ⭐ Recommended
Smooth animated accordion with enter/exit transitions.
- **Why it fits:** Built-in animations, accessible, customizable timing
- **Features:** Keyboard nav, ARIA compliant, Motion powered
```bash
npx shadcn@latest add @animate-ui/components-base-accordion
```

### 2. @shadcn/accordion
Standard accordion (no built-in animation).
- **Why it fits:** Simple, lightweight, easy to add custom animations
```bash
npx shadcn@latest add @shadcn/accordion
```

---
**Options:** [1] Install animated | [2] Install basic + add animations | [Custom] Build from scratch
```

### Example 3: No Good Match

**Situation:** Search returns no relevant results

**Agent response:**
```markdown
## Component Discovery: "quantum flux capacitor"

No existing components found for this specific need.

**Closest matches:**
- @shadcn/card - Could be adapted as a container
- @animate-ui/components-backgrounds-gradient - For visual effects

Since this is a unique component, I'll build it custom.
Want me to check any specific registries first, or proceed with custom build?
```

## Best Practices

### Do

- Search BEFORE writing any component code
- Present multiple options when available
- Explain WHY each option fits (or doesn't)
- Include ready-to-run install commands
- Offer to show code examples

### Don't

- Skip searching because "it's faster to build"
- Present too many options (3-5 max)
- Forget to mention the install command
- Assume user wants the first result
- Build custom without at least checking first

## Resources

- **Registry Catalog:** [references/registries.md](references/registries.md)
- **Registry Browser:** [registry.directory](https://registry.directory)
- **Official Blocks:** [ui.shadcn.com/blocks](https://ui.shadcn.com/blocks)
- **Component Index:** [shadcnregistry.com](https://shadcnregistry.com)
- **shadcn MCP:** [github.com/nicholasoxford/shadcn-mcp](https://github.com/nicholasoxford/shadcn-mcp)
