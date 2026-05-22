---
name: Fluxwing Component Expander
description: Add interaction states like hover, focus, disabled, active, error to existing uxscii components. Use when working with .uxm files, when user wants to expand, enhance, or add states to .uxm components.
version: 0.0.1
author: Trabian
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Fluxwing Component Expander

Expand existing uxscii components by adding interaction states.

## Data Location Rules

**READ from:**
- `./fluxwing/components/` - User-created components to expand
- `./fluxwing/library/` - User library components to expand
- `{SKILL_ROOT}/docs/` - Documentation for state definitions

**WRITE to:**
- `./fluxwing/components/` - Updated components (overwrite existing)
- `./fluxwing/library/` - Updated library components (overwrite existing)

## Your Task

Expand an existing uxscii component by adding interaction states.

## Workflow

### 1. Locate Component

Ask for the component name if not provided:
- "Which component do you want to expand?"
- Search in `./fluxwing/components/` and `./fluxwing/library/`
- Display current states if component found

### 2. Determine States to Add

**Default behavior (no instructions)**: Add ALL standard states for component type

**Smart defaults by type**:
- **button**: hover, active, disabled
- **input**: focus, error, disabled
- **checkbox/radio**: checked, disabled
- **select**: open, disabled
- **link**: hover, visited, active
- **card**: hover, selected
- **modal**: open, closing
- **alert**: success, warning, error, info
- **badge**: active, inactive
- **navigation**: active, hover
- **toggle**: on, off, disabled
- **slider**: dragging, disabled
- **tab**: selected, hover
- **list**: selected, hover
- **table**: sorted, hover

**User can override**: "Only add hover and focus" or "Add error state only"

### 3. Read Existing Component Files

Read both files:
- `{component-name}.uxm` - Current JSON metadata
- `{component-name}.md` - Current ASCII template

Extract:
- Current states (from behavior.states array)
- Component type (from type field)
- Visual properties (from ascii section)
- Variables (from ascii.variables array)
- Border style from default state (from behavior.states[0].properties.border)

### 4. Generate New States

For each new state to add:

**A. Add state definition to .uxm file**

Insert into the `behavior.states` array. Each state needs:

```json
{
  "name": "hover",
  "properties": {
    "border": "heavy",
    "background": "primary-dark",
    "textColor": "default"
  },
  "triggers": ["mouseenter"]
}
```

**State property patterns by state name**:

- **hover**:
  - border: "heavy"
  - background: slightly darker than default
  - triggers: ["mouseenter"]

- **focus**:
  - border: "double"
  - background: same as default
  - textColor: "primary"
  - triggers: ["focus"]

- **active**:
  - border: "heavy"
  - background: "filled"
  - triggers: ["mousedown"]

- **disabled**:
  - border: "dashed"
  - opacity: 0.5
  - cursor: "not-allowed"

- **error**:
  - border: "heavy"
  - borderColor: "red"
  - textColor: "error"

- **success**:
  - border: "heavy"
  - borderColor: "green"
  - textColor: "success"

- **loading**:
  - opacity: 0.7
  - cursor: "wait"

- **checked** (checkbox/radio):
  - border: "heavy"
  - background: "filled"
  - textColor: "primary"

- **selected**:
  - border: "heavy"
  - background: "highlight"
  - textColor: "primary"

- **open** (modal/select):
  - visible: true
  - triggers: ["click"]

- **visited** (link):
  - textColor: "visited"

**B. Generate ASCII for new state in .md file**

Use appropriate box-drawing characters for each state:

- **hover**: Heavy border `┏━┓┃┗━┛`
- **focus**: Double border `╔═╗║╚═╝`
- **active**: Heavy filled `┏━┓┃┗━┛` with darker interior
- **disabled**: Dashed border `┌┄┄┐┆└┄┄┘`
- **error**: Heavy border with indicator `┏━┓┃┗━┛ ⚠`
- **success**: Heavy border with indicator `┏━┓┃┗━┛ ✓`
- **checked**: Box with checkmark `[✓]` or filled indicator
- **selected**: Heavy border with highlight background
- **loading**: Spinner or progress indicator

**Template for new state section in .md file**:

```markdown
## {State Name} State

\`\`\`
{ASCII art using appropriate border style}
\`\`\`
```

### 5. Update Files

**Write updated files**:
- Overwrite `{component-name}.uxm` with expanded states array
- Append new state sections to `{component-name}.md`

