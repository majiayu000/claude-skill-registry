---
name: plaited-web-patterns
description: Default Web API patterns for bElement architecture, including modern HTML features, performance optimizations, and Shadow DOM compatible patterns. Use create-web-patterns-skill command to add additional pattern skills.
license: ISC
compatibility: Requires bun
allowed-tools: WebFetch, Write, Read, Glob, mcp__chrome-devtools__*
---

# Plaited Web Patterns

Extract modern HTML and Web API patterns from external sources and adapt them for Plaited's bElement architecture.

## Purpose

This skill activates when:
- Extracting patterns from web articles (web.dev, MDN, etc.)
- Analyzing Web API documentation for Plaited integration
- Adapting web APIs to work with bElement
- Creating new web pattern documentation

## Pattern Extraction

### Target Patterns

- Modern HTML features (dialog, popover, invokers, command pattern)
- Web APIs (Intersection Observer, Resize Observer, View Transitions)
- Performance optimizations (preconnect, fetchpriority, priority hints)
- Accessibility improvements (ARIA patterns, semantic HTML)
- Shadow DOM compatible patterns

### Extraction Workflow

1. Fetch URL with WebFetch tool
2. Identify patterns matching target criteria
3. Apply framework-first adaptation (see below)
4. Format using output template
5. Save to references/ directory

## Framework-First Adaptation

**CRITICAL**: Check what bElement already provides BEFORE reaching for web APIs.

### What bElement Provides

**BProgramArgs** (available in bProgram callback):
- `$` - Shadow DOM query selector with p-target matching
- `root` - ShadowRoot reference
- `host` - Custom element instance
- `internals` - ElementInternals API
- `trigger` - Internal event dispatcher
- `emit` - Cross-element event dispatcher

**Automatic Systems**:
- **p-trigger**: Declarative event binding with automatic delegation
- **p-target**: Helper methods (render, insert, replace, attr)
- **Shadow DOM**: Automatic via shadowDom parameter
- **Lifecycle**: Callback handlers (onConnected, onDisconnected, etc.)
- **Form Association**: formAssociated: true enables ElementInternals

**Before using ANY web API, ask:**
1. Does BProgramArgs already provide this?
2. Can p-trigger handle this event?
3. Can p-target + helper methods do this?
4. Is this a lifecycle event?

### Adaptation Reference

| Need | bElement Provides | Don't Use |
|------|-------------------|-----------|
| Query Shadow DOM | `$` with p-target | root.querySelector() |
| Event listening | p-trigger attribute | addEventListener() |
| DOM manipulation | Helper methods | Direct DOM APIs |
| Shadow root | `root` in BProgramArgs | this.shadowRoot |
| Element instance | `host` in BProgramArgs | this |
| ElementInternals | `internals` in BProgramArgs | this.attachInternals() |
| Lifecycle | Callback handlers | Raw Custom Element methods |

### Web API Integration (when not in bElement)

```typescript
// Always cleanup web APIs in onDisconnected
bProgram({ host }) {
  let observer: IntersectionObserver | undefined

  return {
    onConnected() {
      observer = new IntersectionObserver((entries) => {
        // Handle intersection
      })
      observer.observe(host)
    },
    onDisconnected() {
      observer?.disconnect()  // Required cleanup
      observer = undefined
    }
  }
}
```

## Output Location

Save extracted patterns to:
```
/references/[pattern-name].md
```

## Pattern Output Template

```markdown
# [Pattern Name]

## Overview
Brief description of what this pattern does.

## Use Cases
- When to use this pattern
- Common scenarios

## Implementation

### Vanilla JavaScript
// Standard web API usage

### Plaited Adaptation
import { bElement } from 'plaited/ui'

export const Example = bElement({
  tag: 'example-element',
  shadowDom: (
    // Template with p-trigger and p-target
  ),
  bProgram({ $, host }) {
    return {
      onConnected() {
        // Setup if web API needed
      },
      onDisconnected() {
        // Cleanup required for web APIs
      }
    }
  }
})

## Plaited Integration
- Works with Shadow DOM: [yes/no]
- Uses bElement built-ins: [list]
- Requires external web API: [yes/no]
- Cleanup required: [yes/no]

## Browser Compatibility
| Browser | Support |
|---------|---------|
| Chrome | X.X+ |
| Firefox | X.X+ |
| Safari | X.X+ |

## Accessibility
- ARIA considerations
- Keyboard navigation
- Screen reader support

## References
- Source: [Article URL]
- MDN: [MDN link]
```

## Adding New Patterns

When you add a new pattern to the `references/` directory, tell Claude to re-read the skill:
- "Re-read the plaited-web-patterns skill to see the new pattern"
- Claude will use the Read tool to load the updated content

## Related Skills
- plaited-ui-patterns - bElement patterns and styling
- plaited-standards - Code conventions
- typescript-lsp - Type verification for bElement APIs
