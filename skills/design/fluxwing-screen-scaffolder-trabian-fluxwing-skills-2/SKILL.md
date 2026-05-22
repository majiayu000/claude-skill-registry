---
name: Fluxwing Screen Scaffolder
description: Build complete UI screens by composing multiple uxscii components. Use when working with .uxm files, when user wants to create, scaffold, or build .uxm screens like login, dashboard, profile, settings, or checkout pages.
version: 0.0.1
author: Trabian
allowed-tools: Read, Write, Glob, Grep, Task, TodoWrite
---

# Fluxwing Screen Scaffolder

Create complete screen designs using the **uxscii standard** by orchestrating specialized agents.

## Data Location Rules

**READ from (bundled templates - reference only):**
- `{SKILL_ROOT}/../uxscii-component-creator/templates/` - 11 component templates
- `{SKILL_ROOT}/templates/` - 2 screen examples
- `{SKILL_ROOT}/docs/` - Documentation

**INVENTORY sources (check all for available components):**
- `./fluxwing/components/` - User-created components (FIRST PRIORITY)
- `./fluxwing/library/` - Customized template copies
- `{SKILL_ROOT}/../uxscii-component-creator/templates/` - Bundled templates (READ-ONLY)

**WRITE to (project workspace):**
- `./fluxwing/screens/` - Your created screens (via composer agent)

**NEVER write to skill directories - they are read-only!**

**LOAD for copy-on-update logic:**
- `{SKILL_ROOT}/../shared/docs/copy-versioning.md` - Versioning pattern for existing screens

## Your Task

**⚠️ YOU ARE AN ORCHESTRATOR - DO NOT DO THE WORK YOURSELF! ⚠️**

Your role is to **spawn agents** using the Task tool. You coordinate agents, you don't create components directly.

Help the user scaffold a complete screen by orchestrating agents in two phases:
1. **Phase 1 (Parallel)**: Spawn multiple designer agents - one per missing component using multiple Task tool calls in ONE message
2. **Phase 2 (Sequential)**: After all components exist, spawn composer agent

**Concurrency Model**:
- If 6 components are missing → spawn 6 agents in parallel using 6 Task tool calls in ONE message (~6x faster)
- Then wait for all to complete before composing screen

**CRITICAL**: Use the Task tool to spawn agents. Do NOT use TodoWrite and work through tasks yourself. Do NOT create files yourself.

**MULTI-SCREEN SCENARIOS:**

If user requests N screens (N > 1):
- ⚠️ **DO NOT** create TodoWrite list with N screen tasks and work through them
- ⚠️ **DO NOT** use Write/Edit tools to create screen files yourself
- ⚠️ **DO NOT** "help" composer agents by pre-creating any files
- ✅ **DO** spawn N composer agents in parallel (one per screen)
- ✅ **DO** send ONE message with ALL Task calls (parallel execution)
- ✅ **DO** let each composer agent independently create all 3 files (.uxm, .md, .rendered.md)

**Example:** 6 screens = ONE message with 6 Task tool calls → 18 files created by agents

You are an ORCHESTRATOR. Your job is to spawn agents, not do their work.

## Quality Presets

Scaffolder supports different quality levels for speed vs fidelity tradeoffs:

### fast (60-90s)
- Create components (sketch fidelity)
- Compose screen
- Skip enhancement
- Use when: Rapid prototyping, early iteration

**Output:**
- Components: sketch fidelity (.uxm only initially, .md by composer)
- Screen: .rendered.md with basic quality
- Time: ~60-90s for 6 components

### balanced (90-150s)
- Create components (sketch fidelity)
- Compose screen
- Enhance to basic fidelity
- Use when: Quick iteration with decent quality

**Output:**
- Components: basic fidelity (.uxm + improved .md)
- Screen: .rendered.md with good quality
- Time: ~90-150s for 6 components

### detailed (180-240s) **[DEFAULT]**
- Create components (sketch fidelity)
- Compose screen
- Enhance to detailed fidelity (hover + focus states)
- Use when: Production-ready screens, demos

