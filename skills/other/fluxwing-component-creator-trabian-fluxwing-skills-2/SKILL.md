---
name: Fluxwing Component Creator
description: Create uxscii components with ASCII art and structured metadata when user wants to create, build, or design UI components. Use when working with .uxm files, when user mentions .uxm components, or when creating buttons, inputs, cards, forms, modals, or navigation.
version: 0.0.1
author: Trabian
allowed-tools: Read, Write, Edit, Glob, Grep, Task, TodoWrite, Bash
---

# Fluxwing Component Creator

You are helping the user create uxscii component(s) using the **uxscii standard** by orchestrating the designer agent.

## Data Location Rules

**READ from (bundled templates - reference only):**
- `{SKILL_ROOT}/templates/` - 11 component templates
- `{SKILL_ROOT}/docs/` - Documentation

**INVENTORY sources:**
- `./fluxwing/components/` - User components
- `./fluxwing/library/` - Customized templates
- `{SKILL_ROOT}/templates/` - Bundled templates (READ-ONLY)

**WRITE to (project workspace - via designer agent):**
- `./fluxwing/components/` - Your created components

**NEVER write to skill directory - it's read-only!**

**LOAD for copy-on-update logic:**
- `{SKILL_ROOT}/../shared/docs/copy-versioning.md` - Versioning pattern for existing components

## Your Task

Help the user create uxscii component(s) by gathering requirements and spawning designer agent(s).

**Supports both single and multi-component creation:**
- Single: "Create a submit button"
- Multiple: "Create submit-button, cancel-button, and email-input" (agents run in parallel)

## Speed Modes

Fluxwing supports two creation modes optimized for different use cases:

### Fast Mode (Scaffolding)
**When:** Scaffolder creates multiple components in parallel
**Speed:** ~10 seconds per component
**Output:** `.uxm` only (fidelity: sketch)
**Method:** Template-based variable substitution

Fast mode skips:
- Documentation loading
- ASCII art generation
- Detailed metadata

### Detailed Mode (Standalone)
**When:** User explicitly creates single component
**Speed:** ~60-90 seconds per component
**Output:** `.uxm` + `.md` (fidelity: detailed)
**Method:** Full docs, careful ASCII generation

Detailed mode includes:
- Complete documentation reference
- Hand-crafted ASCII art
- Rich metadata with examples

**Default:** Fast mode when called by scaffolder, detailed mode otherwise

## Workflow

### Step 1: Determine Creation Mode & Parse Request

**First, determine creation mode:**

Check context to decide fast vs detailed mode:

**Use Fast Mode if:**
- Called by scaffolder skill (check for "screen context" in request)
- User explicitly requests "fast" or "quick" component
- Creating multiple components (6+ components)

**Use Detailed Mode if:**
- User creating single component interactively
- User requests "detailed" or "production" quality
- No screen context provided

**Default:** Detailed mode (safer, better quality)

**Then, detect if user wants single or multiple components:**

1. **Single component request**:
   - "Create a submit button"
   - "I need a card component"
   - Proceed with single-component workflow (Steps 2-4)

2. **Multiple component request**:
   - "Create submit-button, cancel-button, and email-input"
   - "I need a button, input, and card"
   - "Create these components: [list]"
   - Proceed with multi-component workflow (see Step 3b)

**For each component, gather:**
- **Component name** (will be converted to kebab-case, e.g., "Submit Button" → "submit-button")
- **Component type**: button, input, card, navigation, form, list, modal, table, badge, alert, container, text, image, divider, or custom
- **Key properties**: What should be configurable? (text, colors, sizes, etc.)
- **Visual style preferences**: rounded, sharp, minimal, detailed, etc.

**If details are missing**: Make reasonable assumptions based on component type and common patterns. Don't over-ask.

**Note**: Components are created with default state only for fast MVP prototyping. Users can expand components later to add interactive states (hover, focus, disabled, etc.).

### Step 2: Check for Similar Templates

Browse available templates to offer starting points:

