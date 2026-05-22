---
name: Documentation Patterns
description: Technical writing frameworks for clear, maintainable documentation
version: 1.0.0
license: MIT
tier: community
---

# Documentation Patterns

> **Documentation that people actually read and use**

This skill provides frameworks for writing technical documentation that serves its readers effectively.

## Core Principles

### 1. Documentation Is a Product
Treat docs like software: design, iterate, test, improve.

### 2. Different Docs for Different Goals
Tutorials, references, and explanations serve different purposes. Don't mix them.

### 3. Write for Scanning
Most readers don't read linearly. Structure for quick answers.

## The Documentation System (Diataxis)

Four distinct documentation types, each with a specific purpose:

```
                        PRACTICAL                    THEORETICAL
                    (Learning-oriented)          (Understanding-oriented)
                            │                            │
   ┌────────────────────────┼────────────────────────────┼────────────────────┐
   │                        │                            │                    │
   │     TUTORIALS          │      EXPLANATION           │    ACQUISITION     │
   │  (Learning by doing)   │  (Understanding context)   │    (Studying)      │
   │                        │                            │                    │
   │                        │                            │                    │
   ├────────────────────────┼────────────────────────────┼────────────────────┤
   │                        │                            │                    │
   │     HOW-TO GUIDES      │      REFERENCE             │    APPLICATION     │
   │  (Accomplishing tasks) │  (Looking up information)  │    (Working)       │
   │                        │                            │                    │
   └────────────────────────┴────────────────────────────┴────────────────────┘
```

### 1. Tutorials (Learning)

**Purpose:** Teach a newcomer how to get started
**Reader:** New, wants to learn
**Form:** Lessons that lead through steps

```markdown
# Tutorial: Create Your First Component

In this tutorial, you'll build a simple button component
from scratch. By the end, you'll understand the basics
of our component system.

## What You'll Learn
- How to create a component file
- How to use our styling system
- How to add interactivity

## Prerequisites
- Node.js installed
- Basic React knowledge

## Step 1: Set Up Your File
Create a new file called `Button.tsx` in the components folder:
[exact code to copy]

## Step 2: Add the Basic Structure
[exact code with explanation]

## Step 3: Style Your Button
[exact code with explanation]

## What's Next?
Now that you've created a basic button, try:
- Adding different variants
- Making it accessible
```

**Tutorial Checklist:**
- [ ] Has a clear learning outcome
- [ ] Every step produces visible results
- [ ] Uses concrete, realistic examples
- [ ] Can be completed in one sitting
- [ ] Doesn't explain everything (focused)

### 2. How-To Guides (Goals)

**Purpose:** Help accomplish a specific task
**Reader:** Knows what they want to do
**Form:** Steps to achieve a goal

```markdown
# How to Add Dark Mode Support

This guide shows you how to add dark mode to your application.

## Prerequisites
- Existing application with our design system
- Tailwind CSS configured

## Steps

### 1. Configure Theme Variables
Add these CSS variables to your globals.css:
[code]

### 2. Add Theme Toggle
Create a theme context:
[code]

### 3. Update Components
Ensure components use theme-aware classes:
[code]

### 4. Persist User Preference
Store the theme choice:
[code]

## Troubleshooting

**Theme doesn't persist on refresh**
Check that localStorage is accessible...

**Flash of wrong theme on load**
Add a script to the head...
```

**How-To Checklist:**
- [ ] Title states the goal clearly
- [ ] Prerequisites listed upfront
- [ ] Steps are actionable
- [ ] Troubleshooting section included
- [ ] Doesn't teach concepts (just does)

### 3. Reference (Information)

**Purpose:** Provide accurate, complete technical details
**Reader:** Knows what they're looking for
**Form:** Structured, consistent entries

```markdown
# Button Component API

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'ghost'` | `'primary'` | Visual style |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | Button size |
| `disabled` | `boolean` | `false` | Disables interaction |
| `isLoading` | `boolean` | `false` | Shows loading state |
| `onClick` | `() => void` | - | Click handler |