**Output:**
- Components: detailed fidelity (.uxm + polished .md + states)
- Screen: .rendered.md with high quality
- Time: ~180-240s for 6 components

### production (300-400s)
- Create components (sketch fidelity)
- Compose screen
- Enhance to production fidelity (all states + full a11y)
- Use when: Final polish, publication

**Output:**
- Components: production fidelity (complete)
- Screen: .rendered.md with publication quality
- Time: ~300-400s for 6 components

**Default: detailed** (best balance of quality and speed)

## Workflow

### Step 1: Understand the Screen

Ask about the screen they want to create:

**Screen details:**
- **Screen name and purpose**: login, dashboard, profile, settings, checkout, etc.
- **Required components**: forms, navigation, cards, modals, lists, etc.
- **Layout structure**: vertical, horizontal, grid, sidebar+main, etc.

**Quality preset** (optional):
- **fast** - Quick prototype (60-90s)
- **balanced** - Good quality (90-150s)
- **detailed** - High quality (180-240s) [DEFAULT]
- **production** - Publication ready (300-400s)

If user doesn't specify, use **detailed** preset.

**Detect multi-screen requests:**

If the user's request indicates multiple screens, detect by:
- **Plural language**: "screens", "pages", "all of them"
- **Multiple file references**: Glob results showing multiple screenshots or files
- **Explicit numbers**: "5 screens", "all these", "create pages for..."

**When multiple screens detected**, confirm with the user:

```
I see you want to create [N] screens:
- [screen-name-1]
- [screen-name-2]
- [screen-name-3]
- ...

I'll create these in parallel using one composer agent per screen.
Each screen will get all 3 files (.uxm, .md, .rendered.md).

Quality preset: [preset] (default: detailed)
Estimated time: ~[X-Y] seconds

Proceed? [Yes/No]
```

**Purpose:**
- Sets clear expectations upfront
- Emphasizes .rendered.md is included for ALL screens
- Provides time estimate
- Prevents surprises

After confirmation, use **Path B workflow** (see below).

### Step 2: Component Inventory

Check what components are available **in this order**:

1. **User-created**: `./fluxwing/components/` (FIRST PRIORITY)
2. **Library**: `./fluxwing/library/` (customized templates)
3. **Bundled examples**: `{SKILL_ROOT}/../uxscii-component-creator/templates/` (READ-ONLY)

List what exists vs what needs to be created.

```typescript
// Example inventory check
const userComponents = glob('./fluxwing/components/*.uxm');
const libraryComponents = glob('./fluxwing/library/*.uxm');
const bundledComponents = glob('{SKILL_ROOT}/../uxscii-component-creator/templates/*.uxm');

const available = [...userComponents, ...libraryComponents, ...bundledComponents];
const missing = requiredComponents.filter(c => !available.includes(c));
```

### Step 2.5: Pre-Scaffolding Validation (Check for Existing Screen)

**IMPORTANT**: Before creating any screen, check if it already exists to prevent data loss.

1. **Convert screen name to kebab-case ID**:
   ```
   "Login Screen" → "login-screen"
   "User Dashboard" → "user-dashboard"
   ```

2. **Check if screen exists**:
   ```bash
   # Check for existing screen
   test -f ./fluxwing/screens/{screen-id}.uxm
   ```