```typescript
// Check bundled templates
const bundledTemplates = glob('{SKILL_ROOT}/templates/*.uxm');
// Check user library
const libraryTemplates = glob('./fluxwing/library/*.uxm');

// Suggest similar templates if found
if (similarTemplates.length > 0) {
  console.log(`Similar templates found: ${similarTemplates.join(', ')}`);
  console.log('Would you like to base this on an existing template or create from scratch?');
}
```

### Step 3: Pre-Creation Validation (Check for Existing Component)

**IMPORTANT**: Before creating any component, check if it already exists to prevent data loss.

**For each component you plan to create:**

1. **Convert to kebab-case ID**:
   ```
   "Submit Button" → "submit-button"
   "User Profile Card" → "user-profile-card"
   ```

2. **Check if component exists**:
   ```bash
   # Check for existing component
   test -f ./fluxwing/components/{component-id}.uxm
   ```

3. **If component EXISTS**:

   **Inform user and offer choices**:
   ```
   Component '{component-id}' already exists (version {current-version}).

   Options:
   (a) Create new version (copy-on-update: {component-id}-v{N+1})
   (b) Create with different name
   (c) Cancel operation

   What would you like to do?
   ```

   **Handle user response**:

   - **Choice (a) - Create new version**:
     1. Load copy-versioning logic from `{SKILL_ROOT}/../shared/docs/copy-versioning.md`
     2. Read existing `{component-id}.uxm`
     3. Find highest version (check for `{component-id}-v2`, `-v3`, etc.)
     4. Calculate next version: `v{N+1}`
     5. Pass to designer agent with versioning parameters:
        - `baseComponentId`: Original ID (e.g., "submit-button")
        - `newComponentId`: Versioned ID (e.g., "submit-button-v2")
        - `baseOnExisting`: true
        - `sourceVersion`: Highest existing version
     6. Designer creates `{component-id}-v{N+1}.uxm` and `.md`
     7. Metadata: Increment minor version (1.0.0 → 1.1.0), update modified, preserve created

   - **Choice (b) - Different name**:
     1. Ask: "What would you like to name this component?"
     2. Wait for user response
     3. Use new name for component ID
     4. Proceed with normal creation

   - **Choice (c) - Cancel**:
     1. Do not create any files
     2. Inform user: "Operation cancelled. No files were created."
     3. Exit workflow

4. **If component DOES NOT exist**:
   - Proceed with normal creation workflow (no versioning needed)
   - Component will be created as `{component-id}.uxm` (no version suffix)
   - Initial version: 1.0.0

**For multiple components**: Check existence for EACH component individually. Some may need versioning, others may not.

## Agent Prompts

### Fast Mode Agent (For Scaffolder)

Use this when creating multiple components quickly:

```typescript
Task({
  subagent_type: "general-purpose",
  // Note: model parameter not yet supported by Task tool
  description: "Create ${componentName} (fast)",
  prompt: `Create sketch-fidelity uxscii component from template.

Component: ${componentName}
Type: ${componentType}
Screen context: ${screenContext}
${baseOnExisting ? `
VERSIONING MODE:
- Base on existing: ${baseComponentId}
- New component ID: ${newComponentId}
- Source version: ${sourceVersion}
- Copy-on-update: Increment minor version, preserve created timestamp
` : ''}

FAST MODE - Speed is critical! <10 seconds target.

Your task:
1. ${baseOnExisting ? `Load existing: ./fluxwing/components/${sourceVersion}.uxm` : `Load minimal template: {SKILL_ROOT}/templates/minimal/${componentType}.uxm.template`}
2. ${baseOnExisting ? `Read current version number and metadata.created timestamp` : `If template not found, FAIL with error: "No template found for type: ${componentType}"`}
3. Replace template variables (component type specific):

   **Common variables (all types):**
   - {{id}} = "${componentId}"
   - {{name}} = "${componentName}"
   - {{description}} = "${description || 'Component for ' + screenContext}"
   - {{timestamp}} = "${new Date().toISOString()}"

   **Component-specific variables:**
   | Type       | Variables                                  |
   |------------|-------------------------------------------|
   | button     | {{label}}, {{variant}}                    |
   | input      | {{placeholder}}, {{type}}, {{value}}      |
   | text       | {{content}}, {{align}}                    |
   | heading    | {{text}}, {{level}}                       |
   | card       | {{title}}, {{content}}                    |
   | modal      | {{title}}, {{content}}                    |
   | container  | {{content}}, {{direction}}                |
   | navigation | {{items}}, {{orientation}}                |
   | form       | {{fields}}, {{action}}                    |
   | table      | {{headers}}, {{rows}}                     |
   | list       | {{items}}, {{type}}                       |

   Use component name as default value if variable not provided.