## Examples

### Basic Usage
```jsx
<Button>Click me</Button>
```

### With Variant
```jsx
<Button variant="secondary">Cancel</Button>
```

### Loading State
```jsx
<Button isLoading>Saving...</Button>
```

## Accessibility
- Uses `<button>` element for proper semantics
- Supports keyboard activation (Enter, Space)
- Has visible focus state
- Announces loading state to screen readers
```

**Reference Checklist:**
- [ ] Complete coverage of all options
- [ ] Consistent format throughout
- [ ] Technical accuracy verified
- [ ] Examples for each concept
- [ ] Easy to scan/search

### 4. Explanation (Understanding)

**Purpose:** Help understand concepts and context
**Reader:** Wants to deepen understanding
**Form:** Discursive, contextual prose

```markdown
# Understanding Our Component Architecture

## Why Components?

Our design system is built on the principle of composition.
Rather than creating complex, monolithic UI pieces, we build
small, focused components that combine to create any interface.

This approach has several benefits:

**Maintainability**: Changes to one component don't affect others...

**Testability**: Small components are easy to test in isolation...

**Consistency**: Shared components ensure visual consistency...

## The Component Hierarchy

Components exist at different levels of abstraction:

### Primitives
The building blocks: Button, Input, Text...
These have no business logic, only UI concerns.

### Patterns
Compositions of primitives: FormField, Card, Modal...
These solve common UI patterns.

### Features
Compositions with business logic: LoginForm, UserCard...
These connect UI to application state.

## Design Decisions

### Why We Chose Radix UI

When evaluating component libraries, we considered...
We chose Radix because...

### Our Styling Approach

We use Tailwind CSS with CSS variables because...
The trade-offs of this approach include...
```

**Explanation Checklist:**
- [ ] Provides context and background
- [ ] Explains "why" not just "what"
- [ ] Connects to bigger picture
- [ ] Uses analogies when helpful
- [ ] Doesn't include step-by-step instructions

## README Structure

### Project README Template

```markdown
# Project Name

> One-line description of what this project does

Brief paragraph expanding on the description. What problem
does it solve? Who is it for?

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Quick Start

```bash
# Install
npm install project-name

# Configure
cp .env.example .env

# Run
npm run dev
```

## Documentation

- [Getting Started Guide](./docs/getting-started.md)
- [API Reference](./docs/api.md)
- [Examples](./examples/)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
```

### Package README Template

```markdown
# package-name

> Brief description

## Installation

```bash
npm install package-name
```

## Usage

```javascript
import { thing } from 'package-name';

// Basic example
thing.do();
```

## API

### `thing.do(options)`

Does the thing.

**Parameters:**
- `options.foo` (string): The foo
- `options.bar` (number, optional): The bar (default: 42)

**Returns:** `Promise<Result>`

**Example:**
```javascript
const result = await thing.do({ foo: 'value' });
```

## License

MIT
```

## Code Documentation

### Function Documentation (JSDoc)

```typescript
/**
 * Calculates the total price including tax.
 *
 * @param items - Array of items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.1 for 10%)
 * @returns Total price with tax applied
 *
 * @example
 * ```ts
 * const total = calculateTotal(
 *   [{ price: 100, quantity: 2 }],
 *   0.1
 * );
 * // Returns: 220
 * ```
 *
 * @throws {Error} If taxRate is negative
 */
function calculateTotal(
  items: Array<{ price: number; quantity: number }>,
  taxRate: number
): number {
  if (taxRate < 0) {
    throw new Error('Tax rate cannot be negative');
  }
  const subtotal = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  return subtotal * (1 + taxRate);
}
```

### Component Documentation

```typescript
/**
 * A customizable button component with multiple variants.
 *
 * @example
 * ```tsx
 * // Primary button
 * <Button onClick={handleClick}>Submit</Button>
 *
 * // Secondary button with icon
 * <Button variant="secondary" icon={<PlusIcon />}>
 *   Add Item
 * </Button>
 * ```
 */