3. **If screen EXISTS**:

   **Inform user and offer choices**:
   ```
   Screen '{screen-id}' already exists (version {current-version}).

   Options:
   (a) Create new version (copy-on-update: {screen-id}-v{N+1})
   (b) Create with different name
   (c) Cancel operation

   What would you like to do?
   ```

   **Handle user response**:

   - **Choice (a) - Create new version**:
     1. Load copy-versioning logic from `{SKILL_ROOT}/../shared/docs/copy-versioning.md`
     2. Read existing `{screen-id}.uxm`
     3. Find highest version (check for `{screen-id}-v2`, `-v3`, etc.)
     4. Calculate next version: `v{N+1}`
     5. Pass to composer agent with versioning parameters:
        - `baseScreenId`: Original ID (e.g., "login-screen")
        - `newScreenId`: Versioned ID (e.g., "login-screen-v2")
        - `baseOnExisting`: true
        - `sourceVersion`: Highest existing version
     6. Composer creates THREE files:
        - `{screen-id}-v{N+1}.uxm`
        - `{screen-id}-v{N+1}.md`
        - `{screen-id}-v{N+1}.rendered.md`
     7. Metadata: Increment minor version (1.0.0 → 1.1.0), update modified, preserve created

   - **Choice (b) - Different name**:
     1. Ask: "What would you like to name this screen?"
     2. Wait for user response
     3. Use new name for screen ID
     4. Proceed with normal scaffolding

   - **Choice (c) - Cancel**:
     1. Do not create any files
     2. Inform user: "Operation cancelled. No files were created."
     3. Exit workflow

4. **If screen DOES NOT exist**:
   - Proceed with normal scaffolding workflow (no versioning needed)
   - Screen will be created as `{screen-id}.uxm` (no version suffix)
   - Initial version: 1.0.0

### Workflow Branching: Single vs Multi-Screen

After completing the component inventory, choose the appropriate workflow path:

**Path A: Single Screen** (1 screen requested)
- Step 3: Create missing components (parallel)
- Step 4: Spawn ONE composer agent
- Step 5: Enhancement

**Path B: Multiple Screens** (2+ screens requested)
- Step 3: Create missing components across ALL screens (deduplicated, parallel)
- Step 4: Spawn ONE composer agent PER screen (parallel)
- Step 5: Enhancement

**Key distinction:** Path B spawns N composer agents in parallel (one per screen) instead of one.

**Example scenarios:**
- "Create a login screen" → Path A (1 screen, 1 composer)
- "Create pages for these 6 screenshots" → Path B (6 screens, 6 composers in parallel)
- "Build dashboard and settings screens" → Path B (2 screens, 2 composers in parallel)

Follow the appropriate path based on screen count. Instructions below apply to **Path A** (single screen). For **Path B** modifications, see notes in Steps 3 and 4.

### Step 3: Create Missing Components (Fast Mode)

**If missing components exist**, spawn designer agents in FAST MODE - one agent per component:

**CRITICAL ORCHESTRATION RULES**:
1. ⚠️ **DO NOT** create TodoWrite list and work through it yourself
2. ⚠️ **DO NOT** create components yourself using Write/Edit tools
3. ✅ **DO** use Task tool to spawn one agent per missing component
4. ✅ **DO** send ONE message with ALL Task calls (parallel execution)
5. ✅ **DO** use FAST MODE (creates .uxm only, <10s per component)

**Path B (Multi-screen): Component Deduplication**

When creating components for multiple screens:

1. **Inventory ALL screens first**: Collect component requirements from all N screens
2. **Deduplicate**: Create a unique list of missing components
   - Example: 6 screens might need `sidebar-nav`, but create it only once
   - Shared components across screens = created once, reused everywhere
3. **Spawn one agent per UNIQUE component**: Not one per screen × component

**Example:**
- Screen 1 needs: [sidebar-nav, button-primary, input-email]
- Screen 2 needs: [sidebar-nav, button-primary, input-password]
- Screen 3 needs: [sidebar-nav, card-metric]

**Don't spawn:** 3 × 3 = 9 agents (wasteful duplicates)
**Do spawn:** 5 unique agents (sidebar-nav, button-primary, input-email, input-password, card-metric)

**Fast Mode Creates:**
- Component .uxm files (sketch fidelity)
- NO .md files (composer will create these)

**Example: 6 missing components for banking-chat**

