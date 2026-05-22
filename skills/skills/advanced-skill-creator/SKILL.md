---
name: advanced-skill-creator
description: >
  Meta-skill that generates domain-specific skills using advanced reasoning techniques.
  PROACTIVELY activate for: (1) Create/build/make skills, (2) Generate expert panels
  for any domain, (3) Design evaluation frameworks, (4) Create research workflows,
  (5) Structure complex multi-step processes, (6) Instantiate templates with parameters.
  
  Triggers: "create a skill for", "build evaluation for", "design workflow for",
  "generate expert panel for", "how should I approach [complex task]", "create skill",
  "new skill for", "skill template", "generate skill"
---

# Advanced Skill Creator

Generate domain-specific skills and workflows using advanced reasoning techniques.

## Purpose

This meta-skill orchestrates skill generation by:
1. Analyzing task requirements
2. Selecting appropriate patterns from the library
3. Instantiating templates with domain parameters
4. Generating executable SKILL.md files or portable prompts

## Core Libraries

This skill has access to (load on demand):
- `@core/technique-taxonomy.yaml` — 200+ techniques across 6 cognitive categories
- `@core/artifact-contracts.yaml` — Standardized I/O schemas
- `@core/scoring-rubrics.yaml` — Pluggable evaluation algorithms
- `@core/skill-patterns.yaml` — Parameterized workflow patterns
- `@core/checkpoint-patterns.yaml` — AskUserQuestion checkpoint patterns

## Checkpoints

This skill uses interactive checkpoints (see `references/checkpoints.yaml`) to resolve ambiguity:
- **task_type_classification** — When request matches multiple patterns
- **domain_selection** — When domain not specified
- **stakeholder_selection** — When multiple stakeholder types could apply
- **preset_conflict** — When user params conflict with presets
- **anti_pattern_composition** — When composition matches known anti-pattern
- **output_mode** — When output format not specified
- **plugin_routing** — When skill could belong to multiple plugins

## Available Templates

| Template | Use Case | Key Parameters |
|----------|----------|----------------|
| `expert-panel` | Multi-perspective evaluation | domain, panel_size, goal |
| `tournament-ranking` | Pairwise comparison | items, criteria, algorithm |
| `adversarial-validation` | Red/blue team analysis | proposition, attack_vectors |
| `research-brief` | Multi-LLM research design | domain, models, depth |
| `gap-audit` | Completeness assessment | document, standards |
| `jtbd-extraction` | Job story generation | features, persona |
| `user-flow-mapping` | Journey documentation | process, touchpoints |
| `feature-extraction` | Identify features | context, granularity |
| `diataxis-documentation` | Generate docs | doc_type, audience |

## Workflow

### Phase 1: Requirements Analysis

When asked to create a skill or workflow:

1. **Identify the core task type:**
   - Evaluation/Comparison → Use MOE-EVALUATE or TOURNAMENT patterns
   - Generation/Ideation → Use MOE-GENERATE pattern
   - Validation/Testing → Use ADVERSARIAL-VALIDATE pattern
   - Research/Discovery → Use RESEARCH-SYNTHESIZE pattern
   - Documentation → Use DIATAXIS pattern
   - Extraction → Use ELICIT-EXTRACT pattern

2. **CHECKPOINT: task_type_classification**
   - If request matches multiple patterns (confidence < 0.7): **AskUserQuestion**
   - Present top 2-3 matching patterns with descriptions
   - Example: "Should this skill evaluate existing options or generate new ones?"

3. **Determine parameters needed:**
   - Domain/context
   - Stakeholders
   - Quality dimensions
   - Output format

4. **CHECKPOINT: domain_selection**
   - If domain not specified and not inferable: **AskUserQuestion**
   - Options: Architecture, Product, Strategy, Research, Custom
   - Example: "What domain is this skill for?"

5. **Check for existing skills that might compose:**
   - Can we chain existing skills?
   - What's missing that requires new skill?

### Phase 2: Pattern Selection

Load `@core/skill-patterns.yaml` and select pattern based on:

| Task Type | Pattern | When to Use |
|-----------|---------|-------------|
| Compare options | MOE-EVALUATE | 2-8 options, need expert perspectives |
| Rank many items | TOURNAMENT-RANK | >5 items, need statistical ranking |
| Generate ideas | MOE-GENERATE | Need diverse, expert-informed ideas |
| Stress-test decision | ADVERSARIAL-VALIDATE | High-stakes, need to find weaknesses |
| Synthesize research | RESEARCH-SYNTHESIZE | Multiple sources to reconcile |
| Check completeness | GAP-AUDIT | Document against standards |
| Extract requirements | ELICIT-EXTRACT | Unstructured → structured |

### Phase 3: Template Instantiation

