---
name: Fluxwing Screenshot Importer
description: Import UI screenshots and generate uxscii components automatically using vision analysis. Use when user wants to import, convert, or generate .uxm components from screenshots or images.
version: 0.0.1
author: Trabian
allowed-tools: Read, Write, Task, TodoWrite, Glob
---

# Fluxwing Screenshot Importer

Import UI screenshots and convert them to the **uxscii standard** by orchestrating specialized vision agents.

## Data Location Rules

**READ from (bundled templates - reference only):**
- `{SKILL_ROOT}/../uxscii-component-creator/templates/` - 11 component templates (for reference)
- `{SKILL_ROOT}/docs/` - Screenshot processing documentation

**WRITE to (project workspace):**
- `./fluxwing/components/` - Extracted components (.uxm + .md)
- `./fluxwing/screens/` - Screen composition (.uxm + .md + .rendered.md)

**NEVER write to skill directories - they are read-only!**

## Your Task

Import a screenshot of a UI design and automatically generate uxscii components and screens by **orchestrating specialized agents**:

1. **Vision Coordinator Agent** - Spawns 3 parallel vision agents (layout + components + properties)
2. **Component Generator Agents** - Generate component files in parallel (atomic + composite)
3. **Screen Scaffolder Skill** - Delegates to fluxwing-screen-scaffolder for screen composition

**⚠️ ORCHESTRATION RULES:**

**YOU CAN (as orchestrator):**
- ✅ Spawn vision analysis agents
- ✅ Spawn component generator agents
- ✅ Invoke fluxwing-screen-scaffolder skill
- ✅ Read screenshots
- ✅ Validate vision data

**YOU CANNOT (worker mode - forbidden):**
- ⚠️ Create screen files yourself using Write/Edit tools
- ⚠️ Generate .uxm, .md, or .rendered.md files for screens
- ⚠️ "Help" the scaffolder by pre-creating screen files
- ⚠️ Use TodoWrite to work through screen creation tasks yourself

**For screen composition:** ALWAYS delegate to fluxwing-screen-scaffolder skill. It will spawn composer agents that create all screen files (.uxm, .md, .rendered.md).

## Workflow

### Phase 1: Get Screenshot Path

Ask the user for the screenshot path if not provided:
- "Which screenshot would you like to import?"
- Validate file exists and is a supported format (PNG, JPG, JPEG, WebP, GIF)

```typescript
// Example
const screenshotPath = "/path/to/screenshot.png";
```

### Phase 2: Spawn Vision Coordinator Agent

**CRITICAL**: Spawn the `screenshot-vision-coordinator` agent to orchestrate parallel vision analysis.

This agent will:
- Spawn 3 vision agents in parallel (layout discovery + component detection + visual properties)
- Wait for all agents to complete
- Merge results into unified component data structure
- Return JSON with screen metadata, components array, and composition

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Analyze screenshot with vision analysis",
  prompt: `You are a UI screenshot analyzer extracting component structure for uxscii.

Screenshot path: ${screenshotPath}

Your task:
1. Read the screenshot image file
2. Analyze the UI layout structure (vertical, horizontal, grid, sidebar+main)
3. Detect all UI components (buttons, inputs, navigation, cards, etc.)
4. Extract visual properties (colors, spacing, borders, typography)
5. Identify component hierarchy (atomic vs composite)
6. Merge all findings into a unified data structure
7. Return valid JSON output

CRITICAL detection requirements:
- Do NOT miss navigation elements (check all edges - top, left, right, bottom)
- Do NOT miss small elements (icons, badges, close buttons, status indicators)
- Identify composite components (forms, cards with multiple elements)
- Note spatial relationships between components

Expected output format (valid JSON only, no markdown):
{
  "success": true,
  "screen": {
    "id": "screen-name",
    "type": "dashboard|login|profile|settings",
    "name": "Screen Name",
    "description": "What this screen does",
    "layout": "vertical|horizontal|grid|sidebar-main"
  },
  "components": [
    {
      "id": "component-id",
      "type": "button|input|navigation|etc",
      "name": "Component Name",
      "description": "What it does",
      "visualProperties": {...},
      "isComposite": false
    }
  ],
  "composition": {
    "atomicComponents": ["id1", "id2"],
    "compositeComponents": ["id3"],
    "screenComponents": ["screen-id"]
  }
}

Use your vision capabilities to analyze the screenshot carefully.`
})
```

**Wait for the vision coordinator to complete and return results.**

### Phase 3: Validate Vision Data

Check the returned data structure:

```typescript
const visionData = visionCoordinatorResult;

// Required fields
if (!visionData.success) {
  throw new Error(`Vision analysis failed: ${visionData.error}`);
}