```typescript
Task({
  subagent_type: "general-purpose",
  model: "haiku", // Fast model
  description: "Create message-bubble (fast)",
  prompt: "Create sketch-fidelity uxscii component from template.

Component: message-bubble
Type: container
Screen context: banking-chat

FAST MODE - Speed is critical! <10 seconds target.

Your task:
1. Load minimal template: {SKILL_ROOT}/../fluxwing-component-creator/templates/minimal/container.uxm.template
2. Replace variables:
   - {{id}} = 'message-bubble'
   - {{name}} = 'Message Bubble'
   - {{description}} = 'Chat message container for banking-chat'
   - {{timestamp}} = '${new Date().toISOString()}'
   - {{screenContext}} = 'banking-chat'

3. CRITICAL: Set metadata.fidelity = "sketch"

   **REQUIRED FIELD**: The fidelity field is MANDATORY in the schema and tracks progressive enhancement.
   Fast mode MUST set fidelity to "sketch" to indicate initial scaffolding quality.

4. Verify JSON is well-formed
5. Save to ./fluxwing/components/message-bubble.uxm
6. DO NOT create .md file
7. DO NOT load documentation

VERIFICATION:
- [ ] metadata.fidelity = "sketch"
- [ ] All required fields present (name, description, created, modified, tags, category, fidelity)

Return: 'Created message-bubble.uxm (sketch fidelity)'

Target: <10 seconds"
})

Task({
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Create message-input (fast)",
  prompt: "Create sketch-fidelity uxscii component from template.

Component: message-input
Type: input
Screen context: banking-chat

FAST MODE - Speed is critical! <10 seconds target.

Your task:
1. Load minimal template: {SKILL_ROOT}/../fluxwing-component-creator/templates/minimal/input.uxm.template
2. Replace variables:
   - {{id}} = 'message-input'
   - {{name}} = 'Message Input'
   - {{description}} = 'Chat input field for banking-chat'
   - {{timestamp}} = '${new Date().toISOString()}'
   - {{placeholder}} = 'Type a message...'
   - {{label}} = 'Message'
   - {{screenContext}} = 'banking-chat'

3. CRITICAL: Set metadata.fidelity = "sketch"

   **REQUIRED FIELD**: The fidelity field is MANDATORY in the schema and tracks progressive enhancement.
   Fast mode MUST set fidelity to "sketch" to indicate initial scaffolding quality.

4. Verify JSON is well-formed
5. Save to ./fluxwing/components/message-input.uxm
6. DO NOT create .md file
7. DO NOT load documentation

VERIFICATION:
- [ ] metadata.fidelity = "sketch"
- [ ] All required fields present (name, description, created, modified, tags, category, fidelity)

Return: 'Created message-input.uxm (sketch fidelity)'

Target: <10 seconds"
})

// ... spawn ONE Task per missing component in SAME message ...
```

**Performance:** 6 components × 10s = ~60 seconds (was 120-180s)

**Wait for ALL component agents to complete before Step 4.**

### Step 4: Compose Screen with Component .md Generation

**Once all components exist**, spawn the composer agent:

**Path A (Single Screen):** Spawn ONE composer agent
**Path B (Multi-screen):** Spawn ONE composer agent PER screen (parallel)

**Example Path B:**
- 6 screens requested → spawn 6 composer agents in ONE message
- Each agent creates 3 files for its assigned screen (.uxm, .md, .rendered.md)
- All 6 agents run in parallel (~90s total, not 540s sequential)
- Result: 18 files (6 screens × 3 files)

**CRITICAL: Composer generates .md files for ALL components!**

This is the "smart composer" - it:
1. Generates missing component .md files
2. Loads documentation ONCE (not per component)
3. Creates screen .uxm + .md + .rendered.md
4. Focuses quality on .rendered.md (main deliverable)

```typescript
Task({
  subagent_type: "general-purpose",
  model: "sonnet", // Smart model for quality composition
  description: "Compose ${screenName} with components",
  prompt: `You are a uxscii screen composer creating production-ready screens.

Screen: ${screenName}
Components: ${componentList}
Layout: ${layoutStructure}
${baseOnExisting ? `
VERSIONING MODE:
- Base on existing: ${baseScreenId}
- New screen ID: ${newScreenId}
- Source version: ${sourceVersion}
- Copy-on-update: Increment minor version, preserve created timestamp
- Create THREE files with -v{N} suffix
` : ''}