Based on selected pattern, configure template:
```yaml
skill_instantiation:
  pattern: "[selected pattern]"
  domain: "[user's domain]"
  parameters:
    # Pattern-specific parameters
  techniques:
    # Selected from technique-taxonomy
  output_contract:
    # From artifact-contracts
```

1. **CHECKPOINT: preset_conflict**
   - If user params conflict with domain preset: **AskUserQuestion**
   - Example: "You specified 6 experts, but 'product' preset uses 4. Which should we use?"

2. **CHECKPOINT: anti_pattern_composition**
   - If composition matches anti-pattern: **AskUserQuestion**
   - Warn about the issue and offer alternatives
   - Example: "Chaining ADVERSARIAL-VALIDATE → ADVERSARIAL-VALIDATE creates infinite loops"

### Phase 4: Output Generation

1. **CHECKPOINT: output_mode**
   - If output format not specified: **AskUserQuestion**
   - Options: Executable SKILL.md, Portable prompt, Both
   - Example: "Should this be an executable skill or a portable prompt?"

Generate one of:

**A. Executable Skill (SKILL.md)**
- Complete frontmatter with triggers
- Full workflow instructions
- Quality gates
- Output templates

**B. Portable Prompt**
- Standalone prompt for other contexts
- Self-contained instructions
- No skill dependencies

**→ Proceed to Phase 5 to save the skill in the correct location.**

### Phase 5: Skill Placement

Generated skills MUST be placed in the correct plugin directory for marketplace visibility:

1. **Determine target plugin based on skill type:**

   | Skill Type | Target Plugin |
   |------------|---------------|
   | Evaluation/Comparison | `evaluation-tools` |
   | Research/Discovery | `research-tools` |
   | Documentation | `documentation-tools` |
   | Prompt optimization | `prompt-tools` |
   | Skill generation/Meta | `meta-tools` |

2. **CHECKPOINT: plugin_routing**
   - If skill matches criteria for 2+ plugins: **AskUserQuestion**
   - Example: "This skill audits documentation. Should it go in evaluation-tools or documentation-tools?"

3. **Create the skill directory structure:**
   ```
   plugins/<target-plugin>/skills/<skill-name>/
   ├── SKILL.md              ← Main skill definition (required)
   ├── references/           ← Supporting reference docs (optional)
   └── templates/            ← Output templates (optional)
   ```

4. **File naming conventions:**
   - Skill directory: kebab-case (e.g., `architecture-evaluator`)
   - SKILL.md: Required, exact filename
   - References: descriptive kebab-case (e.g., `scoring-criteria.md`)

**Important:** Skills saved outside `plugins/<plugin>/skills/` will NOT appear in the marketplace.

## Output Templates

### Skill Output Template
```markdown
---
name: [skill-name]
description: >
  [Description with PROACTIVELY activate for: (1)..., (2)..., (3)...]
  Triggers: "[trigger phrases]"
---

# [Skill Name]

[One-line purpose]

## When to Use

[Ideal use cases and anti-patterns]

## Workflow

### Step 1: [First Step]
[Instructions]

### Step 2: [Second Step]
[Instructions]

## Parameters

| Parameter | Default | Options | Description |
|-----------|---------|---------|-------------|

## Output Format

[Expected output structure]

## Quality Gates

- [ ] [Gate 1]
- [ ] [Gate 2]

## Examples

[Example invocations and outputs]
```

## Quality Gates

Before completing skill generation:

- [ ] Pattern selection rationale documented
- [ ] All required parameters configured
- [ ] Technique provenance traced (which techniques from taxonomy)
- [ ] Output contract specified (from artifact-contracts)
- [ ] Triggers are specific and actionable
- [ ] Description includes numbered use cases
- [ ] Target plugin identified and skill saved to `plugins/<plugin>/skills/<skill-name>/`
- [ ] All applicable checkpoints evaluated (ambiguity resolved via AskUserQuestion)

## Examples

**Example 1: Create evaluation skill**
User: Create a skill for evaluating architecture proposals
Advanced Skill Creator:
→ Task type: Evaluation/Comparison
→ Pattern: MOE-EVALUATE
→ Domain: Architecture
→ Generate: architecture-evaluator skill with:

Technical Authority, Quality Guardian, Risk Specialist experts
Criteria: scalability, maintainability, cost, security
Output: RANKED-SOLUTION-LIST contract


**Example 2: Create research workflow**
User: Build a workflow for competitive analysis
Advanced Skill Creator:
→ Task type: Research/Discovery
→ Pattern: RESEARCH-SYNTHESIZE
→ Domain: Competitive intelligence
→ Generate: competitive-analyzer skill with:

Research brief generation (Claude + Gemini)
Consolidation workflow
Gap identification

