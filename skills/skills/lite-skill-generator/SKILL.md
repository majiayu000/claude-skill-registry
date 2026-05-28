---
name: lite-skill-generator
description: Lightweight skill generator with style learning - creates simple skills using flow-based execution and style imitation. Use for quick skill scaffolding, simple workflow creation, or style-aware skill generation.
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# Lite Skill Generator

Lightweight meta-skill for rapid skill creation with intelligent style learning and flow-based execution.

## Core Concept

**Simplicity First**: Generate simple, focused skills quickly with minimal overhead. Learn from existing skills to maintain consistent style and structure.

**Progressive Disclosure**: Follow anthropics' three-layer loading principle:
1. **Metadata** - name, description, triggers (always loaded)
2. **SKILL.md** - core instructions (loaded when triggered)
3. **Bundled resources** - scripts, references, assets (loaded on demand)

## Execution Model

**3-Phase Flow**: Style Learning → Requirements Gathering → Generation

```
User Input → Phase 1: Style Analysis → Phase 2: Requirements → Phase 3: Generate → Skill Package
                ↓                            ↓                        ↓
         Learn from examples      Interactive prompts      Write files + validate
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Lite Skill Generator                          │
│                                                                  │
│  Input: Skill name, purpose, reference skills                   │
│                         ↓                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  Phase 1-3: Lightweight Pipeline                        │    │
│  │  ┌────┐ ┌────┐ ┌────┐                                  │    │
│  │  │ P1 │→│ P2 │→│ P3 │                                  │    │
│  │  │Styl│ │Req │ │Gen │                                  │    │
│  │  └────┘ └────┘ └────┘                                  │    │
│  └─────────────────────────────────────────────────────────┘    │
│                         ↓                                        │
│  Output: .claude/skills/{skill-name}/ (minimal package)         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 3-Phase Workflow

### Phase 1: Style Analysis & Learning

Analyze reference skills to extract language patterns, structural conventions, and writing style.

```javascript
// Phase 1 Execution Flow
async function analyzeStyle(referencePaths) {
  // Step 1: Load reference skills
  const references = [];
  for (const path of referencePaths) {
    const content = Read(path);
    references.push({
      path: path,
      content: content,
      metadata: extractYAMLFrontmatter(content)
    });
  }

  // Step 2: Extract style patterns
  const styleProfile = {
    // Structural patterns
    structure: {
      hasFrontmatter: references.every(r => r.metadata !== null),
      sectionHeaders: extractCommonSections(references),
      codeBlockUsage: detectCodeBlockPatterns(references),
      flowDiagramUsage: detectFlowDiagrams(references)
    },

    // Language patterns
    language: {
      instructionStyle: detectInstructionStyle(references), // 'imperative' | 'declarative' | 'procedural'
      pseudocodeUsage: detectPseudocodePatterns(references),
      verbosity: calculateVerbosityLevel(references),      // 'concise' | 'detailed' | 'verbose'
      terminology: extractCommonTerms(references)
    },

    // Organization patterns
    organization: {
      phaseStructure: detectPhasePattern(references),      // 'sequential' | 'autonomous' | 'flat'
      exampleDensity: calculateExampleRatio(references),
      templateUsage: detectTemplateReferences(references)
    }
  };

  // Step 3: Generate style guide
  return {
    profile: styleProfile,
    recommendations: generateStyleRecommendations(styleProfile),
    examples: extractStyleExamples(references, styleProfile)
  };
}