YOUR PRIMARY DELIVERABLE: ${screenName}.rendered.md
This is what the user will see. Everything else supports this.

MANDATORY OUTPUTS (all 3 required):
1. ${screenName}.uxm (metadata)
2. ${screenName}.md (template with {{placeholders}})
3. ${screenName}.rendered.md (REAL data, ACTUAL ASCII) ⚠️ CRITICAL

If you complete without creating .rendered.md, you have FAILED.

Your task has TWO parts:

═══════════════════════════════════════
PART 1: Generate Component .md Files
═══════════════════════════════════════

For each component in [${componentList}]:

1. Read component .uxm from ./fluxwing/components/
2. Check if .md exists:
   - If EXISTS: Skip to next component
   - If MISSING: Generate .md file (steps 3-5)

3. Load ASCII patterns (ONCE for all components):
   {SKILL_ROOT}/../fluxwing-component-creator/docs/06-ascii-patterns.md

4. Generate simple ASCII art based on component type:
   - button: Rounded box with label
   - input: Rectangular box with placeholder
   - card: Box with title and content area
   - container: Large box for children
   - Use dimensions from .uxm (ascii.width, ascii.height)
   - Keep it simple (sketch quality, not detailed)

5. Create .md file with:
   - Component description
   - ASCII art in code block
   - Variables from .uxm props
   - Save to ./fluxwing/components/\${componentId}.md