4. CRITICAL: Set metadata.fidelity = "sketch"

   **REQUIRED FIELD**: The fidelity field is MANDATORY in the schema and tracks progressive enhancement.
   Fast mode MUST set fidelity to "sketch" to indicate initial scaffolding quality.

   This field enables progressive fidelity workflow:
   - sketch (fast mode) → basic → detailed → production

5. ${baseOnExisting ? `Update version metadata:
   - id: "${newComponentId}" (versioned ID)
   - version: Increment minor from source (e.g., 1.0.0 → 1.1.0)
   - metadata.created: PRESERVE from ${sourceVersion}
   - metadata.modified: SET to current timestamp
` : `Verify JSON is well-formed (quick syntax check)`}
6. Save to ./fluxwing/components/${componentId}.uxm
7. DO NOT create .md file
8. DO NOT load documentation
9. DO NOT generate ASCII art

VERIFICATION CHECKLIST:
- [ ] metadata.fidelity field is set to "sketch"
- [ ] All required fields are present (name, description, created, modified, tags, category, fidelity)
- [ ] JSON is valid and well-formed

Return message: "Created ${componentId}.uxm (sketch fidelity)"

Target: <10 seconds
`
})
```

### Detailed Mode Agent (For User)

Use this when creating single component with full quality:

```typescript
Task({
  subagent_type: "general-purpose",
  // Note: model parameter not yet supported by Task tool
  description: "Create ${componentName} (detailed)",
  prompt: `Create production-ready uxscii component with full documentation.

Component: ${componentName}
Type: ${componentType}
${baseOnExisting ? `
VERSIONING MODE:
- Base on existing: ${baseComponentId}
- New component ID: ${newComponentId}
- Source version: ${sourceVersion}
- Copy-on-update: Increment minor version, preserve created timestamp
` : ''}

DETAILED MODE - Quality is priority.

Your task:
1. ${baseOnExisting ? `Load existing: ./fluxwing/components/${sourceVersion}.uxm` : `Load schema: {SKILL_ROOT}/schemas/uxm-component.schema.json`}
2. ${baseOnExisting ? `Read copy-versioning docs: {SKILL_ROOT}/../shared/docs/copy-versioning.md` : `Load docs: {SKILL_ROOT}/docs/03-component-creation.md`}
3. Load ASCII patterns: {SKILL_ROOT}/docs/06-ascii-patterns.md
4. Create rich .uxm with:
   - Detailed metadata.description
   - Relevant tags
   - Complete props with examples
   - Default + hover states
   - Full accessibility metadata

5. CRITICAL: Set metadata.fidelity = "detailed"

   **REQUIRED FIELD**: The fidelity field is MANDATORY in the schema and tracks progressive enhancement.
   Detailed mode MUST set fidelity to "detailed" to indicate high-quality production-ready components.

   This field enables progressive fidelity workflow:
   - sketch → basic → detailed (detailed mode) → production

6. ${baseOnExisting ? `Update version metadata:
   - id: "${newComponentId}" (versioned ID with -v{N} suffix)
   - version: Increment minor from source (e.g., 1.0.0 → 1.1.0)
   - metadata.created: PRESERVE from ${sourceVersion}
   - metadata.modified: SET to current timestamp
   - metadata.fidelity: Update if enhancing (preserve or upgrade)
` : `Verify JSON is well-formed`}

7. Create polished .md with:
   - Clean ASCII art using box-drawing characters
   - All variables documented
   - State examples
   - ${baseOnExisting ? `Filename: ${newComponentId}.md (versioned)` : `Filename: ${componentId}.md`}

