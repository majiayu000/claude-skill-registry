---
name: ui-design-skill
description: Expert guidance on UI/UX design for console and web interfaces. Use when designing, implementing, or reviewing: (1) Console UIs with Rich library for terminal apps, (2) Web UIs with Tailwind CSS, (3) Responsive layouts and mobile-first design, (4) Accessible interfaces following WCAG guidelines, (5) Design systems and component consistency, (6) User-centered design decisions. Invoke when user asks about colors, layouts, typography, user flows, or interface patterns.
---

# UI Design Skill

Expert guidance for creating beautiful, accessible, and user-friendly interfaces.

## Design Decision Framework

```
User Need → Information Architecture → Visual Hierarchy → Interaction Design → Accessibility Check
```

### When to Use Which Technology

| Context | Technology | Reference |
|---------|------------|-----------|
| Phase I Console App | Rich library | [rich-console-ui.md](references/rich-console-ui.md) |
| Phase II Web App | Tailwind CSS | [tailwind-patterns.md](references/tailwind-patterns.md) |
| Mobile/Responsive | Media queries | [responsive-design.md](references/responsive-design.md) |

## Core Principles (Nielsen's Heuristics)

1. **Visibility of system status** - Always show what's happening
2. **Match real world** - Use familiar language and concepts
3. **User control** - Provide undo, cancel, clear exits
4. **Consistency** - Same actions = same results
5. **Error prevention** - Prevent problems before they occur
6. **Recognition over recall** - Show options, don't require memory
7. **Flexibility** - Support both novice and expert users
8. **Aesthetic minimalism** - Remove unnecessary information
9. **Error recovery** - Clear error messages with solutions
10. **Help & documentation** - Easy to search, task-focused

## Visual Hierarchy Quick Reference

### Typography Scale
```
Heading 1:  2.25rem (36px)  - Page titles
Heading 2:  1.875rem (30px) - Section headers
Heading 3:  1.5rem (24px)   - Subsections
Body:       1rem (16px)     - Main content
Small:      0.875rem (14px) - Secondary info
Caption:    0.75rem (12px)  - Labels, hints
```

### Color Usage
```
Primary:    Brand identity, main CTAs
Secondary:  Supporting actions
Success:    Confirmations, completions (green)
Warning:    Caution states (yellow/amber)
Error:      Failures, destructive actions (red)
Neutral:    Text, backgrounds, borders
```

### Spacing Scale (8px base)
```
xs:  4px   (0.25rem)
sm:  8px   (0.5rem)
md:  16px  (1rem)
lg:  24px  (1.5rem)
xl:  32px  (2rem)
2xl: 48px  (3rem)
```

## Console UI Quick Start (Rich)

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

# Status messages
console.print("[green]✓[/green] Task completed")
console.print("[red]✗[/red] Error occurred")
console.print("[yellow]![/yellow] Warning message")

# Data display
table = Table(title="Tasks")
table.add_column("ID", style="dim")
table.add_column("Title", style="bold")
table.add_column("Status")
table.add_row("1", "Buy groceries", "[green]Done[/green]")
console.print(table)

# User input
name = Prompt.ask("Enter task name")
confirm = Confirm.ask("Delete this task?")
```

## Web UI Quick Start (Tailwind)

```html
<!-- Card Component -->
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 class="text-lg font-semibold text-gray-900">Task Title</h3>
  <p class="text-gray-600 mt-2">Task description here</p>
  <div class="mt-4 flex gap-2">
    <button class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
      Complete
    </button>
    <button class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
      Edit
    </button>
  </div>
</div>
```

## Accessibility Checklist

- [ ] Color contrast ratio ≥ 4.5:1 for text
- [ ] All interactive elements keyboard accessible
- [ ] Focus states visible and clear
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Error messages announced to screen readers
- [ ] Heading hierarchy is logical (h1 → h2 → h3)
- [ ] Touch targets ≥ 44x44 pixels

## References

- **[Design Principles](references/design-principles.md)** - User-centered design, mental models, feedback
- **[Rich Console UI](references/rich-console-ui.md)** - Tables, panels, progress bars, prompts
- **[Tailwind Patterns](references/tailwind-patterns.md)** - Components, utilities, dark mode
- **[Responsive Design](references/responsive-design.md)** - Breakpoints, mobile-first, layouts
- **[Accessibility (WCAG)](references/accessibility-wcag.md)** - ARIA, keyboard nav, screen readers
- **[Design Systems](references/design-systems.md)** - Tokens, components, documentation