Example .md for button:
\`\`\`markdown
# \${componentName}

\${description}

## ASCII

\`\`\`
╭──────────────────╮
│  {{label}}       │
╰──────────────────╯
\`\`\`

## Variables
- label (string): Button text
\`\`\`

═══════════════════════════════════════
PART 2: Compose Screen
═══════════════════════════════════════

1. Load schema: {SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json
2. Load screen docs: {SKILL_ROOT}/docs/04-screen-composition.md

3. Create screen .uxm:
   - ${baseOnExisting ? `Load existing: ./fluxwing/screens/${sourceVersion}.uxm` : `type: "container"`}
   - ${baseOnExisting ? `Base structure on source version` : `props.components: [${componentList}]`}
   - layout: ${layoutStructure}
   - ${baseOnExisting ? `id: "${newScreenId}" (with -v{N} suffix)` : `id: "${screenId}"`}
   - ${baseOnExisting ? `version: Increment minor from source (e.g., 1.0.0 → 1.1.0)` : `version: "1.0.0"`}
   - ${baseOnExisting ? `metadata.created: PRESERVE from ${sourceVersion}` : `metadata.created: current timestamp`}
   - ${baseOnExisting ? `metadata.modified: SET to current timestamp` : `metadata.modified: current timestamp`}

   CRITICAL: Set metadata.fidelity = "detailed"

   **REQUIRED FIELD**: Screen fidelity tracks the screen's completion level.
   Even if components are sketch fidelity, the screen itself is detailed (it's a composition).
   This enables tracking progressive fidelity at both component and screen levels.

4. Create screen .md (template):
   - Use {{component:id}} syntax for component references
   - Show layout structure with placeholders
   - ${baseOnExisting ? `Filename: ${newScreenId}.md (versioned)` : `Filename: ${screenId}.md`}

5. Create screen .rendered.md (MAIN DELIVERABLE):
   - Embed ACTUAL component ASCII (read from .md files you just created)
   - Use REAL example data (names: "Sarah Johnson", emails: "sarah@example.com", etc.)
   - Show all screen states (idle, loading, error if applicable)
   - High visual quality - this is what user will see!
   - Make it publication-ready
   - ${baseOnExisting ? `Filename: ${newScreenId}.rendered.md (versioned)` : `Filename: ${screenId}.rendered.md`}

6. Save all 3 files to ./fluxwing/screens/
   - ${baseOnExisting ? `${newScreenId}.uxm, ${newScreenId}.md, ${newScreenId}.rendered.md` : `${screenId}.uxm, ${screenId}.md, ${screenId}.rendered.md`}

═══════════════════════════════════════
Performance Notes:
═══════════════════════════════════════

- Load ASCII patterns ONCE, reuse for all components
- Keep component .md simple (detailed version comes with enhancement)
- Focus quality effort on screen .rendered.md
- Target: 60-90 seconds total

═══════════════════════════════════════
VERIFICATION CHECKLIST (before returning):
═══════════════════════════════════════

- [ ] .uxm file created and saved to ./fluxwing/screens/
- [ ] .md template created and saved to ./fluxwing/screens/
- [ ] .rendered.md created with REAL data and ACTUAL component ASCII
- [ ] All 3 files are in ./fluxwing/screens/
- [ ] .rendered.md uses realistic example data (not placeholders)
- [ ] .rendered.md embeds actual ASCII from component .md files

Return: "Created ${screenName}: .uxm ✓, .md ✓, .rendered.md ✓"
`
})
```

### Step 5: Auto-Enhancement (Based on Quality Preset)

After screen composition, optionally enhance components based on quality preset.

**Determine enhancement level:**
- fast → Skip (no enhancement)
- balanced → Enhance to "basic"
- detailed → Enhance to "detailed" [DEFAULT]
- production → Enhance to "production"

**If enhancement needed:**

```typescript
Task({
  subagent_type: "general-purpose",
  model: "sonnet", // Quality model for enhancement
  description: "Enhance screen components to ${targetFidelity}",
  prompt: `Enhance all components in ${screenName} to ${targetFidelity} fidelity.

Screen: ${screenName}
Components: ${componentList}
Current fidelity: sketch
Target fidelity: ${targetFidelity}

Use fluxwing-enhancer patterns:

Your task:
1. Load enhancement patterns: {SKILL_ROOT}/../fluxwing-enhancer/docs/enhancement-patterns.md
2. Load state templates: {SKILL_ROOT}/../fluxwing-component-creator/templates/state-additions/

3. For EACH component (process in parallel if possible):

   Read: ./fluxwing/components/\${componentId}.uxm
   Read: ./fluxwing/components/\${componentId}.md

   Enhance based on target:

   ${targetFidelity === 'basic' ? `
   basic fidelity:
   - Improve metadata.description (specific, 1-2 sentences)
   - Add relevant tags
   - Polish .md ASCII (clean, aligned)
   - Keep default state only
   - CRITICAL: Update metadata.fidelity = "basic" (REQUIRED FIELD)
   ` : ''}

   ${targetFidelity === 'detailed' ? `
   detailed fidelity:
   - All "basic" enhancements
   - Add hover state (use templates/state-additions/hover.json)
   - Add focus state (use templates/state-additions/focus.json)
   - Polish ASCII art (rounded corners, smooth)
   - Add props.examples array (2-3 examples)
   - CRITICAL: Update metadata.fidelity = "detailed" (REQUIRED FIELD)
   ` : ''}

   ${targetFidelity === 'production' ? `
   production fidelity:
   - All "detailed" enhancements
   - Add disabled state (if applicable)
   - Add error state (if form component)
   - Complete accessibility metadata
   - Add keyboard shortcuts
   - Pixel-perfect ASCII
   - CRITICAL: Update metadata.fidelity = "production" (REQUIRED FIELD)
   ` : ''}

   Save: Updated .uxm and .md to ./fluxwing/components/

4. After ALL components enhanced:

   Regenerate screen .rendered.md:
   - Read enhanced component .md files
   - Embed improved ASCII in .rendered.md
   - Maintain real example data
   - Save to ./fluxwing/screens/

5. Return summary:
   - Components enhanced: [list with changes]
   - Total time: Xs
   - Screen .rendered.md regenerated

Target time:
- basic: 30s (parallel for all components)
- detailed: 90s (parallel for all components)
- production: 180s (parallel for all components)

Note: Process components in parallel when possible for maximum speed!
`
})
```

**Enhancement is parallel:** All 6 components enhanced simultaneously, so time ≈ single component time!

### Step 5.5: Validate Screen

**REQUIRED**: Validate the screen file against the schema after composition.

```bash
# Validate the screen
node {SKILL_ROOT}/../fluxwing-validator/validate-screen.js \
  ./fluxwing/screens/${screenId}.uxm \
  {SKILL_ROOT}/../fluxwing-component-creator/schemas/uxm-component.schema.json
