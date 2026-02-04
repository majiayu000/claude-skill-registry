---
name: Fluxwing Enhancer
description: Enhance uxscii components from sketch to production fidelity. Use when working with .uxm files marked as "fidelity: sketch" or when user wants to add detail and polish to components.
version: 0.0.1
author: Trabian
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite
---

# Fluxwing Enhancer

Progressively enhance uxscii components from sketch to production quality.

## Data Location Rules

**READ from:**
- `./fluxwing/components/` - User components to enhance
- `{SKILL_ROOT}/../fluxwing-component-creator/templates/state-additions/` - State templates
- `{SKILL_ROOT}/docs/` - Enhancement documentation

**WRITE to:**
- `./fluxwing/components/` - Updated component files (in place)
- `./fluxwing/screens/` - Updated screen .rendered.md (if applicable)

## Fidelity Levels

### sketch (Fast Scaffold Output)
- Basic .uxm with minimal metadata
- May lack .md file or have simple .md
- Single "default" state
- Creation time: ~10 seconds

**Characteristics:**
- Minimal description
- Generic tags
- No examples
- Basic props only

### basic (First Enhancement)
- Enriched metadata (better description, tags)
- Simple .md with clean ASCII
- Default state only
- Enhancement time: ~30 seconds

**Improvements over sketch:**
- Detailed description
- Specific tags
- Clean ASCII art
- Documented variables

### detailed (Second Enhancement)
- Rich metadata with usage examples
- Polished .md with careful ASCII art
- 2-3 interaction states (hover, focus)
- Enhancement time: ~90 seconds

**Improvements over basic:**
- Usage examples in metadata
- Hover + focus states
- Polished ASCII
- Props.examples array

### production (Final Polish)
- Complete metadata with accessibility details
- Publication-quality ASCII
- All relevant states (hover, focus, disabled, active, error)
- Full documentation
- Enhancement time: ~180 seconds

**Improvements over detailed:**
- All applicable states
- Complete accessibility metadata
- Keyboard shortcuts
- Publication-quality ASCII
- Edge case documentation

## Your Task

Help users enhance components from current fidelity to target fidelity.

### Workflow

#### Step 1: Inventory Components

Check what components exist and their current fidelity:

```bash
ls ./fluxwing/components/*.uxm
```

For each component, read fidelity level:
```bash
python3 -c "import json; print(json.load(open('./fluxwing/components/button.uxm'))['metadata'].get('fidelity', 'detailed'))"
```

List components by fidelity:
- sketch: [component-ids]
- basic: [component-ids]
- detailed: [component-ids]
- production: [component-ids]

#### Step 2: Determine Target Fidelity

Ask user or use defaults:

**User specifies:**
- "Enhance to basic"
- "Upgrade to detailed"
- "Make production-ready"

**Auto-select (if not specified):**
- sketch → detailed (most common, best balance)
- basic → detailed
- detailed → production

#### Step 3: Spawn Enhancement Agents

**If enhancing multiple components (3+):**
- Spawn agents in parallel (one per component)
- Each agent enhances independently
- Wait for all to complete

**If enhancing single component:**
- Spawn single agent
- Focus on quality

**Enhancement Agent Prompt:**

```typescript
Task({
  subagent_type: "general-purpose",
  model: "sonnet", // Quality matters for enhancement
  description: "Enhance ${componentId} to ${targetFidelity}",
  prompt: `Enhance uxscii component from ${currentFidelity} to ${targetFidelity}.

Component: ${componentId}
Current fidelity: ${currentFidelity}
Target fidelity: ${targetFidelity}

Your task:
1. Read ./fluxwing/components/${componentId}.uxm
2. Read ./fluxwing/components/${componentId}.md (if exists)
3. Load enhancement patterns: {SKILL_ROOT}/docs/enhancement-patterns.md
4. Load state templates: {SKILL_ROOT}/../fluxwing-component-creator/templates/state-additions/

5. Enhance based on target fidelity:

   ${targetFidelity === 'basic' ? `
   For "basic" fidelity:
   - Improve metadata.description (1-2 sentences, specific)
   - Add specific tags (not just generic type)
   - Create/improve .md with clean ASCII art
   - Keep single default state
   - Update fidelity field to "basic"
   ` : ''}

   ${targetFidelity === 'detailed' ? `
   For "detailed" fidelity:
   - All "basic" enhancements (if not already done)
   - Add hover state (use {SKILL_ROOT}/../fluxwing-component-creator/templates/state-additions/hover.json)
   - Add focus state (use {SKILL_ROOT}/../fluxwing-component-creator/templates/state-additions/focus.json)
   - Polish ASCII art (smooth alignment, consistent spacing)
   - Add props.examples array (2-3 usage examples)
   - Update fidelity field to "detailed"
   ` : ''}

   ${targetFidelity === 'production' ? `
   For "production" fidelity:
   - All "detailed" enhancements (if not already done)
   - Add disabled state (if applicable for component type)
   - Add error state (if applicable for component type)
   - Complete accessibility metadata:
     - aria-label templates
     - keyboard shortcuts
     - screen reader descriptions
   - Add behavior.keyboardShortcuts (if interactive)
   - Publication-quality ASCII (pixel-perfect alignment)
   - Document edge cases in description
   - Update fidelity field to "production"
   ` : ''}

6. Save updated files (overwrite existing)
7. Verify JSON is valid
8. Return enhancement summary

Target time: ${targetTime[targetFidelity]} seconds

Return format:
"Enhanced ${componentId}: ${currentFidelity} → ${targetFidelity}
- Added X states
- Improved metadata
- Polished ASCII"
`
})
```

#### Step 4: Regenerate Screen (If Applicable)

If components belong to a screen, regenerate .rendered.md:

```bash
# Find which screen uses this component
grep -l "${componentId}" ./fluxwing/screens/*.uxm
```

If found, respawn composer to regenerate .rendered.md with enhanced components.

#### Step 5: Report Results

```markdown
# Enhancement Complete ✓

## Components Enhanced

${enhancedComponents.map(c => `
### ${c.id}
- Before: ${c.oldFidelity}
- After: ${c.newFidelity}
- Time: ${c.time}s
- Changes:
  - ${c.changes.join('\n  - ')}
`).join('\n')}

## Total Time: ${totalTime}s

## Screens Updated
${updatedScreens.length > 0 ? updatedScreens.map(s => `- ${s}.rendered.md regenerated`).join('\n') : 'None'}

## Next Steps
1. Review enhanced components: \`ls ./fluxwing/components/\`
2. View updated screen: \`cat ./fluxwing/screens/${screenName}.rendered.md\`
3. Customize as needed
```

## Example Usage

**User:** "Enhance all components in banking-chat to detailed"

**Enhancer:**
1. Finds 6 sketch components
2. Spawns 6 enhancement agents (parallel)
3. Each agent: sketch → detailed (~90s)
4. Regenerates banking-chat.rendered.md
5. Total time: ~120 seconds

**User:** "Make submit-button production-ready"

**Enhancer:**
1. Finds submit-button (detailed fidelity)
2. Spawns 1 enhancement agent
3. Agent: detailed → production (~180s)
4. Updates screen if applicable
5. Total time: ~180 seconds

## Success Criteria

- ✓ Components upgraded to target fidelity
- ✓ All states added as specified
- ✓ ASCII art improved
- ✓ Metadata enriched
- ✓ Screen .rendered.md regenerated (if applicable)
- ✓ All files validate against schema

You are building a progressive enhancement system for maximum flexibility!