8. Validate against schema
9. Save both files to ./fluxwing/components/
   - ${baseOnExisting ? `${newComponentId}.uxm and ${newComponentId}.md` : `${componentId}.uxm and ${componentId}.md`}

VERIFICATION CHECKLIST:
- [ ] metadata.fidelity field is set to "detailed"
- [ ] All required fields are present (name, description, created, modified, tags, category, fidelity)
- [ ] Both .uxm and .md files are created
- [ ] ${baseOnExisting ? `Version incremented and ID has -v{N} suffix` : `Component ID is kebab-case`}
- [ ] ${baseOnExisting ? `metadata.created preserved from source` : `metadata.created set to current timestamp`}
- [ ] JSON is valid and well-formed

Return: Component summary with preview ${baseOnExisting ? `- Mention version created` : ``}

Target: 60-90 seconds
`
})
```

### Step 3a: Spawn Designer Agent (Single Component)

**For SINGLE component requests**, spawn one designer agent:

```typescript
Task({
  subagent_type: "general-purpose",
  description: "Create single uxscii component",
  prompt: `You are a uxscii component designer creating production-ready components.

Component requirements:
- Name: ${componentName}
- Type: ${componentType}
- Key properties: ${keyProperties}
- Visual style: ${visualStyle}

Your task:
1. Load schema from {SKILL_ROOT}/schemas/uxm-component.schema.json
2. Load documentation from {SKILL_ROOT}/docs/03-component-creation.md and 06-ascii-patterns.md
3. Check {SKILL_ROOT}/templates/ for similar examples
4. Create .uxm file (valid JSON with default state only)
5. Create .md file (ASCII template with default state only)
6. Save both files to ./fluxwing/components/
7. Validate using: node {SKILL_ROOT}/../fluxwing-validator/validate-component.js ./fluxwing/components/${componentId}.uxm {SKILL_ROOT}/schemas/uxm-component.schema.json
8. Use TodoWrite to track progress
9. Return component summary with ASCII preview

Component creation guidelines:
- Create default state only for fast MVP prototyping
- Use consistent box-drawing characters (see docs/06-ascii-patterns.md)
- Include complete accessibility attributes (ARIA roles, keyboard support)
- Follow naming conventions: kebab-case IDs, camelCase variables
- Ensure all template variables in .md are defined in .uxm props
- Keep ASCII dimensions reasonable (width: 1-120, height: 1-50)

Data locations:
- READ templates from: {SKILL_ROOT}/templates/ (reference only)
- WRITE components to: ./fluxwing/components/ (your output)
- NEVER write to skill directory

Follow the uxscii standard strictly for production quality.`
})
```

**Wait for designer agent to complete.**

### Step 3b: Spawn Designer Agents (Multiple Components - IN PARALLEL)

**For MULTIPLE component requests**, spawn ALL designer agents in a SINGLE message for maximum parallelism:

**CRITICAL**: You MUST send ONE message with multiple Task calls to achieve parallel execution.

**DO THIS**: One message with N Task calls (one per component)
**DON'T DO THIS**: Separate messages for each component (runs sequentially)

```typescript
// Example: User wants submit-button, cancel-button, email-input

Task({
  subagent_type: "general-purpose",
  description: "Create submit-button component",
  prompt: `You are a uxscii component designer creating production-ready components.

Component requirements:
- Name: submit-button
- Type: button
- Key properties: text, variant
- Visual style: rounded, filled

Your task:
1. Load schema from {SKILL_ROOT}/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/03-component-creation.md and 06-ascii-patterns.md
3. Create .uxm file (valid JSON with default state only)
4. Create .md file (ASCII template with default state only)
5. Save to ./fluxwing/components/
6. Validate using: node {SKILL_ROOT}/../fluxwing-validator/validate-component.js
7. Return component summary

Follow uxscii standard strictly. Create default state only for fast MVP.`
})

Task({
  subagent_type: "general-purpose",
  description: "Create cancel-button component",
  prompt: `You are a uxscii component designer creating production-ready components.