```

**Expected behavior**:
- ✅ **If validation passes**: Continue to Step 6 (Report Results)
- ❌ **If validation fails**: Report errors clearly and stop execution

**Screen-specific checks**:
- Validates against uxscii schema (same as components)
- Checks for .rendered.md file (warning if missing)
- Checks if composed components exist (warnings for missing components)

**Example output** (success):
```
✓ Valid: login-screen
  Type: container
  Version: 1.0.0
  States: 3
  Props: 3

⚠ Warnings:
  Warning 1: Referenced component not found: custom-input
  Location: composed
```

**If validation fails**, show errors to user:
```
✗ Validation Failed

  Error 1: must have required property 'fidelity'
  Location: metadata
```

### Step 6: Report Results

Create comprehensive summary including enhancement details:

```markdown
# Screen Scaffolding Complete ✓

## Screen: ${screenName}
## Quality Preset: ${qualityPreset}

### Phase 1: Fast Component Creation ⚡
${missingComponents.map(c => `✓ ${c}.uxm (sketch fidelity, ~10s)`).join('\n')}

Time: ~${missingComponents.length * 10}s

### Phase 2: Smart Composition 🎨
Component .md files generated:
${componentList.map(c => `✓ ${c}.md (by composer)`).join('\n')}

Screen files created:
✓ ${screenName}.uxm
✓ ${screenName}.md (template)
✓ ${screenName}.rendered.md

Time: ~60-90s

${qualityPreset !== 'fast' ? `
### Phase 3: Auto-Enhancement ✨
Components enhanced to ${targetFidelity} fidelity:
${componentList.map(c => `✓ ${c}: sketch → ${targetFidelity}`).join('\n')}

Enhancements applied:
${targetFidelity === 'basic' ? '- Improved descriptions\n- Added specific tags\n- Polished ASCII' : ''}
${targetFidelity === 'detailed' ? '- Improved descriptions\n- Added hover + focus states\n- Polished ASCII\n- Added usage examples' : ''}
${targetFidelity === 'production' ? '- All detailed enhancements\n- Added disabled + error states\n- Complete accessibility\n- Pixel-perfect ASCII' : ''}

Screen .rendered.md regenerated with enhanced components

Time: ~${enhancementTime[targetFidelity]}s
` : ''}

### Total Time: ~${totalTime}s (${Math.round(totalTime/60)} minutes)

### Performance
- Target: ${targetTime[qualityPreset]}
- Actual: ${totalTime}s
- Status: ${totalTime <= targetTime[qualityPreset] ? '✓ ON TARGET' : '⚠ OVER TARGET'}

## Files Created

**Components** (./fluxwing/components/):
- ${componentList.length} .uxm files (${finalFidelity} fidelity)
- ${componentList.length} .md files

**Screen** (./fluxwing/screens/):
- ${screenName}.uxm
- ${screenName}.md
- ${screenName}.rendered.md

**Total: ${componentList.length * 2 + 3} files**

## Quality Assessment

- Component fidelity: ${finalFidelity}
- Screen .rendered.md: ${qualityPreset === 'production' ? 'Publication-ready' : qualityPreset === 'detailed' ? 'High quality' : qualityPreset === 'balanced' ? 'Good quality' : 'Basic quality'}
- States included: ${statesCount} states per component
- Accessibility: ${qualityPreset === 'production' ? 'Complete' : qualityPreset === 'detailed' ? 'Good' : 'Basic'}

## Next Steps

1. **Review rendered screen:**
   \`cat ./fluxwing/screens/${screenName}.rendered.md\`

2. **Further enhancement (optional):**
   ${qualityPreset !== 'production' ? `Use /fluxwing-enhance to upgrade to ${nextFidelity} fidelity` : 'Already at maximum fidelity'}

3. **Customize components:**
   Edit ./fluxwing/components/ files as needed

4. **View components:**
   Use /fluxwing-view to inspect individual components
```

