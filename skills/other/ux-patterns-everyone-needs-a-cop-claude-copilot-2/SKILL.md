---
skill_name: ux-patterns
skill_category: design
description: UX patterns for task flows, wireframes, accessibility, and user interactions
allowed_tools: [Read, Edit, Write, Glob, Grep]
token_estimate: 1400
version: 1.0
last_updated: 2026-01-13
owner: Claude Copilot
status: active
tags: [ux, interaction, wireframe, task-flow, accessibility, pattern, anti-pattern]
related_skills: [design-patterns]
trigger_files: ["**/*.wireframe", "**/ux/**", "**/flows/**", "**/journeys/**"]
trigger_keywords: [task-flow, wireframe, user-journey, interaction-design, accessibility, WCAG, error-state, empty-state, service-blueprint]
quality_keywords: [anti-pattern, pattern, validation, best-practice, accessibility]
---

# UX Patterns

Patterns for designing task flows, service blueprints, wireframes, and user interactions with comprehensive state coverage.

## Purpose

Provides patterns for:
- Task flows with all user paths
- Service blueprints (frontstage/backstage)
- Wireframe specifications
- Error and empty state design
- Accessibility from the start

---

## Core Patterns

### Pattern 1: Task Flow Structure

**When to use:** Defining any user interaction flow.

**Implementation:**
```markdown
## Task Flow: [Name]

**User Goal:** What they want to accomplish
**Entry Point:** Where they start
**Success:** How they know they succeeded

### Primary Path
1. [Action] -> [Response] -> [State]
2. [Action] -> [Response] -> [State]
3. [Action] -> [Response] -> [Success]

### Alternative Paths
- [Condition] -> [Alternative flow]

### Error States
| Error | Message | Recovery |
|-------|---------|----------|
| [Error] | [What happened + How to fix] | [User action] |
```

**Benefits:**
- Clear success criteria
- All paths documented
- Error recovery built-in

### Pattern 2: Service Blueprint

**When to use:** Mapping end-to-end service experiences.

**Implementation:**
```markdown
## Service Blueprint: [Name]

### Journey Stages
[Awareness] -> [Consideration] -> [Purchase] -> [Use] -> [Support]

### Customer Actions (per stage)
| Stage | Actions |
|-------|---------|
| [Stage] | [What customer does] |

### Frontstage (Visible)
| [Touchpoint] | [Touchpoint] | [Touchpoint] |

### Line of Visibility
---

### Backstage (Invisible)
| [Process] | [Process] | [Process] |

### Support Processes
| [System] | [System] | [System] |

### Pain Points
- **[Stage]:** [Issue] - [Evidence]

### Opportunities
- **[Stage]:** [Improvement] - [Impact]
```

### Pattern 3: State Coverage Matrix

**When to use:** Ensuring all UI states are designed.

**Implementation:**
| State | When | Content | Action |
|-------|------|---------|--------|
| Default | Normal use | Full content | Primary action |
| Loading | Fetching data | Skeleton/spinner | Disabled actions |
| Empty | No data yet | Why empty + CTA | Create/Add action |
| Error | Operation failed | What + How to fix | Retry/Fix action |
| Success | Action completed | Confirmation | Next action |
| Partial | Some data | Available content | Load more |

---

## Anti-Patterns

### Anti-Pattern 1: Assumption-Based Design

| Aspect | Description |
|--------|-------------|
| **WHY** | Leads to unusable products, wasted effort, user frustration |
| **DETECTION** | No user research cited, no evidence for design decisions |
| **FIX** | Ground every design decision in user research or data |

**Bad Example:**
```markdown
Users will want a dashboard on login.
```

**Good Example:**
```markdown
Research shows 78% of users check status immediately after login.
Evidence: User interviews (n=12), analytics showing /dashboard as top page.
```

### Anti-Pattern 2: Missing States

| Aspect | Description |
|--------|-------------|
| **WHY** | Users encounter undesigned situations, broken experience |
| **DETECTION** | Only happy path designed, no empty/error/loading states |
| **FIX** | Design ALL states: default, loading, empty, error, success, partial |

### Anti-Pattern 3: Color as Sole Indicator

| Aspect | Description |
|--------|-------------|
| **WHY** | Excludes colorblind users (8% of men), fails WCAG |
| **DETECTION** | Status shown only via red/green/yellow color |
| **FIX** | Always add icons, text, or patterns alongside color |

**Bad Example:**
```
[Red dot] Failed    [Green dot] Success
```

**Good Example:**
```
[X icon] Failed    [Checkmark icon] Success
```

### Anti-Pattern 4: Vague Error Messages

| Aspect | Description |
|--------|-------------|
| **WHY** | Users can't recover, support burden increases |
| **DETECTION** | "Error", "Invalid input", "Something went wrong" |
| **FIX** | Error format: [What happened] + [How to fix it] |

**Bad Example:**
```
Invalid input
```

**Good Example:**
```
Email format looks wrong. Try: name@example.com
```

---

## Accessibility Requirements

### Keyboard Navigation
- All interactive elements reachable via Tab
- Logical tab order (left-right, top-bottom)
- Enter/Space activate buttons
- Escape closes modals
- Arrow keys navigate within components

### Focus Management
- Focus visible at all times (2px outline minimum)
- Focus moves logically (not trapped)
- Focus returns to trigger after modal closes
- Skip links for long navigation

### Screen Reader Support
- Semantic HTML (button, nav, main, article)
- ARIA labels for icons and images
- Live regions for dynamic content (role="status")
- Announcements for state changes

---

## Validation Checklist

### Task Flows
- [ ] User goal clearly defined
- [ ] Entry point and success criteria specified
- [ ] All alternative paths documented
- [ ] Error states with recovery actions

### States
- [ ] Default state designed
- [ ] Loading state with feedback
- [ ] Empty state with explanation + CTA
- [ ] Error state with [What happened] + [How to fix]
- [ ] Success state with confirmation

### Accessibility
- [ ] Keyboard navigation tested
- [ ] Focus order is logical
- [ ] Screen reader announcements planned
- [ ] No color-only indicators

---

## Output Templates

### Task Flow
```markdown
## Task Flow: [Task Name]

**User Goal:** [What user wants]
**Entry Point:** [Where they start]
**Success:** [How they know done]

### Primary Path
1. [Action] -> [Response] -> [State]

### Error States
| Error | Message | Recovery |
|-------|---------|----------|
| [Error] | [What + Fix] | [Action] |
```

### Wireframe
```markdown
## Wireframe: [Screen Name]

### Purpose
[What this screen accomplishes]

### Components
| Component | Behavior | States |
|-----------|----------|--------|
| [Name] | [Function] | Default, Hover, Focus, Error |

### Accessibility
- Tab order: [Sequence]
- Screen reader: [Announcements]
- Focus: [Visible states]
```

### Empty State
```markdown
## Empty State: [Context]

**Headline:** [What this is]
**Body:** [Why it's empty]
**CTA:** [Primary action button]
**Secondary:** [Alternative action or help]
```
