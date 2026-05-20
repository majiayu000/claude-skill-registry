---
name: skill-builder-generic
description: Universal guide for creating production-ready Claude Code skills for any project. Includes 6-step workflow (understand, plan, initialize, edit, package, iterate), progressive disclosure design, YAML frontmatter templates, validation scripts, reference organization patterns, and 10 community-proven innovations. Use when creating new Claude Code skills, converting documentation to skills, improving existing skills, or learning skill development best practices for any domain.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Universal Claude Code Skill Builder

## Philosophy & Overview

### What Are Claude Code Skills?

Skills are structured knowledge packages that extend Claude Code's capabilities for specific domains. They follow a standardized format:
- YAML frontmatter for metadata
- Markdown content for instructions
- Progressive disclosure for context optimization
- Optional references/, scripts/, and assets/ for bundled resources

### Why Skills Matter

**Without Skills**: Every task requires full context in conversation, repeated explanations, and no knowledge persistence across sessions.

**With Skills**: Domain knowledge is packaged once, invoked by name, loaded progressively, and reused across all projects.

### When to Create Skills

Create skills when:
- You have domain-specific knowledge to capture (design systems, API patterns, deployment workflows)
- You repeat similar instructions frequently (testing patterns, code review standards)
- You want to share knowledge with team or community
- You need consistent execution of complex workflows

Don't create skills when:
- Information is one-time use
- Task is better suited for inline conversation
- Knowledge changes too rapidly to maintain

### Core Principles

**Progressive Disclosure**: Keep SKILL.md lean, bundle details in references/
- SKILL.md: Always loaded (overview, quick start, key workflows)
- references/: Loaded on-demand (comprehensive guides, deep details)
- scripts/: Loaded when execution needed (automation, validation)

**Imperative/Infinitive Voice**: Write action-oriented instructions
- Good: "Create skill structure using workflow pattern"
- Bad: "You should probably think about creating a skill structure"

**Trigger Keywords**: Include discoverable terms in description
- Include: Task verbs (create, build, validate), domain terms (FHIR, deployment, testing)
- Context: Where skill applies (medical integration, API design, code review)

---

## 6-Step Creation Process

### Step 1: Understand Requirements

**Objective**: Clearly define what the skill should accomplish

**Questions to Answer**:
- What problem does this skill solve?
- Who will use this skill? (You, team, community)
- What domain knowledge must be captured?
- What workflows need to be documented?
- Are there existing skills to reference or patterns to follow?

**Output**: Clear problem statement and scope definition

**Example**:
```
Problem: Developers waste time figuring out Railway deployment for each project
Scope: Document Railway deployment workflow for Node.js + React apps
Users: Development team
Domain: Deployment, Railway, Docker, environment configuration
Patterns: Workflow-based (sequential steps)
```

**References**: See [references/converting-docs-to-skills.md](references/converting-docs-to-skills.md) for converting existing documentation

---

### Step 2: Plan Structure

**Objective**: Choose organizational pattern and plan file structure