**Preserve**:
- All existing metadata (name, description, author, created, tags, category)
- All existing variables
- All existing states
- All existing props
- Component ID and version

**Update**:
- `metadata.modified` timestamp (set to current ISO 8601 timestamp)
- `behavior.states` array (add new states to end)
- `.md` file (append new state sections before Variables section if it exists, otherwise at end)

**Important**: When updating the .md file, insert new state sections AFTER existing state sections but BEFORE the Variables, Accessibility, and Usage sections.

### 5a. Validate Expanded Component

After updating the files, validate the expanded component to ensure quality:

```bash
uv run {SKILL_ROOT}/../uxscii-component-creator/scripts/quick_validate.py \\
  ./fluxwing/components/{component-name}.uxm \\
  {SKILL_ROOT}/../uxscii-component-creator/schemas/uxm-component.schema.json
```

**Validation checks:**
- ✓ JSON schema compliance
- ✓ All states have valid properties
- ✓ Variables match between .uxm and .md
- ✓ Accessibility requirements met
- ✓ No duplicate states

**If validation fails:**
1. Read the error messages
2. Fix the issues in the .uxm or .md files
3. Re-validate before confirming to user

**Performance**: ~100ms (very fast!)

### 6. Confirm Expansion

Show summary:
```
✓ Expanded: ./fluxwing/components/{component-name}
✓ Added states: hover, active, disabled
✓ Total states: 4 (default, hover, active, disabled)

Preview of hover state:
┏━━━━━━━━━━━━━━━━━━━━┓
┃   {{text}}         ┃
┗━━━━━━━━━━━━━━━━━━━━┛
```

## Resources Available

- **State patterns**: `{SKILL_ROOT}/docs/06-ascii-patterns.md` - Box-drawing characters
- **Component creation**: `{SKILL_ROOT}/docs/03-component-creation.md` - Component structure

## Example Interaction

```
User: Expand submit-button with hover state

Skill: I found `submit-button` in ./fluxwing/components/

Current states: default

I'll add the hover state to make the button interactive.

[Reads submit-button.uxm and submit-button.md]
[Generates hover state]
[Updates both files]

✓ Expanded: ./fluxwing/components/submit-button
✓ Added states: hover
✓ Total states: 2 (default, hover)

Preview of hover state:
┏━━━━━━━━━━━━━━━━━━━━┓
┃   Submit Form      ┃
┗━━━━━━━━━━━━━━━━━━━━┛

Next steps:
- Add more states (active, disabled)
- Use this button in a screen
- View all components
```

## Example with Custom States

```
User: Add focus and error states to email-input

Skill: I found `email-input` in ./fluxwing/components/

Current states: default

I'll add the requested states: focus, error

[Generates only focus and error states]

✓ Expanded: ./fluxwing/components/email-input
✓ Added states: focus, error
✓ Total states: 3 (default, focus, error)

Note: Standard input states also include 'disabled'.
Let me know if you want to add it!
```

## Quality Standards

Ensure expanded components include:
- ✓ Valid JSON schema compliance (no breaking changes)
- ✓ All new states have definitions in .uxm behavior.states array
- ✓ All new states have ASCII sections in .md
- ✓ State properties match component type conventions
- ✓ Consistent box-drawing character usage
- ✓ Updated modification timestamp
- ✓ Preserved existing data (no data loss)
- ✓ No duplicate states (check before adding)

## Important Notes

- **Always preserve existing states** (never remove or modify existing ones)
- **Detect duplicate states** (skip if state already exists in behavior.states array)
- **Validate component after expansion** (ensure valid JSON)
- **Use appropriate border styles per state** (refer to patterns doc)
- **Match visual style of existing default state** (consistent dimensions and layout)
- **Test keyboard navigation** for new interactive states
- **Insert .md sections in correct location** (after states, before Variables section)
- **Update only the modified timestamp** (preserve created timestamp)

## Error Handling

If component not found:
```
✗ Component '{component-name}' not found.

Searched in:
- ./fluxwing/components/
- ./fluxwing/library/

Available components:
[List first 10 components found]

Please check the component name and try again.
```

If state already exists:
```
⚠ State 'hover' already exists in {component-name}.
Skipping duplicate state.

Current states: default, hover
Adding: active, disabled
```

If file write fails:
```
✗ Failed to update {component-name}.

Error: [specific error message]

The component files remain unchanged.
Please check file permissions and try again.
```

You're helping users create fully interactive uxscii components!