Component requirements:
- Name: cancel-button
- Type: button
- Key properties: text, variant
- Visual style: rounded, outlined

Your task:
1. Load schema from {SKILL_ROOT}/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/03-component-creation.md and 06-ascii-patterns.md
3. Create .uxm file (valid JSON with default state only)
4. Create .md file (ASCII template with default state only)
5. Save to ./fluxwing/components/
6. Validate using: node {SKILL_ROOT}/../fluxwing-validator/validate-component.js
7. Return component summary

Follow uxscii standard strictly. Create default state only for fast MVP.`
})

Task({
  subagent_type: "general-purpose",
  description: "Create email-input component",
  prompt: `You are a uxscii component designer creating production-ready components.

Component requirements:
- Name: email-input
- Type: input
- Key properties: placeholder, value
- Visual style: light border, minimal

Your task:
1. Load schema from {SKILL_ROOT}/schemas/uxm-component.schema.json
2. Load docs from {SKILL_ROOT}/docs/03-component-creation.md and 06-ascii-patterns.md
3. Create .uxm file (valid JSON with default state only)
4. Create .md file (ASCII template with default state only)
5. Save to ./fluxwing/components/
6. Validate using: node {SKILL_ROOT}/../fluxwing-validator/validate-component.js
7. Return component summary

Follow uxscii standard strictly. Create default state only for fast MVP.`
})

... all Task calls in the SAME message for parallel execution ...
```

**Wait for ALL designer agents to complete.**

**Performance Benefit**: Creating 3 components in parallel is ~3x faster than sequential creation!

### Step 3c: Validate Created Components (Optional but Recommended)

After the designer agent(s) complete, validate the created components using the fast validation script:

```bash
# For single component
node {SKILL_ROOT}/../fluxwing-validator/validate-component.js \\
  ./fluxwing/components/${componentId}.uxm \\
  {SKILL_ROOT}/schemas/uxm-component.schema.json

# For multiple components, validate each one
node {SKILL_ROOT}/../fluxwing-validator/validate-component.js \\
  ./fluxwing/components/submit-button.uxm \\
  {SKILL_ROOT}/schemas/uxm-component.schema.json

node {SKILL_ROOT}/../fluxwing-validator/validate-component.js \\
  ./fluxwing/components/cancel-button.uxm \\
  {SKILL_ROOT}/schemas/uxm-component.schema.json
```

**Validation output:**
- ✓ If valid: Shows component summary (type, states, props)
- ✗ If invalid: Shows specific errors that need fixing

**Performance**: ~80ms per component (very fast!)

**If validation fails:**
1. Read the error messages carefully
2. Fix the issues in the .uxm or .md files
3. Re-validate before reporting to user

**Note**: The validation script checks:
- JSON schema compliance
- .md file exists
- Variables match between .uxm and .md
- Accessibility requirements
- Dimension constraints

### Step 4: Report Success

**For SINGLE component**, present the results:

```markdown
# Component Created ✓

## ${componentName}

**Type**: ${componentType}
**Files**:
- ./fluxwing/components/${componentId}.uxm
- ./fluxwing/components/${componentId}.md

**States**: default (created)
**Detected states**: ${detectedStates.join(', ')}

## Preview

${asciiPreview}

## Next Steps

1. Add interaction states using the component expander skill
2. Use in a screen with the screen scaffolder skill
3. View all components with the library browser skill
4. Customize: Edit files in ./fluxwing/components/
```

**For MULTIPLE components**, present a summary:

```markdown
# Components Created ✓

Created ${componentCount} components in parallel:

## submit-button (button)
**Files**:
- ./fluxwing/components/submit-button.uxm
- ./fluxwing/components/submit-button.md

**Preview**:
╭──────────────────╮
│   Submit Form    │
╰──────────────────╯

## cancel-button (button)
**Files**:
- ./fluxwing/components/cancel-button.uxm
- ./fluxwing/components/cancel-button.md

**Preview**:
┌──────────────────┐
│   Cancel         │
└──────────────────┘

## email-input (input)
**Files**:
- ./fluxwing/components/email-input.uxm
- ./fluxwing/components/email-input.md

**Preview**:
┌────────────────────────────┐
│ Email: [________________]  │
└────────────────────────────┘

---

**Total**: 6 files created (3 .uxm + 3 .md)
**Performance**: Created in parallel (~3x faster than sequential)

## Next Steps

1. Add interaction states to components
2. Use components in screens
3. View all components
4. Customize: Edit files in ./fluxwing/components/
```

