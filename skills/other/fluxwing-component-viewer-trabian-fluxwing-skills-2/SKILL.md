---
name: Fluxwing Component Viewer
description: View detailed information about a specific uxscii component including metadata, states, props, and ASCII preview. Use when working with .uxm files, when user wants to see, view, inspect, or get details about a .uxm component.
version: 0.0.1
author: Trabian
allowed-tools: Read, Glob, Grep
---

# Fluxwing Component Viewer

View detailed information about a specific uxscii component from any source.

## Data Location Rules

**READ from (bundled templates - reference only):**
- `{SKILL_ROOT}/../uxscii-component-creator/templates/` - 11 component templates
- `{SKILL_ROOT}/../uxscii-screen-scaffolder/templates/` - 2 screen examples (if available)

**READ from (project workspace):**
- `./fluxwing/components/` - Your created components
- `./fluxwing/library/` - Customized template copies
- `./fluxwing/screens/` - Your created screens

**NEVER write - this is a read-only viewer!**

## Your Task

Display comprehensive details about a single uxscii component, including metadata, ASCII template preview, and context-appropriate actions.

## Component Lookup Process

### 1. Parse Component Name
- Extract component name from user request
- If no name provided: Ask "Which component would you like to view?"
- Normalize name to lowercase with hyphens

### 2. Search Priority Order (Stop at First Match)
Search these locations in order and stop at the first match:

1. **Project Components**: `./fluxwing/components/[name].uxm`
   - User/agent-created custom components
   - Fully editable
   - Tag as: "Your Component"

2. **Project Library**: `./fluxwing/library/[name].uxm`
   - Customized copies of bundled templates
   - Fully editable
   - Tag as: "Your Library"

3. **Bundled Templates**: `{SKILL_ROOT}/../uxscii-component-creator/templates/[name].uxm`
   - Read-only reference templates
   - Must be copied to edit
   - Tag as: "Bundled Template"

**Important**: Stop searching after first match. If found in bundled templates, check if it also exists in user's project and add a note: "💡 You also have a customized version in ./fluxwing/library/"

### 3. Read Component Files
For the matched component, read both files:
- `[name].uxm` - JSON metadata
- `[name].md` - ASCII template

## Display Format

### Concise View (Default)

Present component information in a clean, scannable format:

```
📄 PRIMARY-BUTTON
─────────────────────────────────────────────────────
📦 Source: Bundled Template
📍 Location: Component Creator Templates
⏱️  Modified: 2024-10-11 10:30:00
🔖 Version: 1.0.0

Description:
Standard clickable button with hover, focus, and disabled states

Component Details:
• Type: button
• Props: text (string), variant (string), disabled (boolean)
• States: default, hover, focus, disabled
• Accessibility: ✓ Role (button), ✓ Focusable, ✓ Keyboard (Space, Enter)

ASCII Template Preview (first 20 lines):

Default State:
▓▓▓▓▓▓▓▓▓▓▓▓
▓ {{text}} ▓
▓▓▓▓▓▓▓▓▓▓▓▓

Hover State:
░▓▓▓▓▓▓▓▓▓▓▓░
░▓ {{text}} ▓░
░▓▓▓▓▓▓▓▓▓▓░

Disabled State:
┌ ─ ─ ─ ─ ─┐
│ {{text}} │
└ ─ ─ ─ ─ ─┘

[... 1 more state]

Template has 4 states total. View full template?
─────────────────────────────────────────────────────
```

### Format Guidelines

**Header Section:**
- Component name in CAPS
- Emoji indicators:
  - 📦 = Bundled Template
  - ✏️ = Your Library
  - 🎨 = Your Component
- Full file path for clarity
- Last modified timestamp (if available)
- Version from metadata

**Description:**
- Use the `metadata.description` field from .uxm file
- Keep it concise (1-2 lines)

**Component Details:**
- **Type**: Direct from .uxm `type` field
- **Props**: List prop names with types in parentheses
  - Format: `propName (type)`
  - Example: `text (string), disabled (boolean)`