if (!visionData.components || visionData.components.length === 0) {
  throw new Error("No components detected in screenshot");
}

// Navigation check (CRITICAL)
const hasNavigation = visionData.components.some(c =>
  c.type === 'navigation' || c.id.includes('nav') || c.id.includes('header')
);

if (visionData.screen.type === 'dashboard' && !hasNavigation) {
  console.warn("⚠️ Dashboard detected but no navigation found - verify all nav elements were detected");
}
```

### Phase 4: Spawn Component Generator Agents (Parallel)

**CRITICAL**: YOU MUST spawn ALL component generator agents in a SINGLE message with multiple Task tool calls. This is the ONLY way to achieve true parallel execution.

**DO THIS**: Send ONE message containing ALL Task calls for all components
**DON'T DO THIS**: Send separate messages for each component (this runs them sequentially)

For each atomic component, create a Task call in the SAME message:

```
Task({
  subagent_type: "general-purpose",
  description: "Generate email-input component",
  prompt: "You are a uxscii component generator. Generate component files from vision data.

Component data: {id: 'email-input', type: 'input', visualProperties: {...}}

Your task:
1. Load schema from {SKILL_ROOT}/../uxscii-component-creator/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/screenshot-import-helpers.md
3. Generate .uxm file (valid JSON with default state only)
4. Generate .md file (ASCII template matching visual properties)
5. Save to ./fluxwing/components/
6. Return success with file paths

Follow uxscii standard strictly."
})

Task({
  subagent_type: "general-purpose",
  description: "Generate password-input component",
  prompt: "You are a uxscii component generator. Generate component files from vision data.

Component data: {id: 'password-input', type: 'input', visualProperties: {...}}

Your task:
1. Load schema from {SKILL_ROOT}/../uxscii-component-creator/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/screenshot-import-helpers.md
3. Generate .uxm file (valid JSON with default state only)
4. Generate .md file (ASCII template matching visual properties)
5. Save to ./fluxwing/components/
6. Return success with file paths

Follow uxscii standard strictly."
})

Task({
  subagent_type: "general-purpose",
  description: "Generate submit-button component",
  prompt: "You are a uxscii component generator. Generate component files from vision data.

Component data: {id: 'submit-button', type: 'button', visualProperties: {...}}

Your task:
1. Load schema from {SKILL_ROOT}/../uxscii-component-creator/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/screenshot-import-helpers.md
3. Generate .uxm file (valid JSON with default state only)
4. Generate .md file (ASCII template matching visual properties)
5. Save to ./fluxwing/components/
6. Return success with file paths

Follow uxscii standard strictly."
})

... repeat for ALL atomic components in the SAME message ...

... then for composite components in the SAME message:

Task({
  subagent_type: "general-purpose",
  description: "Generate login-form composite",
  prompt: "You are a uxscii component generator. Generate composite component from vision data.

Component data: {id: 'login-form', type: 'form', components: [...], visualProperties: {...}}

IMPORTANT: Include component references in props.components array.

Your task:
1. Load schema from {SKILL_ROOT}/../uxscii-component-creator/schemas/uxm-component.schema.json
2. Generate .uxm with components array in props
3. Generate .md with {{component:id}} references
4. Save to ./fluxwing/components/
5. Return success

Follow uxscii standard strictly."
})
```

**Remember**: ALL Task calls must be in a SINGLE message for parallel execution!

### Phase 5: Delegate Screen Composition to Scaffolder

**CRITICAL**: YOU ARE AN ORCHESTRATOR - delegate screen creation to the screen-scaffolder skill!

**⚠️ DO NOT create screen files yourself using Write/Edit tools!**

After all components are created, use the fluxwing-screen-scaffolder to compose screens:

**Single Screen Import:**
```typescript
// Invoke screen-scaffolder skill
Skill({ command: "fluxwing-skills:fluxwing-screen-scaffolder" })

// The scaffolder will:
// 1. See all components already exist (you just created them)
// 2. Skip component creation (Step 3)
// 3. Spawn ONE composer agent (Step 4)
// 4. Composer creates .uxm + .md + .rendered.md
```

**Multiple Screenshots Import (N > 1):**
```typescript
// After analyzing ALL screenshots and creating ALL components
// Invoke screen-scaffolder skill ONCE
Skill({ command: "fluxwing-skills:fluxwing-screen-scaffolder" })

// Tell it about the screens:
// "I've imported N screenshots and created X components.
//  Please compose these N screens: [list screen names and component lists]"