interface ButtonProps {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Size of the button */
  size?: 'sm' | 'md' | 'lg';
  /** Whether the button is disabled */
  disabled?: boolean;
  /** Icon to display before the label */
  icon?: React.ReactNode;
  /** Click handler */
  onClick?: () => void;
  /** Button contents */
  children: React.ReactNode;
}
```

### When to Comment (and When Not To)

```yaml
Write Comments For:
  - Why decisions were made
  - Non-obvious edge cases
  - Complex algorithms
  - Workarounds for bugs
  - Public API documentation

Don't Comment:
  - What the code does (code should be clear)
  - Every line
  - Obvious implementations
  - TODOs without tickets

Example Bad Comment:
  // Increment counter by 1
  counter += 1;

Example Good Comment:
  // Using >= instead of > to handle floating point rounding errors
  // See issue #1234 for details
  if (value >= threshold) {
```

## Writing Guidelines

### Voice and Tone

```yaml
Technical Writing Voice:

  Be Direct:
    Bad: "It is recommended that you should..."
    Good: "We recommend..." or just state the thing

  Be Specific:
    Bad: "This might cause issues"
    Good: "This causes a memory leak in Chrome"

  Use Active Voice:
    Bad: "The button is clicked by the user"
    Good: "The user clicks the button"

  Address the Reader:
    Bad: "One can configure settings in..."
    Good: "You can configure settings in..."
```

### Formatting Best Practices

```yaml
Headings:
  - Use sentence case (Capitalize only first word)
  - Keep short and scannable
  - Use hierarchy consistently

Lists:
  - Use bullets for unordered items
  - Use numbers for sequential steps
  - Keep items parallel in structure

Code:
  - Use inline code for short references: `variable`
  - Use code blocks for examples
  - Always specify language for syntax highlighting

Links:
  - Use descriptive text, not "click here"
  - Link to specific sections when possible
```

### Inclusive Language

```yaml
Avoid:
  - "Simply" / "Just" / "Easy" (dismissive)
  - "Obviously" / "Clearly" (assumes knowledge)
  - Gendered pronouns when unnecessary
  - Jargon without explanation

Use:
  - "First" instead of "First off"
  - Specific technical terms (defined)
  - "They" for generic singular
```

## Documentation Structure

### Information Architecture

```yaml
Organization Principles:

  By User Journey:
    - Getting started → Core concepts → Advanced

  By Task:
    - Authentication → Authorization → User management

  By Feature:
    - Components → Hooks → Utilities

  Navigation:
    - Clear hierarchy
    - Searchable
    - Cross-linked
```

### Page Structure

```markdown
# Page Title

Brief intro paragraph explaining what this page covers and
who it's for.

## Section 1

Content with examples...

### Subsection 1.1

More specific content...

## Section 2

Content...

## Related

- [Related Page 1](./related1.md)
- [Related Page 2](./related2.md)
```

## Maintenance

### Keeping Docs Fresh

```yaml
Documentation Debt Signals:
  - Screenshots that don't match UI
  - Code examples that don't compile
  - Broken links
  - Outdated version numbers
  - Missing recent features

Prevention:
  - Doc review in PR checklist
  - Automated link checking
  - Version docs with code
  - Regular doc audits (quarterly)
```

### Doc Review Checklist

```markdown
## Documentation Review

### Accuracy
- [ ] Code examples work
- [ ] Technical details are correct
- [ ] Screenshots are current

### Completeness
- [ ] All features documented
- [ ] Edge cases mentioned
- [ ] Prerequisites listed

### Clarity
- [ ] Language is clear
- [ ] Structure aids scanning
- [ ] Examples are helpful

### Maintenance
- [ ] Links work
- [ ] Version numbers correct
- [ ] No outdated content
```

---

*"The best documentation is so good that people don't notice it. They just find what they need and move on."*