## Example Interactions

### Example 1: Single Component

```
User: Create a submit button

Skill: I'll create a submit button component! Let me check for similar templates...

[Checks bundled templates]

I found a primary-button template. Would you like me to:
1. Base it on the primary-button template (faster)
2. Create a custom design from scratch

[User responds: custom, rounded corners, filled]

Perfect! Creating submit-button component with the designer agent...

[Spawns designer agent]

✓ Component created successfully!

Files:
- ./fluxwing/components/submit-button.uxm
- ./fluxwing/components/submit-button.md

Preview (default state):
╭──────────────────╮
│   Submit Form    │
╰──────────────────╯

Next steps:
- Add states: Ask me to "add hover state to submit-button"
- Use in screen: Ask me to "create a login screen"
```

### Example 2: Multiple Components (Parallel)

```
User: Create submit-button, cancel-button, and email-input

Skill: I'll create all 3 components in parallel! This will be much faster.

Based on the component types, I'll use these defaults:
- submit-button: button type, rounded, filled style
- cancel-button: button type, rounded, outlined style
- email-input: input type, light border, minimal style

[Spawns 3 designer agents in a SINGLE message]

✓ All 3 components created successfully in parallel!

## submit-button (button)
Files: submit-button.uxm + submit-button.md

## cancel-button (button)
Files: cancel-button.uxm + cancel-button.md

## email-input (input)
Files: email-input.uxm + email-input.md

Total: 6 files created
Performance: ~3x faster than sequential creation

Next steps:
- Add states to components
- Use in a screen
- View all components
```

## Benefits of Using Designer Agent

- **Consistent quality**: Agent follows quality standards
- **Complete metadata**: Proper tags, descriptions, accessibility
- **Best practices**: Schema compliance, naming conventions
- **Reusable logic**: Same creation workflow across all skills
- **Parallel execution**: Multiple components created simultaneously (not sequentially)

## Performance Benefits

**Single vs Multi-Component Creation:**

- **Sequential (old)**: Component 1 → wait → Component 2 → wait → Component 3
  - Time: 3 × agent_time

- **Parallel (new)**: Component 1 + Component 2 + Component 3 → all at once
  - Time: 1 × agent_time (3x faster!)

**When to use multi-component creation:**
- Creating multiple components for a single screen (e.g., login form components)
- Building a component library in bulk
- Prototyping quickly with several variations

**Example speedup:**
- 1 component: ~30 seconds
- 3 components sequential: ~90 seconds
- 3 components parallel: ~30 seconds (3x faster!) ⚡

## Error Handling

**If single designer agent fails:**
- Report specific error from agent
- Suggest fixes or alternatives
- User can retry with adjusted requirements

**If multiple designer agents fail:**
- Report which components succeeded and which failed
- Keep successfully created components (partial success is OK)
- User can retry failed components individually or as a group

**Example partial failure:**
```
✓ submit-button created successfully
✓ cancel-button created successfully
✗ email-input failed: Invalid component type specified

2 of 3 components created. You can:
1. Retry email-input with corrected parameters
2. Use the 2 successful components as-is
3. Manually create email-input
```

## Success Criteria

**For single component:**
- ✓ Designer agent created component successfully
- ✓ Both .uxm and .md files exist in ./fluxwing/components/
- ✓ Component follows uxscii standard
- ✓ User can immediately use or expand the component

**For multiple components:**
- ✓ All designer agents launched in parallel (single message)
- ✓ Each component has both .uxm and .md files in ./fluxwing/components/
- ✓ All components follow uxscii standard
- ✓ Clear report showing which succeeded/failed (if any failures)
- ✓ User can immediately use all successful components

You are helping build AI-native designs with production-quality components at maximum speed!