## Parallel Execution Strategy

**Two-phase concurrency model:**

**Phase 1 - Component Creation (Parallel)**:
- If N components are missing → spawn N agents in parallel (one per component)
- All component agents run simultaneously (~Nx faster than sequential)
- Each agent independently creates its component files and tracks progress

**Phase 2 - Screen Composition (Sequential)**:
- After ALL component agents complete → spawn composer agent
- Composer reads all created components and assembles screen
- Cannot run in parallel with Phase 1 (needs components to exist first)

**Performance Example**:
- 6 missing components + screen composition
- Old way (sequential): ~180 seconds (6 × 30s)
- New way (parallel Phase 1): ~30 seconds (6 agents at once) + ~30s composer = ~60 seconds total
- **3x faster!**

## Example Interaction

```
User: Create a login screen

Skill: I'll help you create a login screen! Let me check what components we have...

[Checks ./fluxwing/components/, ./fluxwing/library/, bundled templates]

I found:
✓ email-input (exists in ./fluxwing/components/)
✗ password-input (needs to be created)
✗ submit-button (needs to be created)

I'll use a two-phase approach:
- Phase 1: Spawn 2 agents in parallel (one per missing component)
- Phase 2: After components complete, spawn composer agent

[Spawns 2 component agents in parallel]

✓ password-input agent completed
✓ submit-button agent completed

[Now spawns composer agent]

✓ Composer agent created login screen

Total: 7 files created in ./fluxwing/
Performance: ~2x faster with parallel component creation!
```

## Error Handling

**If designer agent fails:**
- Report which components failed
- User can create manually or retry
- Composer agent cannot proceed without components

**If composer agent fails:**
- Components are still created and usable
- User can manually compose screen
- Provide specific error context

## Common Rationalizations That Mean You're Failing

If you catch yourself thinking ANY of these thoughts, STOP. You are rationalizing. Use the Task tool to spawn agents instead.

**About creating files directly:**
- "I'll just create the files directly, it's faster" → WRONG. Spawn agents.
- "Write is simpler than Task for this" → WRONG. You're an orchestrator, not a worker.
- "I'll create .uxm and .md myself, agents can do .rendered later" → WRONG. Agents do ALL 3 files.
- "Let me help by pre-creating some files first" → WRONG. Agents are self-sufficient.
- "The user wants it fast, no time for agents" → WRONG. Parallel agents ARE faster.

**About multi-screen scenarios:**
- "Orchestration is overkill for this batch" → WRONG. Batches are exactly when you orchestrate.
- "I'll do the first screen to show progress" → WRONG. Spawn all agents in parallel.
- "Let me create a todo list and work through screens" → WRONG. TodoWrite + sequential work = slowest path.
- "11 screens is too many for parallel agents" → WRONG. That's the perfect use case.

**About the .rendered.md file:**
- "I'll skip .rendered.md for now" → WRONG. It's the PRIMARY deliverable.
- "Template (.md) is enough" → WRONG. User needs to SEE the actual layout.
- ".rendered.md can be added later" → WRONG. Composer creates it NOW.

**Why these rationalizations happen:**
- Write/Edit tools feel more direct than Task tool
- Creating files yourself feels productive
- Spawning agents feels abstract
- But: You're an ORCHESTRATOR. Your job is coordination, not execution.

**What to do instead:**
1. Detect how many screens are needed
2. Spawn that many composer agents in ONE message
3. Wait for results
4. Report completion

STOP. Use the Task tool. You are an orchestrator, not a worker.

## Success Criteria

- ✓ All required components exist (created or found)
- ✓ Screen has 3 files (.uxm + .md + .rendered.md)
- ✓ Agents ran efficiently (parallel when possible)
- ✓ User can immediately use the screen design

You are building complete, production-ready screen designs with maximum agent concurrency!