- **States**: Comma-separated list of state names
- **Accessibility**: Show checkmarks for present features
  - Role, Focusable, Keyboard shortcuts, ARIA labels

**ASCII Template Preview:**
- Show first 20 lines by default
- If template has multiple states, show state labels
- If template exceeds 20 lines, add: `[... N more states/lines]`
- Preserve exact spacing and box-drawing characters
- Show variables as `{{variableName}}`

### Truncation Logic

If `.md` template exceeds 20 lines:
1. Count total states/sections in template
2. Show first 2-3 states completely
3. Add summary line: `[... N more states]`
4. Offer: "View full template?" as interactive option

## Interactive Options

After displaying the component, offer context-appropriate actions:

### For Bundled Templates (read-only)

```
What would you like to do?

1️⃣ Copy to project library (makes it editable)
2️⃣ View full template file (all states)
3️⃣ View full metadata (complete .uxm)
4️⃣ Browse all components
```

**Action Details:**
- **Copy**: Copy both .uxm and .md to `./fluxwing/library/`
- **View full template**: Display complete .md file (no truncation)
- **View full metadata**: Display complete .uxm JSON
- **Browse**: Return to library browser

### For Project Files (./fluxwing/library/ or ./fluxwing/components/)

```
What would you like to do?

1️⃣ Edit component (modify .uxm and .md)
2️⃣ View full template file (all states)
3️⃣ View full metadata (complete .uxm)
4️⃣ Delete component (manual: remove files from filesystem)
5️⃣ Browse all components
```

**Action Details:**
- **Edit**: Open both .uxm and .md for editing
- **Delete**: Don't automatically delete - instruct user:
  ```
  To delete this component, remove these files from your filesystem:
    • ./fluxwing/components/[name].uxm
    • ./fluxwing/components/[name].md
  ```

## Error Handling

### No Component Name Provided

```
Which component would you like to view?

Example:
  "Show me primary-button"
  "View details for user-card"

View all available components: Ask me to "show me all components"
```

### Component Not Found

```
✗ Component '[name]' not found.

Searched in:
- ./fluxwing/components/
- ./fluxwing/library/
- Bundled templates

Available components:
[List first 10 components found]

Did you mean one of these?
- primary-button
- submit-button
- user-card
```

**Fuzzy search**: If component name is close to an existing component, suggest it:
```
✗ Component 'primry-button' not found.

Did you mean 'primary-button'?
```

### File Read Errors

```
✗ Found component but couldn't read files.

Location: ./fluxwing/components/[name].uxm
Error: [specific error message]

Please check file permissions and try again.
```

## Example Interactions

### Example 1: View Bundled Template

```
User: Show me the primary-button

Skill: 📄 PRIMARY-BUTTON
─────────────────────────────────────────────────────
📦 Source: Bundled Template
📍 Location: Component Creator Templates

Description:
Standard clickable button with hover, focus, and disabled states

Component Details:
• Type: button
• Props: text (string), variant (string), disabled (boolean)
• States: default, hover, focus, disabled
• Accessibility: ✓ Full support

[ASCII preview shown...]

What would you like to do?
1️⃣ Copy to project library
2️⃣ View full template
3️⃣ View metadata
4️⃣ Browse all components
```

### Example 2: View User Component

```
User: What's in my submit-button component?

Skill: 📄 SUBMIT-BUTTON
─────────────────────────────────────────────────────
🎨 Source: Your Component
📍 Location: ./fluxwing/components/submit-button.uxm
⏱️  Modified: 2024-10-15 14:23:00

Description:
Custom submit button for forms

Component Details:
• Type: button
• Props: text (string)
• States: default
• Accessibility: ✓ Basic support

[ASCII preview shown...]

💡 Tip: Add more states with "expand submit-button with hover and disabled"
```

## Resources

- **Core Concepts**: See `{SKILL_ROOT}/docs/02-core-concepts.md` for component fundamentals

You're helping users understand their uxscii components in detail!