// The scaffolder will:
// 1. Detect multi-screen scenario (N > 1)
// 2. Confirm with user
// 3. Skip component creation (all exist)
// 4. Spawn N composer agents in parallel (one per screen)
// 5. Each composer creates 3 files (.uxm, .md, .rendered.md)
// Result: 3N files created by scaffolder agents
```

**What you provide to scaffolder:**
- Screen name and type (from vision analysis)
- Component list (what components the screen needs)
- Layout structure (from vision data)
- Screenshot path (for .rendered.md generation)

### Phase 6: Report Results

Create comprehensive summary:

```markdown
# Screenshot Import Complete ✓

## Screenshot Analysis
- File: ${screenshotPath}
- Screen type: ${screenData.type}
- Layout: ${screenData.layout}

## Components Generated

### Atomic Components (${atomicCount})
${atomicComponents.map(c => `✓ ${c.id} (${c.type})`).join('\n')}

### Composite Components (${compositeCount})
${compositeComponents.map(c => `✓ ${c.id} (${c.type})`).join('\n')}

### Screen
✓ ${screenId}

## Files Created

**Components** (./fluxwing/components/):
- ${totalComponentFiles} files (.uxm + .md)

**Screen** (./fluxwing/screens/):
- ${screenId}.uxm
- ${screenId}.md
- ${screenId}.rendered.md

**Total: ${totalFiles} files created**

## Performance
- Vision analysis: Parallel (3 agents) ⚡
- Component generation: Parallel (${atomicCount + compositeCount} agents) ⚡
- Total time: ~${estimatedTime}s

## Next Steps

1. Review screen: `cat ./fluxwing/screens/${screenId}.rendered.md`
2. Add interaction states to components
3. Customize components as needed
4. View all components
```

## Vision Agents Used

This skill orchestrates 5 specialized vision agents:

1. **screenshot-vision-coordinator** - Orchestrates parallel analysis
2. **screenshot-component-detection** - Finds UI elements
3. **screenshot-layout-discovery** - Understands structure
4. **screenshot-visual-properties** - Extracts styling
5. **screenshot-component-generator** - Creates .uxm/.md files

## Example Interaction

```
User: Import this screenshot at /Users/me/Desktop/login.png

Skill: I'll import the UI screenshot and generate uxscii components!

[Validates screenshot exists]

Step 1: Analyzing screenshot with vision agents...
[Spawns vision coordinator]

✓ Vision analysis complete:
  - Detected 5 components
  - Screen type: login
  - Layout: vertical-center

Step 2: Generating component files in parallel...
[Spawns 5 component generator agents in parallel]

✓ All components generated!

# Screenshot Import Complete ✓

## Components Generated
✓ email-input (input)
✓ password-input (input)
✓ submit-button (button)
✓ cancel-link (link)
✓ login-form (form)

## Files Created
- 10 component files
- 3 screen files
Total: 13 files

Performance: ~45s (5 agents in parallel) ⚡

Next steps:
- Review: cat ./fluxwing/screens/login-screen.rendered.md
- Add states to make components interactive
```

## Quality Standards

Ensure imported components include:
- ✓ Valid JSON schema compliance
- ✓ Complete metadata (name, description, tags)
- ✓ Proper component types
- ✓ ASCII art matches detected visual properties
- ✓ All detected components extracted
- ✓ Screen composition includes all components
- ✓ Rendered example with realistic data

## Important Notes

- **Parallel execution is critical**: All agents must be spawned in a single message
- **Navigation elements**: Verify top nav, side nav, footer nav are detected
- **Small elements**: Don't miss icons, badges, close buttons, status indicators
- **Composite components**: Forms, cards with multiple elements
- **Screen files**: Always create 3 files (.uxm, .md, .rendered.md)
- **Validation**: Check vision data before generating components

## Error Handling

**If vision analysis fails:**
```
✗ Vision analysis failed: [error message]

Please check:
- Screenshot file exists and is readable
- File format is supported (PNG, JPG, JPEG, WebP, GIF)
- Screenshot contains visible UI elements
```

**If component generation fails:**
```
⚠️ Partial success: 3 of 5 components generated

Successful:
✓ email-input
✓ password-input
✓ submit-button

Failed:
✗ cancel-link: [error]
✗ login-form: [error]

You can retry failed components or create them manually.
```

**If no components detected:**
```
✗ No components detected in screenshot.

This could mean:
- Screenshot is blank or unclear
- UI elements are too small to detect
- Screenshot is not a UI design

Please try a different screenshot or create components manually.
```

## Resources

See `{SKILL_ROOT}/docs/` for detailed documentation on:
- screenshot-import-ascii.md - ASCII generation patterns
- screenshot-import-examples.md - Example imports
- screenshot-import-helpers.md - Helper functions
- screenshot-data-merging.md - Data structure merging
- screenshot-screen-generation.md - Screen file creation
- screenshot-validation-functions.md - Data validation

You're helping users rapidly convert visual designs into uxscii components!