**Choose Organizational Pattern** (see [4 Organizational Patterns](#4-organizational-patterns)):

1. **Workflow-based**: Sequential processes with clear steps
   - Use when: Deployment, API integration, testing workflows
   - Structure: Step 1 → Step 2 → Step 3 → Result

2. **Task-based**: Independent operations without order dependency
   - Use when: Utilities, troubleshooting guides, debugging
   - Structure: Task A, Task B, Task C (any order)

3. **Reference/Guidelines**: Standards, patterns, design systems
   - Use when: Design systems, coding standards, style guides
   - Structure: Concepts, guidelines, examples

4. **Capabilities-based**: Integrated feature suites with multiple entry points
   - Use when: Complex systems, multiple related workflows
   - Structure: Feature A, Feature B, Feature C (interconnected)

**Plan File Structure**:
```
skill-name/
├── SKILL.md (always)
├── references/ (if detailed guides needed)
│   ├── detailed-guide-1.md
│   └── detailed-guide-2.md
├── scripts/ (if automation needed)
│   └── helper-script.py
└── templates/ (if reusable patterns)
    └── template-file.md
```

**Progressive Disclosure Planning**:
- SKILL.md: <5,000 words (overview, quick start, key workflows)
- references/: Comprehensive details, long guides (10,000+ words okay)
- scripts/: Automation helpers (documented with --help)

**Output**: Organizational pattern chosen, file structure planned

**References**: See [references/reference-organization-strategies.md](references/reference-organization-strategies.md) for detailed planning

---

### Step 3: Initialize Skill

**Objective**: Create directory structure and scaffold files

**Manual Approach**:
```bash
# Create skill directory
mkdir -p .claude/skills/skill-name

# Create SKILL.md with frontmatter
cat > .claude/skills/skill-name/SKILL.md <<'EOF'
---
name: skill-name
description: [What it does]. Use when [triggers].
---

# Skill Name

## Overview
[Purpose in 1-2 sentences]

## Quick Start
[Basic usage]
EOF

# Create subdirectories if needed
mkdir -p .claude/skills/skill-name/references
mkdir -p .claude/skills/skill-name/scripts
```

**Automated Approach** (using scripts):
```bash
# Initialize with template
python scripts/init-skill.py skill-name --template workflow

# Initialize interactively
python scripts/init-skill.py skill-name --interactive
```

**YAML Frontmatter Template**:
```yaml
---
name: skill-name-in-hyphen-case
description: [What skill does in 1-2 sentences]. [Key features]. Use when [trigger scenarios with keywords].
---
```

**Description Formula**: What + Features + Triggers
- What: Primary purpose (1 sentence)
- Features: Key capabilities (optional, 1 sentence)
- Triggers: When to use with discoverable keywords (1 sentence)

**Output**: Directory structure created, SKILL.md scaffolded

**References**: See [references/yaml-frontmatter-complete-guide.md](references/yaml-frontmatter-complete-guide.md) for YAML details

---

### Step 4: Edit Content

**Objective**: Write comprehensive skill documentation

**SKILL.md Structure** (Workflow-based example):
```markdown
---
name: deployment-guide
description: Railway deployment workflow for Node.js + React apps...
---

# Deployment Guide

## Overview
Complete Railway deployment workflow for full-stack applications.

## Prerequisites
- Railway account
- GitHub repository
- Node.js project

## Workflow

### Step 1: Prepare Application
[Instructions]

### Step 2: Configure Railway
[Instructions]

### Step 3: Deploy
[Instructions]

### Step 4: Verify
[Instructions]

## Troubleshooting
Common issues and solutions. See [references/troubleshooting-guide.md](references/troubleshooting-guide.md) for comprehensive guide.

## References
- [Environment Configuration](references/environment-config.md)
- [Deployment Checklist](references/deployment-checklist.md)
```

**Writing Guidelines**:

1. **Use Imperative Voice**:
   - Good: "Configure environment variables"
   - Bad: "You should configure environment variables"

2. **Be Specific**:
   - Good: "Run `npm run build` to create production bundle"
   - Bad: "Build the application"

3. **Include Examples**:
   - Code blocks with actual examples
   - Before/after comparisons
   - Expected outputs

4. **Reference, Don't Duplicate**:
   - SKILL.md: Overview and workflow
   - references/: Detailed explanations
   - Link with: "See [references/file.md](references/file.md) for details"

**Output**: SKILL.md written, references created if needed

**References**: See [references/writing-style-imperative-guide.md](references/writing-style-imperative-guide.md) for writing standards

---

### Step 5: Package & Validate

**Objective**: Validate skill meets quality standards

**Validation Checklist**:

**YAML Frontmatter** (12 checks):
- [ ] Name in hyphen-case (no underscores, spaces, capitals)
- [ ] Description <1024 characters
- [ ] Description includes what skill does
- [ ] Description includes trigger keywords
- [ ] Description includes when to use
- [ ] Name matches directory name
- [ ] No optional fields with empty values
- [ ] Proper YAML syntax (no tabs, correct indentation)
- [ ] Description is complete sentence(s)
- [ ] Description specific (not vague)
- [ ] Trigger keywords discoverable
- [ ] Name descriptive and clear

**File Structure** (10 checks):
- [ ] SKILL.md exists and is primary file
- [ ] Directory structure clean (no unnecessary nesting)
- [ ] references/ used for detailed content (if applicable)
- [ ] scripts/ used for automation (if applicable)
- [ ] File names descriptive and consistent
- [ ] No duplicate content across files
- [ ] Cross-references working (links valid)
- [ ] Progressive disclosure followed
- [ ] Files organized logically
- [ ] No orphaned files

**Content Quality** (10 checks):
- [ ] SKILL.md <5,000 words
- [ ] Overview section clear and concise
- [ ] Quick start example included
- [ ] Imperative/infinitive voice used
- [ ] Code examples included where relevant
- [ ] No placeholder text (TODO, FIX, etc.)
- [ ] Terminology consistent
- [ ] Grammar and spelling correct
- [ ] Formatting consistent
- [ ] Content accurate and tested

**Automated Validation**:
```bash
# Validate skill structure
python scripts/validate-skill.py skill-name/

# Analyze description for trigger effectiveness
python scripts/analyze-description.py skill-name/

# Package skill for distribution
bash scripts/package-skill.sh skill-name/
```

**Output**: Skill validated, ready for use or distribution

**References**: See [references/validation-checklist-complete.md](references/validation-checklist-complete.md) for comprehensive validation

---

### Step 6: Iterate & Improve

**Objective**: Continuously improve skill based on usage

**Improvement Cycle**:

1. **Use skill in real scenarios**
   - Track what works well
   - Note confusion points
   - Identify missing information

2. **Gather feedback**
   - From team if shared
   - From own usage patterns
   - From Claude Code responses

3. **Identify improvements**
   - Add missing workflows
   - Clarify confusing sections
   - Enhance examples
   - Update for new patterns

4. **Update skill**
   - Edit SKILL.md
   - Update references
   - Add new examples
   - Re-validate

5. **Track evolution**
   - Version in git
   - Document changes
   - Share improvements

**Common Improvements**:
- Add troubleshooting section (most common)
- Include more examples (clarity)
- Expand quick start (easier onboarding)
- Reorganize for better flow (usability)
- Add scripts for automation (efficiency)

**Output**: Skill continuously improving over time

---

## Quick Start: 5-Minute Skill

Create a minimal but complete skill in 5 minutes:

### 1. Choose Name (30 seconds)
```bash
# Use hyphen-case, descriptive
my-skill-name  # Good
my_skill_name  # Bad (underscores)
MySkillName    # Bad (capitals)
```

### 2. Create Structure (1 minute)
```bash
mkdir -p .claude/skills/my-skill-name
cd .claude/skills/my-skill-name
```

### 3. Create SKILL.md (3 minutes)
```markdown
---
name: my-skill-name
description: Brief description of what skill does. Use when working on specific task or domain.
---

# My Skill Name

## Overview
One paragraph explaining purpose and value.

## Quick Start

### Basic Usage
1. First step
2. Second step
3. Third step

### Example
\`\`\`bash
# Example command or code
echo "Hello from skill"
\`\`\`

## When to Use
- Scenario 1
- Scenario 2
- Scenario 3

## References
- Link to external documentation if needed
```

### 4. Test (30 seconds)
```bash
# Test by invoking skill in Claude Code conversation
# "Use the my-skill-name skill to help with [task]"
```

### 5. Iterate
Add more content over time as you use the skill.

**Result**: Functional minimal skill in 5 minutes!

---

## 4 Organizational Patterns

### Pattern 1: Workflow-Based

**Use When**: Sequential processes with clear steps

**Structure**:
```markdown
## Workflow

### Step 1: [Action]
Instructions for step 1

### Step 2: [Action]
Instructions for step 2

### Step 3: [Action]
Instructions for step 3
```

**Examples**:
- Deployment workflows (prepare → configure → deploy → verify)
- API integration (authenticate → fetch → process → store)
- Testing workflows (setup → execute → validate → cleanup)

**Characteristics**:
- Order matters
- Each step builds on previous
- Clear progression
- Defined start and end points

**Best Practices**:
- Number steps clearly
- Include prerequisites at start
- Show expected outcomes for each step
- Provide troubleshooting per step

---

### Pattern 2: Task-Based

**Use When**: Independent operations without order dependency

**Structure**:
```markdown
## Tasks

### Task A: [Action]
Complete instructions for task A

### Task B: [Action]
Complete instructions for task B

### Task C: [Action]
Complete instructions for task C
```

**Examples**:
- Troubleshooting guides (different problems, different solutions)
- Utility collections (various independent tools)
- Command references (different operations)

**Characteristics**:
- Order doesn't matter
- Tasks are independent
- Can perform any subset
- Quick reference format

**Best Practices**:
- Make each task self-contained
- Use descriptive task names
- Include complete instructions per task
- Organize by category if many tasks

---

### Pattern 3: Reference/Guidelines

**Use When**: Standards, patterns, design systems, best practices

**Structure**:
```markdown
## Guidelines

### Guideline 1: [Concept]
Explanation and examples

### Guideline 2: [Concept]
Explanation and examples

## Reference

### Component A
Details and usage

### Component B
Details and usage
```

**Examples**:
- Design systems (colors, typography, components)
- Coding standards (style guide, patterns, conventions)
- API documentation (endpoints, parameters, responses)

**Characteristics**:
- Reference material
- Look-up format
- Examples and specifications
- Comprehensive coverage

**Best Practices**:
- Organize by category
- Include visual examples where applicable
- Provide usage examples
- Keep updated as standards evolve

---

### Pattern 4: Capabilities-Based

**Use When**: Integrated feature suites with multiple entry points

**Structure**:
```markdown
## Capabilities

### Capability A: [Feature]
How to use feature A
- Sub-feature 1
- Sub-feature 2

### Capability B: [Feature]
How to use feature B
- Sub-feature 1
- Sub-feature 2

## Integration
How capabilities work together
```

**Examples**:
- Complex systems (multiple interconnected features)
- Platforms (various ways to accomplish goals)
- Toolkits (collection of related capabilities)

**Characteristics**:
- Multiple features
- Features can be combined
- Flexible usage patterns
- Integration between features

**Best Practices**:
- Explain each capability clearly
- Show integration patterns
- Provide combination examples
- Include capability matrix

---

### Choosing the Right Pattern

**Decision Tree**:

1. **Is there a required sequence?**
   → Yes: **Workflow-based**
   → No: Go to 2

2. **Are operations independent?**
   → Yes: **Task-based**
   → No: Go to 3

3. **Is it primarily reference material?**
   → Yes: **Reference/Guidelines**
   → No: **Capabilities-based**

**Pattern Mixing**: You can combine patterns
- Primary pattern: Overall structure
- Secondary pattern: Individual sections

**Example**: Deployment skill might be:
- Primary: Workflow-based (deployment steps)
- Section: Reference (environment variables)
- Section: Task-based (troubleshooting)

---

## Progressive Disclosure Deep Dive

### The Three-Level System

**Level 1: SKILL.md** (Always Loaded)
- Size: <5,000 words ideal, <10,000 words maximum
- Content: Overview, quick start, primary workflows
- Purpose: Immediate context for Claude
- Loading: Automatic when skill invoked

**Level 2: references/** (On-Demand Loading)
- Size: Unlimited (10,000+ words okay)
- Content: Comprehensive guides, detailed explanations, specifications
- Purpose: Deep dives when needed
- Loading: Claude explicitly references when detail needed

**Level 3: scripts/** (Execution Loading)
- Size: Unlimited code
- Content: Automation scripts, validators, helpers
- Purpose: Executable tools
- Loading: When automation invoked

### When to Use Each Level

**Put in SKILL.md**:
- Skill overview and purpose
- Quick start guide
- Common workflows (80% use cases)
- Decision trees for choosing approaches
- Links to references for details

**Put in references/**:
- Comprehensive guides (>2,000 words)
- Detailed specifications
- In-depth explanations
- Reference tables and matrices
- Historical context
- Advanced techniques

**Put in scripts/**:
- Validation scripts
- Automation helpers
- Code generators
- Analysis tools
- Testing utilities

### Context Window Optimization

**Problem**: Large skills consume context window
**Solution**: Progressive disclosure

**Before Optimization** (Everything in SKILL.md):
```
SKILL.md: 15,000 words
Context used: ~30,000 tokens
Claude has: ~70,000 tokens remaining for work
```

**After Optimization** (Progressive disclosure):
```
SKILL.md: 3,000 words
references/: 12,000 words (loaded when needed)
Context used: ~6,000 tokens (initial)
Claude has: ~94,000 tokens remaining for work
```

**Result**: 5x context efficiency!

### Reference Linking Best Practices

**Good Reference Link**:
```markdown
For comprehensive YAML guide, see [references/yaml-frontmatter-complete-guide.md](references/yaml-frontmatter-complete-guide.md)
```

**What makes it good**:
- Clear description of what's in reference
- Full relative path
- Descriptive file name

**Bad Reference Link**:
```markdown
See the guide [here](references/guide.md)
```

**What's wrong**:
- Vague "here" link
- Non-descriptive file name
- Unclear what guide contains

---

## 10 Community Innovations

Patterns discovered from analyzing 40+ community skills:

### 1. Plan-Validate-Execute Pattern
**Innovation**: Explicit planning phase before execution
**Structure**:
```
1. Analyze requirements
2. Create plan
3. Validate plan with user
4. Execute plan
5. Validate results
```
**Benefit**: Fewer errors, user confidence, better outcomes

---

### 2. Feedback Loop Integration
**Innovation**: Built-in improvement cycles
**Structure**:
```
Execute → Measure → Analyze → Improve → Repeat
```
**Benefit**: Continuous improvement, self-correcting

---

### 3. Superpowers Workflow
**Innovation**: Multi-skill composition for complex tasks
**Structure**:
```
Skill A (research) → Skill B (plan) → Skill C (execute) → Skill D (validate)
```
**Benefit**: Compound capabilities, modular design

---

### 4. Size-Constrained Validation
**Innovation**: Automated checks for SKILL.md size
**Implementation**: Script validates <5,000 words, warns if exceeded
**Benefit**: Maintains context efficiency

---

### 5. Template-Driven Output
**Innovation**: Standardized output formats
**Structure**: templates/ directory with reusable formats
**Benefit**: Consistency, faster creation

---

### 6. Conditional Loading
**Innovation**: Load different references based on context
**Example**: Development vs Production guides
**Benefit**: Context-appropriate information

---

### 7. Domain-Specific Libraries
**Innovation**: Skill-specific helper libraries
**Example**: FHIR validation library for medical skills
**Benefit**: Reusable code, consistent validation

---

### 8. Category Organization
**Innovation**: Skills organized by category in repository
**Structure**: .claude/skills/[category]/[skill-name]/
**Benefit**: Easier navigation, logical grouping

---

### 9. Auto-Generated Documentation
**Innovation**: Scripts generate documentation from code
**Example**: API documentation from endpoint definitions
**Benefit**: Always up-to-date, reduced maintenance

---

### 10. Multi-Phase Validation
**Innovation**: Validation in multiple stages
**Phases**:
1. Syntax validation (YAML, Markdown)
2. Structure validation (files, organization)
3. Content validation (completeness, quality)
4. Functional validation (scripts work, links valid)
5. Integration validation (works with Claude)
**Benefit**: Comprehensive quality assurance

---

## Common Patterns Summary

**YAML Frontmatter**:
- name: hyphen-case, descriptive
- description: <1024 chars, what + triggers

**File Organization**:
- SKILL.md: <5,000 words
- references/: Detailed guides
- scripts/: Automation
- templates/: Reusable patterns

**Writing Style**:
- Imperative/infinitive voice
- Specific, actionable instructions
- Examples included
- Progressive disclosure

**Organizational Patterns**:
1. Workflow: Sequential steps
2. Task: Independent operations
3. Reference: Standards and guidelines
4. Capabilities: Integrated features

**See References**:
- [yaml-frontmatter-complete-guide.md](references/yaml-frontmatter-complete-guide.md)
- [writing-style-imperative-guide.md](references/writing-style-imperative-guide.md)
- [reference-organization-strategies.md](references/reference-organization-strategies.md)

---

## Automation Tools Overview

This skill includes 4 automation scripts:

### init-skill.py
**Purpose**: Initialize new skill with template
**Usage**:
```bash
python scripts/init-skill.py skill-name [--template PATTERN] [--interactive]
```
**Features**:
- Scaffolds directory structure
- Creates SKILL.md with frontmatter
- Supports 5 templates (minimal, workflow, task, reference, capabilities)
- Interactive mode for guided setup

---

### validate-skill.py
**Purpose**: Multi-phase skill validation
**Usage**:
```bash
python scripts/validate-skill.py skill-name/
```
**Validation Phases**:
1. YAML frontmatter (12 checks)
2. File structure (10 checks)
3. Content quality (10 checks)
4. Script functionality (10 checks)
5. Advanced validation (links, duplication, size)
**Exit Codes**: 0=pass, 1=fixable errors, 2=fatal errors

---

### analyze-description.py
**Purpose**: Analyze description for trigger effectiveness
**Usage**:
```bash
python scripts/analyze-description.py skill-name/
```
**Analysis**:
- Trigger keyword extraction
- Action verb detection
- Technology/domain term detection
- Specificity scoring (0-100)
- Improvement suggestions

---

### package-skill.sh
**Purpose**: Package skill for distribution
**Usage**:
```bash
bash scripts/package-skill.sh skill-name/
```
**Process**:
1. Validates skill
2. Creates zip archive
3. Excludes system files (.DS_Store, etc.)
4. Outputs to dist/

**See**: [references/script-integration-patterns.md](references/script-integration-patterns.md) for script development guide

---

## Troubleshooting Quick Fixes

### Issue: Claude doesn't invoke skill

**Causes**:
- Vague description lacking trigger keywords
- Name not discoverable
- Skill not in .claude/skills/ directory

**Fixes**:
1. Add trigger keywords to description
2. Use task-specific verbs (deploy, validate, analyze)
3. Include domain terms (FHIR, Railway, testing)
4. Verify skill location: .claude/skills/skill-name/SKILL.md

---

### Issue: SKILL.md too large

**Causes**:
- All details in SKILL.md
- Not using progressive disclosure

**Fixes**:
1. Move detailed guides to references/
2. Keep SKILL.md <5,000 words
3. Link to references for details
4. Use scripts/ for code examples

---

### Issue: Content feels duplicated

**Causes**:
- Repeating information across files
- Not using references properly

**Fixes**:
1. Consolidate duplicate content
2. Use single source of truth
3. Link to authoritative source
4. See [references/anti-patterns-and-fixes.md](references/anti-patterns-and-fixes.md)

---

### Issue: Validation fails

**Causes**:
- YAML syntax errors
- Missing required fields
- File structure issues

**Fixes**:
1. Run `python scripts/validate-skill.py skill-name/`
2. Check YAML indentation (spaces not tabs)
3. Verify name matches directory
4. Ensure description <1024 characters

---

### Issue: Skills not improving

**Causes**:
- No iteration process
- Not tracking feedback
- No usage analysis

**Fixes**:
1. Establish improvement cycle
2. Track usage patterns
3. Gather feedback regularly
4. Version in git for history
5. See [Step 6: Iterate & Improve](#step-6-iterate--improve)

---

## Next Steps

**To Learn More**:
- Read [references/yaml-frontmatter-complete-guide.md](references/yaml-frontmatter-complete-guide.md) for YAML details
- Read [references/progressive-disclosure-architecture.md](references/progressive-disclosure-architecture.md) for context optimization
- Read [references/validation-checklist-complete.md](references/validation-checklist-complete.md) for quality standards

**To Create Your First Skill**:
1. Follow [Quick Start: 5-Minute Skill](#quick-start-5-minute-skill)
2. Use [Step 1: Understand Requirements](#step-1-understand-requirements) to define scope
3. Apply [4 Organizational Patterns](#4-organizational-patterns) to choose structure
4. Build iteratively using [6-Step Process](#6-step-creation-process)

**To Use Templates**:
- See templates/ directory for 5 ready-to-use patterns
- Copy template matching your needs
- Customize for your domain

**To Validate Quality**:
- Run `python scripts/validate-skill.py skill-name/`
- Review [references/validation-checklist-complete.md](references/validation-checklist-complete.md)
- Analyze description with `python scripts/analyze-description.py skill-name/`

---

**Version**: 1.0
**Research**: 11 sources, 40+ community skills analyzed
**Last Updated**: October 25, 2025
**Skill Type**: Reference/Guidelines (meta-skill for creating skills)
