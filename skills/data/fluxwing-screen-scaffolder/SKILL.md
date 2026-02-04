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

### Step 3: Create Missing Components (Fast Mode)

**If missing components exist**, spawn designer agents in FAST MODE - one agent per component:

**CRITICAL ORCHESTRATION RULES**:
1. ⚠️ **DO NOT** create TodoWrite list and work through it yourself
2. ⚠️ **DO NOT** create components yourself using Write/Edit tools
3. ✅ **DO** use Task tool to spawn one agent per missing component
4. ✅ **DO** send ONE message with ALL Task calls (parallel execution)
5. ✅ **DO** use FAST MODE (creates .uxm only, <10s per component)

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
   - type: "container"
   - props.components: [${componentList}]
   - layout: ${layoutStructure}

   CRITICAL: Set metadata.fidelity = "detailed"

   **REQUIRED FIELD**: Screen fidelity tracks the screen's completion level.
   Even if components are sketch fidelity, the screen itself is detailed (it's a composition).
   This enables tracking progressive fidelity at both component and screen levels.

4. Create screen .md (template):
   - Use {{component:id}} syntax for component references
   - Show layout structure with placeholders

5. Create screen .rendered.md (MAIN DELIVERABLE):
   - Embed ACTUAL component ASCII (read from .md files you just created)
   - Use REAL example data (names: "Sarah Johnson", emails: "sarah@example.com", etc.)
   - Show all screen states (idle, loading, error if applicable)
   - High visual quality - this is what user will see!
   - Make it publication-ready

6. Save all 3 files to ./fluxwing/screens/

═══════════════════════════════════════
Performance Notes:
═══════════════════════════════════════

- Load ASCII patterns ONCE, reuse for all components
- Keep component .md simple (detailed version comes with enhancement)
- Focus quality effort on screen .rendered.md
- Target: 60-90 seconds total

Return summary:
- List component .md files created
- Screen files created
- Preview of .rendered.md (first 20 lines)
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

## Success Criteria

- ✓ All required components exist (created or found)
- ✓ Screen has 3 files (.uxm + .md + .rendered.md)
- ✓ Agents ran efficiently (parallel when possible)
- ✓ User can immediately use the screen design

You are building complete, production-ready screen designs with maximum agent concurrency!