// Structural pattern detection
function extractCommonSections(references) {
  const allSections = references.map(r =>
    r.content.match(/^##? (.+)$/gm)?.map(s => s.replace(/^##? /, ''))
  ).flat();
  return findMostCommon(allSections);
}

// Language style detection
function detectInstructionStyle(references) {
  const imperativePattern = /^(Use|Execute|Run|Call|Create|Generate)\s/gim;
  const declarativePattern = /^(The|This|Each|All)\s.*\s(is|are|will be)\s/gim;
  const proceduralPattern = /^(Step \d+|Phase \d+|First|Then|Finally)\s/gim;

  const scores = references.map(r => ({
    imperative: (r.content.match(imperativePattern) || []).length,
    declarative: (r.content.match(declarativePattern) || []).length,
    procedural: (r.content.match(proceduralPattern) || []).length
  }));

  return getMaxStyle(scores);
}

// Pseudocode pattern detection
function detectPseudocodePatterns(references) {
  const hasJavaScriptBlocks = references.some(r => r.content.includes('```javascript'));
  const hasFunctionDefs = references.some(r => /function\s+\w+\(/m.test(r.content));
  const hasFlowComments = references.some(r => /\/\/.*→/m.test(r.content));

  return {
    usePseudocode: hasJavaScriptBlocks && hasFunctionDefs,
    flowAnnotations: hasFlowComments,
    style: hasFunctionDefs ? 'functional' : 'imperative'
  };
}
```

**Output**:
```
Style Analysis Complete:
  Structure: Flow-based with pseudocode
  Language: Procedural, detailed
  Organization: Sequential phases
  Key Patterns: 3-5 phases, function definitions, ASCII diagrams

Recommendations:
  ✓ Use phase-based structure (3-4 phases)
  ✓ Include pseudocode for complex logic
  ✓ Add ASCII flow diagrams
  ✓ Maintain concise documentation style
```

---

### Phase 2: Requirements Gathering

Interactive discovery of skill requirements using learned style patterns.

```javascript
async function gatherRequirements(styleProfile) {
  // Step 1: Basic information
  const basicInfo = await AskUserQuestion({
    questions: [
      {
        question: "What is the skill name? (kebab-case, e.g., 'pdf-generator')",
        header: "Name",
        options: [
          { label: "pdf-generator", description: "Example: PDF generation skill" },
          { label: "code-analyzer", description: "Example: Code analysis skill" },
          { label: "Custom", description: "Enter custom name" }
        ]
      },
      {
        question: "What is the primary purpose?",
        header: "Purpose",
        options: [
          { label: "Generation", description: "Create/generate artifacts" },
          { label: "Analysis", description: "Analyze/inspect code or data" },
          { label: "Transformation", description: "Convert/transform content" },
          { label: "Orchestration", description: "Coordinate multiple operations" }
        ]
      }
    ]
  });

  // Step 2: Execution complexity
  const complexity = await AskUserQuestion({
    questions: [{
      question: "How many main steps does this skill need?",
      header: "Steps",
      options: [
        { label: "2-3 steps", description: "Simple workflow (recommended for lite-skill)" },
        { label: "4-5 steps", description: "Moderate workflow" },
        { label: "6+ steps", description: "Complex workflow (consider full skill-generator)" }
      ]
    }]
  });

  // Step 3: Tool requirements
  const tools = await AskUserQuestion({
    questions: [{
      question: "Which tools will this skill use? (select multiple)",
      header: "Tools",
      multiSelect: true,
      options: [
        { label: "Read", description: "Read files" },
        { label: "Write", description: "Write files" },
        { label: "Bash", description: "Execute commands" },
        { label: "Task", description: "Launch agents" },
        { label: "AskUserQuestion", description: "Interactive prompts" }
      ]
    }]
  });

  // Step 4: Output format
  const output = await AskUserQuestion({
    questions: [{
      question: "What does this skill produce?",
      header: "Output",
      options: [
        { label: "Single file", description: "One main output file" },
        { label: "Multiple files", description: "Several related files" },
        { label: "Directory structure", description: "Complete directory tree" },
        { label: "Modified files", description: "Edits to existing files" }
      ]
    }]
  });

  // Step 5: Build configuration
  return {
    name: basicInfo.Name,
    purpose: basicInfo.Purpose,
    description: generateDescription(basicInfo.Name, basicInfo.Purpose),
    steps: parseStepCount(complexity.Steps),
    allowedTools: tools.Tools,
    outputType: output.Output,
    styleProfile: styleProfile,
    triggerPhrases: generateTriggerPhrases(basicInfo.Name, basicInfo.Purpose)
  };
}

// Generate skill description from name and purpose
function generateDescription(name, purpose) {
  const templates = {
    Generation: `Generate ${humanize(name)} with intelligent scaffolding`,
    Analysis: `Analyze ${humanize(name)} with detailed reporting`,
    Transformation: `Transform ${humanize(name)} with format conversion`,
    Orchestration: `Orchestrate ${humanize(name)} workflow with multi-step coordination`
  };
  return templates[purpose] || `${humanize(name)} skill for ${purpose.toLowerCase()} tasks`;
}

// Generate trigger phrases
function generateTriggerPhrases(name, purpose) {
  const base = [name, name.replace(/-/g, ' ')];
  const purposeVariants = {
    Generation: ['generate', 'create', 'build'],
    Analysis: ['analyze', 'inspect', 'review'],
    Transformation: ['transform', 'convert', 'format'],
    Orchestration: ['orchestrate', 'coordinate', 'manage']
  };
  return [...base, ...purposeVariants[purpose].map(v => `${v} ${humanize(name)}`)];
}
```

**Display to User**:
```
Requirements Gathered:
  Name: pdf-generator
  Purpose: Generation
  Steps: 3 (Setup → Generate → Validate)
  Tools: Read, Write, Bash
  Output: Single file (PDF document)
  Triggers: "pdf-generator", "generate pdf", "create pdf"

Style Application:
  Using flow-based structure (from style analysis)
  Including pseudocode blocks
  Adding ASCII diagrams for clarity
```

---

### Phase 3: Generate Skill Package

Create minimal skill structure with style-aware content generation.

```javascript
async function generateSkillPackage(requirements) {
  const skillDir = `.claude/skills/${requirements.name}`;
  const workDir = `.workflow/.scratchpad/lite-skill-gen-${Date.now()}`;

  // Step 1: Create directory structure
  Bash(`mkdir -p "${skillDir}" "${workDir}"`);

  // Step 2: Generate SKILL.md (using learned style)
  const skillContent = generateSkillMd(requirements);
  Write(`${skillDir}/SKILL.md`, skillContent);

  // Step 3: Conditionally add bundled resources
  if (requirements.outputType === 'Directory structure') {
    Bash(`mkdir -p "${skillDir}/templates"`);
    const templateContent = generateTemplate(requirements);
    Write(`${skillDir}/templates/base-template.md`, templateContent);
  }

  if (requirements.allowedTools.includes('Bash')) {
    Bash(`mkdir -p "${skillDir}/scripts"`);
    const scriptContent = generateScript(requirements);
    Write(`${skillDir}/scripts/helper.sh`, scriptContent);
  }

  // Step 4: Generate README
  const readmeContent = generateReadme(requirements);
  Write(`${skillDir}/README.md`, readmeContent);

  // Step 5: Validate structure
  const validation = validateSkillStructure(skillDir, requirements);
  Write(`${workDir}/validation-report.json`, JSON.stringify(validation, null, 2));

  // Step 6: Return summary
  return {
    skillPath: skillDir,
    filesCreated: [
      `${skillDir}/SKILL.md`,
      ...(validation.hasTemplates ? [`${skillDir}/templates/`] : []),
      ...(validation.hasScripts ? [`${skillDir}/scripts/`] : []),
      `${skillDir}/README.md`
    ],
    validation: validation,
    nextSteps: generateNextSteps(requirements)
  };
}

// Generate SKILL.md with style awareness
function generateSkillMd(req) {
  const { styleProfile } = req;

  // YAML frontmatter
  const frontmatter = `---
name: ${req.name}
description: ${req.description}
allowed-tools: ${req.allowedTools.join(', ')}
---
`;

  // Main content structure (adapts to style)
  let content = frontmatter;

  content += `\n# ${humanize(req.name)}\n\n`;
  content += `${req.description}\n\n`;

  // Add architecture diagram if style uses them
  if (styleProfile.structure.flowDiagramUsage) {
    content += generateArchitectureDiagram(req);
  }

  // Add execution flow
  content += `## Execution Flow\n\n`;
  if (styleProfile.language.pseudocodeUsage.usePseudocode) {
    content += generatePseudocodeFlow(req);
  } else {
    content += generateProceduralFlow(req);
  }

  // Add phase sections
  for (let i = 0; i < req.steps; i++) {
    content += generatePhaseSection(i + 1, req, styleProfile);
  }

  // Add examples if style is verbose
  if (styleProfile.language.verbosity !== 'concise') {
    content += generateExamplesSection(req);
  }

  return content;
}

// Generate architecture diagram
function generateArchitectureDiagram(req) {
  return `## Architecture
\`\`\`
┌─────────────────────────────────────────────────┐
│               ${humanize(req.name)}              │
│                                                 │
│  Input → Phase 1 → Phase 2 → Phase 3 → Output  │
│          ${getPhaseName(1, req)}                 │
│          ${getPhaseName(2, req)}                 │
│          ${getPhaseName(3, req)}                 │
└─────────────────────────────────────────────────┘
\`\`\`

`;
}

// Generate pseudocode flow
function generatePseudocodeFlow(req) {
  return `\`\`\`javascript
async function ${toCamelCase(req.name)}(input) {
  // Phase 1: ${getPhaseName(1, req)}
  const prepared = await phase1Prepare(input);

  // Phase 2: ${getPhaseName(2, req)}
  const processed = await phase2Process(prepared);

  // Phase 3: ${getPhaseName(3, req)}
  const result = await phase3Finalize(processed);

  return result;
}
\`\`\`

`;
}

// Generate phase section
function generatePhaseSection(phaseNum, req, styleProfile) {
  const phaseName = getPhaseName(phaseNum, req);

  let section = `### Phase ${phaseNum}: ${phaseName}\n\n`;

  if (styleProfile.language.pseudocodeUsage.usePseudocode) {
    section += `\`\`\`javascript\n`;
    section += `async function phase${phaseNum}${toCamelCase(phaseName)}(input) {\n`;
    section += `  // TODO: Implement ${phaseName.toLowerCase()} logic\n`;
    section += `  return output;\n`;
    section += `}\n\`\`\`\n\n`;
  } else {
    section += `**Steps**:\n`;
    section += `1. Load input data\n`;
    section += `2. Process according to ${phaseName.toLowerCase()} logic\n`;
    section += `3. Return result to next phase\n\n`;
  }

  return section;
}

// Validation
function validateSkillStructure(skillDir, req) {
  const requiredFiles = [`${skillDir}/SKILL.md`, `${skillDir}/README.md`];
  const exists = requiredFiles.map(f => Bash(`test -f "${f}"`).exitCode === 0);

  return {
    valid: exists.every(e => e),
    hasTemplates: Bash(`test -d "${skillDir}/templates"`).exitCode === 0,
    hasScripts: Bash(`test -d "${skillDir}/scripts"`).exitCode === 0,
    filesPresent: requiredFiles.filter((f, i) => exists[i]),
    styleCompliance: checkStyleCompliance(skillDir, req.styleProfile)
  };
}
```

**Output**:
```
Skill Package Generated:
  Location: .claude/skills/pdf-generator/

Structure:
  ✓ SKILL.md (entry point)
  ✓ README.md (usage guide)
  ✓ templates/ (directory templates)
  ✓ scripts/ (helper scripts)

Validation:
  ✓ All required files present
  ✓ Style compliance: 95%
  ✓ Frontmatter valid
  ✓ Tool references correct

Next Steps:
  1. Review SKILL.md and customize phases
  2. Test skill: /skill:pdf-generator "test input"
  3. Iterate based on usage
```

---

## Complete Execution Flow

```
User: "Create a PDF generator skill"
    ↓
Phase 1: Style Analysis
    |-- Read reference skills (ccw.md, ccw-coordinator.md)
    |-- Extract style patterns (flow diagrams, pseudocode, structure)
    |-- Generate style profile
    +-- Output: Style recommendations
    ↓
Phase 2: Requirements
    |-- Ask: Name, purpose, steps
    |-- Ask: Tools, output format
    |-- Generate: Description, triggers
    +-- Output: Requirements config
    ↓
Phase 3: Generation
    |-- Create: Directory structure
    |-- Write: SKILL.md (style-aware)
    |-- Write: README.md
    |-- Optionally: templates/, scripts/
    |-- Validate: Structure and style
    +-- Output: Skill package
    ↓
Return: Skill location + next steps
```

## Phase Execution Protocol

```javascript
// Main entry point
async function liteSkillGenerator(input) {
  // Phase 1: Style Learning
  const references = [
    '.claude/commands/ccw.md',
    '.claude/commands/ccw-coordinator.md',
    ...discoverReferenceSkills(input)
  ];
  const styleProfile = await analyzeStyle(references);
  console.log(`Style Analysis: ${styleProfile.organization.phaseStructure}, ${styleProfile.language.verbosity}`);

  // Phase 2: Requirements
  const requirements = await gatherRequirements(styleProfile);
  console.log(`Requirements: ${requirements.name} (${requirements.steps} phases)`);

  // Phase 3: Generation
  const result = await generateSkillPackage(requirements);
  console.log(`✅ Generated: ${result.skillPath}`);

  return result;
}
```

## Output Structure

**Minimal Package** (default):
```
.claude/skills/{skill-name}/
├── SKILL.md                # Entry point with frontmatter
└── README.md               # Usage guide
```

**With Templates** (if needed):
```
.claude/skills/{skill-name}/
├── SKILL.md
├── README.md
└── templates/
    └── base-template.md
```

**With Scripts** (if using Bash):
```
.claude/skills/{skill-name}/
├── SKILL.md
├── README.md
└── scripts/
    └── helper.sh
```

## Key Design Principles

1. **Style Learning** - Analyze reference skills to maintain consistency
2. **Minimal Overhead** - Generate only essential files (SKILL.md + README)
3. **Progressive Disclosure** - Follow anthropics' three-layer loading
4. **Flow-Based** - Use pseudocode and flow diagrams (when style appropriate)
5. **Interactive** - Guided requirements gathering via AskUserQuestion
6. **Fast Generation** - 3 phases instead of 6, focused on simplicity
7. **Style Awareness** - Adapt output based on detected patterns

## Style Pattern Detection

**Structural Patterns**:
- YAML frontmatter usage (100% in references)
- Section headers (H2 for major, H3 for sub-sections)
- Code blocks (JavaScript pseudocode, Bash examples)
- ASCII diagrams (architecture, flow charts)

**Language Patterns**:
- Instruction style: Procedural with function definitions
- Pseudocode: JavaScript-based with flow annotations
- Verbosity: Detailed but focused
- Terminology: Phase, workflow, pipeline, orchestrator

**Organization Patterns**:
- Phase structure: 3-5 sequential phases
- Example density: Moderate (1-2 per major section)
- Template usage: Minimal (only when necessary)

## Usage Examples

**Basic Generation**:
```
User: "Create a markdown formatter skill"
Lite-Skill-Generator:
  → Analyzes ccw.md style
  → Asks: Name? "markdown-formatter"
  → Asks: Purpose? "Transformation"
  → Asks: Steps? "3 steps"
  → Generates: .claude/skills/markdown-formatter/
```

**With Custom References**:
```
User: "Create a skill like software-manual but simpler"
Lite-Skill-Generator:
  → Analyzes software-manual skill
  → Learns: Multi-phase, agent-based, template-heavy
  → Simplifies: 3 phases, direct execution, minimal templates
  → Generates: Simplified version
```

## Comparison: lite-skill-generator vs skill-generator

| Aspect | lite-skill-generator | skill-generator |
|--------|---------------------|-----------------|
| **Phases** | 3 (Style → Req → Gen) | 6 (Spec → Req → Dir → Gen → Specs → Val) |
| **Style Learning** | Yes (analyze references) | No (fixed templates) |
| **Complexity** | Simple skills only | Full-featured skills |
| **Output** | Minimal (SKILL.md + README) | Complete (phases/, specs/, templates/) |
| **Generation Time** | Fast (~2 min) | Thorough (~10 min) |
| **Use Case** | Quick scaffolding | Production-ready skills |

## Workflow Integration

**Standalone**:
```bash
/skill:lite-skill-generator "Create a log analyzer skill"
```

**With References**:
```bash
/skill:lite-skill-generator "Create a skill based on ccw-coordinator.md style"
```

**Batch Generation** (for multiple simple skills):
```bash
/skill:lite-skill-generator "Create 3 skills: json-validator, yaml-parser, toml-converter"
```

---

**Next Steps After Generation**:
1. Review `.claude/skills/{name}/SKILL.md`
2. Customize phase logic for your use case
3. Add examples to README.md
4. Test skill with sample input
5. Iterate based on real usage
