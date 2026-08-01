---
name: agent-creator-majiayu000-claude-skill-regist
description: Use this skill when architecting new Claude Code agents following Anthropic
  best practices. Guides through YAML frontmatter creation, agent structure definition,
  role boundaries, and validation. Criti
---

---
name: agent-creator
description: Use this skill when architecting new Claude Code agents following Anthropic best practices. Guides through YAML frontmatter creation, agent structure definition, role boundaries, and validation. Critical for creating minimal agent files (~150 lines) with proper skill invocations. Examples: <example>Context: User wants to create a new agent for security auditing user: "Create a security-auditor agent" assistant: "I'll use the agent-creator skill to build this agent following Anthropic best practices" <commentary>New agent creation requires the agent-creator skill to ensure proper structure and YAML frontmatter.</commentary></example> <example>Context: Existing agent file is too verbose and needs refactoring user: "The architect agent is 2000 lines, refactor it to minimal structure" assistant: "I'll use the agent-creator skill to refactor this into a minimal ~150 line agent with a separate skill file" <commentary>Agent refactoring requires the agent-creator skill to separate identity from technical procedures.</commentary></example>
color: orange
---

# Agent Creator Skill

**Purpose**: Guide creation of Claude Code agents following Anthropic official best practices.

**When to use**: Creating new agents, refactoring existing agents, validating agent structure.

---

## 🎯 Core Principles

### Agent Structure Philosophy
- **Minimal agents (~150 lines)**: Only identity, role, boundaries, and skill invocation
- **Comprehensive skills**: All technical procedures, workflows, and references
- **Progressive disclosure**: Metadata → Agent .md → SKILL.md → References (on demand)
- **Mandatory skill invocation**: Agents MUST invoke their skill before work

### Separation of Concerns
```
Agent .md (150 lines)           Skill SKILL.md (varies)
├─ YAML frontmatter             ├─ Technical workflows
├─ Identity & role              ├─ Context7 checkpoints
├─ Authority & boundaries       ├─ MCP integrations
├─ Workspace isolation          ├─ Best practices
├─ Mandatory skill call         ├─ Code patterns
└─ Quick reference              └─ References/ (on demand)
```

---

## 📋 6-PHASE WORKFLOW

### PHASE 1: Discovery & Analysis

**Objective**: Understand the agent's purpose and role in the system.

**Steps**:
1. Identify the agent's primary responsibility
2. Determine where it fits in the workflow (Architect → Test → Implementer → Supabase → UI/UX)
3. Define clear trigger scenarios (when should this agent activate?)
4. List exclusive authorizations (what ONLY this agent can do)
5. Define strict prohibitions (what this agent must NEVER do)

**Questions to answer**:
- What problem does this agent solve?
- What are its inputs and outputs?
- Which other agents does it interact with?
- What are its success criteria?

**Deliverable**: Written notes on agent's role, triggers, and boundaries

---

### PHASE 2: Context7 Research (MANDATORY)

**Objective**: Consult official Anthropic documentation for latest best practices.

**⚠️ CRITICAL**: You MUST query Context7 before creating or refactoring agents.

**Required queries**:

```bash
# Query 1: General agent best practices
mcp__context7__resolve-library-id "claude code"
mcp__context7__get-library-docs "/anthropics/claude-code" topic="custom agents creation best practices"

# Query 2: Agent templates and examples
mcp__context7__resolve-library-id "claude code templates"
mcp__context7__get-library-docs "/davila7/claude-code-templates" topic="agent creation yaml structure examples"

# Query 3: YAML frontmatter validation (if uncertain)
mcp__context7__get-library-docs "/anthropics/claude-code" topic="yaml frontmatter agent configuration"
```

**What to look for**:
- ✅ Latest YAML frontmatter requirements
- ✅ Agent file structure changes
- ✅ Description formatting patterns
- ✅ Example agent implementations
- ✅ Validation rules and common mistakes

**Reference documents** (consult if Context7 unavailable):
- `references/context7-queries.md` - Pre-built query patterns
- `references/yaml-frontmatter-guide.md` - YAML validation rules

**Deliverable**: Notes on any differences from existing patterns, new requirements

---

### PHASE 3: YAML Frontmatter Design

**Objective**: Create valid, descriptive YAML frontmatter for the agent.

**Required fields**:
```yaml
---
name: {agent-name}          # kebab-case REQUIRED
description: ...            # Trigger + examples REQUIRED
model: sonnet               # Default REQUIRED
color: {color}              # Visual ID REQUIRED
---
```

**Description structure** (CRITICAL):
```
Use this agent when {trigger scenario}. Specializes in {expertise}.
Examples:
<example>
Context: {situation}
user: '{request}'
assistant: '{response}'
<commentary>{reasoning}</commentary>
</example>
<example>
Context: {another situation}
user: '{another request}'
assistant: '{another response}'
<commentary>{more reasoning}</commentary>
</example>
```

**Naming conventions**:
- **Name**: kebab-case (test-architect, ui-ux-expert, supabase-data-specialist)
- **Color**: Match role type (see `references/color-conventions.md`)
  - red = Architect/Chief
  - blue = Testing/QA
  - yellow = Implementation
  - green = Data/Database
  - pink = UI/UX
  - purple = Security/Review
  - orange = DevOps/Infrastructure

**Examples reference**: `assets/yaml-examples.yml`

**Validation checklist**:
- [ ] Name is kebab-case (lowercase-with-hyphens)
- [ ] Description starts with "Use this agent when..."
- [ ] Description has 2-3 `<example>` blocks
- [ ] Each example has Context, user, assistant, `<commentary>`
- [ ] Model is "sonnet"
- [ ] Color matches role convention
- [ ] YAML syntax is valid (no unescaped colons)

**Deliverable**: Complete YAML frontmatter block

---

### PHASE 4: Agent Body Structure

**Objective**: Create the minimal ~150 line agent body following standard structure.

**Template**: Use `assets/agent-minimal-template.md` as base.

**Required sections** (in order):

#### 1. IDENTITY & ROLE
```markdown
# IDENTITY & ROLE

You are the **{Agent Title}**—{one-sentence mission}.

## Core Mission

{2-3 paragraphs explaining:
 - What this agent does
 - Why it exists
 - How it fits in the system}

## Authority & Boundaries

**YOU ARE THE ONLY AGENT AUTHORIZED TO**:
- {Specific responsibility 1}
- {Specific responsibility 2}
- {Specific responsibility 3}

**YOU ARE STRICTLY PROHIBITED FROM**:
- {Specific prohibition 1}
- {Specific prohibition 2}
- {Specific prohibition 3}
```

**Tips**:
- Be SPECIFIC, not vague (❌ "handle data" → ✅ "implement Supabase RLS policies")
- Use active voice and imperative mood
- Clearly separate what this agent CAN vs CANNOT do

#### 2. ITERATIVE WORKFLOW v2.0
```markdown
# ITERATIVE WORKFLOW v2.0

## Your Workspace

**Isolated folder**: `PRDs/{domain}/{feature}/{agent-name}/`

**Files YOU read**:
- ✅ `{agent-name}/00-request.md` (Architect writes)
- ✅ `architect/00-master-prd.md` (reference)
- ✅ `{previous-agent}/handoff-XXX.md` (if enabled)

**Files you CANNOT read**:
- ❌ Other agent folders (Architect coordinates information)
```

**Purpose**: Establish workspace isolation and file access boundaries.

#### 3. MANDATORY SKILL INVOCATION
```markdown
# 🎯 MANDATORY SKILL INVOCATION

**CRITICAL**: Before ANY work, invoke your technical skill:

\```
Skill: {agent-name}-skill
\```

**The skill provides**:
- ✅ Step-by-step technical procedures
- ✅ Context7 consultation checkpoints (MANDATORY phases)
- ✅ MCP integration workflows
- ✅ Technology-specific references (loaded on demand)
- ✅ Code patterns and best practices

**This skill is NOT optional—it is your complete technical manual.**
```

**Purpose**: Force agent to use its comprehensive skill before starting work.

#### 4. QUICK REFERENCE
```markdown
# QUICK REFERENCE

**Triggers**: {When to use this agent - 1-2 sentences}
**Deliverables**: {What this agent produces - bulleted list}
**Success metrics**: {How to measure completion - 2-3 criteria}

---

**Complete technical guide**: `.claude/skills/{agent-name}-skill/SKILL.md`
```

**Purpose**: Fast lookup for triggers and expected outputs.

**Validation checklist**:
- [ ] All 4 sections present (Identity, Workflow, Skill Invocation, Quick Reference)
- [ ] Agent-specific placeholders replaced (no generic {agent-name} left)
- [ ] Boundaries are specific and actionable
- [ ] Skill invocation is marked as MANDATORY/CRITICAL
- [ ] File is ~80-250 lines (not too short, not too verbose)

**Deliverable**: Complete agent .md file

---

### PHASE 5: Validation & Testing

**Objective**: Verify the agent file is valid and follows best practices.

**Automated validation**:
```bash
# Run validation script
./scripts/validate-agent.sh .claude/agents/{agent-name}.md
```

**The script checks**:
- ✅ YAML frontmatter exists and is valid
- ✅ Required YAML fields (name, description, model, color)
- ✅ Name is kebab-case
- ✅ Description has examples and commentary
- ✅ Color is valid
- ✅ All required sections present
- ✅ File length is reasonable (~80-250 lines)

**Manual validation checklist**:
- [ ] YAML frontmatter is syntactically correct
- [ ] Description triggers are clear and specific
- [ ] Examples demonstrate when to use the agent
- [ ] Commentary explains the reasoning
- [ ] Authorities are exclusive and specific
- [ ] Prohibitions prevent scope creep
- [ ] Workspace isolation is clearly defined
- [ ] Skill invocation is mandatory and emphasized
- [ ] Quick reference is accurate and complete

**Common mistakes to avoid**:
- ❌ Generic triggers ("Use when needed")
- ❌ Vague boundaries ("Handle database stuff")
- ❌ Missing examples in description
- ❌ Non-kebab-case name (TestArchitect, test_architect)
- ❌ Invalid color
- ❌ Missing skill invocation section
- ❌ Agent is >300 lines (move content to skill)

**Reference documents**:
- `references/agent-structure.md` - Complete structure guide
- `references/yaml-frontmatter-guide.md` - YAML validation details

**Deliverable**: Validated agent file passing all checks

---

### PHASE 6: Skill Scaffold Creation

**Objective**: Create the companion skill structure for this agent.

**⚠️ NOTE**: This phase creates the STRUCTURE only. The skill content is created separately using the `skill-creator` skill.

**Directory structure to create**:
```
.claude/skills/{agent-name}-skill/
├── SKILL.md                    # Main skill file (create with skill-creator)
├── metadata.json               # Skill metadata
├── references/                 # Reference documents (loaded on demand)
│   └── README.md              # Index of references
├── scripts/                    # Automation scripts
│   └── README.md              # Script documentation
└── assets/                     # Templates, examples, diagrams
    └── README.md              # Asset catalog
```

**Metadata template** (`metadata.json`):
```json
{
  "name": "{agent-name}-skill",
  "version": "1.0.0",
  "description": "Technical workflow and best practices for {agent-name} agent",
  "agent": "{agent-name}",
  "technologies": ["list", "of", "technologies"],
  "mcps_required": ["context7", "supabase", "chrome-devtools"],
  "references_count": 0,
  "last_updated": "2025-10-24"
}
```

**Reference README template** (`references/README.md`):
```markdown
# {Agent Name} Skill References

References are loaded **on demand** when specific technical guidance is needed.

## Available References

1. **{reference-name}.md** - {Brief description}
   - When to consult: {Trigger}
   - Context7 equivalent: {Query if applicable}

## Update Policy

References should be refreshed when:
- Context7 documentation changes
- New best practices emerge
- Technology versions change
- Common mistakes are identified
```

**Validation checklist**:
- [ ] Skill directory created at correct path
- [ ] metadata.json has correct agent reference
- [ ] All 4 subdirectories present (references/, scripts/, assets/, root)
- [ ] README.md files guide future content creation
- [ ] Skill name matches agent name + "-skill" suffix

**Deliverable**: Skill directory structure ready for content population

---

### 🎯 AUTOMATIC HANDOFF TO SKILL-CREATOR

**⚠️ CRITICAL**: Agent creation is NOT complete until the skill is populated with technical content.

**Now invoke the skill-creator to complete the skill**:

```
Skill: skill-creator
```

**Provide the skill-creator with this information**:

```markdown
Agent: {agent-name}
Color: {color}
Role: {role from agent mission}

Primary Responsibilities (from agent authorities):
- {Authority 1}
- {Authority 2}
- {Authority 3}

Technologies Involved:
- {List technologies this agent works with}
- {e.g., Vitest, Playwright for test-architect}
- {e.g., Supabase, PostgreSQL, RLS for supabase-agent}

Required MCP Integrations:
- context7 (MANDATORY for all agents)
- {Other MCPs: supabase, chrome-devtools, etc.}

Skill Content to Include:
- 6-phase workflow specific to this agent's role
- Context7 checkpoints (mandatory consultation phases)
- Technology-specific references (loaded on demand)
- Code pattern examples and best practices
- Common mistakes and troubleshooting guides
- Automation scripts (if applicable)

Reference the existing agent structure for consistency.
```

**Expected skill-creator deliverables**:
- ✅ SKILL.md with complete 6-phase workflow
- ✅ references/ with technology-specific best practices
- ✅ scripts/ with automation tools (if applicable)
- ✅ assets/ with templates and examples
- ✅ Updated metadata.json with accurate counts

**Once skill-creator completes**:
1. Validate the complete agent + skill package
2. Test agent invocation in Claude Code
3. Verify skill invocation from agent works
4. Update project documentation

---

**Phase 6 Complete** ✅
**Next**: Invoke `Skill: skill-creator` to populate the skill with technical content

---

## 🛠️ UTILITIES & HELPERS

### Quick Start: New Agent from Scratch

**Use the initialization script**:
```bash
./scripts/init-agent.sh <agent-name> <color> "<role-description>"

# Example:
./scripts/init-agent.sh security-auditor purple "Security review and vulnerability scanning"
```

**What it does**:
- ✅ Creates agent file from template
- ✅ Validates naming conventions
- ✅ Replaces basic placeholders
- ✅ Guides you through next steps

**Then**:
1. Edit the created file to fill in FILL_THIS placeholders
2. Add 2-3 examples to YAML description
3. Complete Core Mission section
4. Define Authority & Boundaries
5. Run validation: `./scripts/validate-agent.sh .claude/agents/{agent-name}.md`
6. Create skill structure (Phase 6)

---

### Quick Start: Refactor Existing Agent

**Steps**:
1. **Backup** the current agent file
2. **Extract** identity information:
   - Who is this agent? (title, mission)
   - What can it do exclusively? (authorities)
   - What must it never do? (prohibitions)
3. **Extract** technical content:
   - Workflows and procedures → Move to SKILL.md
   - Technology references → Move to references/
   - Code examples → Move to assets/
4. **Create** minimal agent using `assets/agent-minimal-template.md`
5. **Validate** new structure: `./scripts/validate-agent.sh`
6. **Create** skill with extracted technical content

**Before/After example**:
```
BEFORE:
- architect-agent.md: 2078 lines (identity + workflows + examples + references)

AFTER:
- architect-agent.md: 150 lines (identity + skill invocation only)
- .claude/skills/architect-agent-skill/
  ├── SKILL.md: Workflows and procedures
  ├── references/: Best practices documents
  └── assets/: Templates and examples
```

---

### Reference Documents (Load on Demand)

**Available references**:

1. **`references/agent-structure.md`**
   - **When to use**: Creating or refactoring agent structure
   - **Contains**: Complete section-by-section breakdown, common mistakes, validation tips

2. **`references/yaml-frontmatter-guide.md`**
   - **When to use**: Writing or debugging YAML frontmatter
   - **Contains**: Field specifications, validation rules, error examples, testing methods

3. **`references/context7-queries.md`**
   - **When to use**: Need to verify latest Anthropic best practices
   - **Contains**: Pre-built queries, when to consult Context7, refresh workflows

4. **`references/color-conventions.md`**
   - **When to use**: Choosing agent color
   - **Contains**: Color mapping by role, visual organization principles, validation checklist

**Loading pattern**:
- Don't load all references upfront
- Reference them by name in SKILL.md
- Agent loads specific reference when needed
- Example: "See `references/color-conventions.md` for color selection guide"

---

## ✅ SUCCESS CRITERIA

Agent creation is complete when:

- [ ] YAML frontmatter is valid and descriptive
- [ ] Agent file is 80-250 lines
- [ ] All required sections present
- [ ] Boundaries are specific and actionable
- [ ] Skill invocation is mandatory and emphasized
- [ ] `./scripts/validate-agent.sh` passes without errors
- [ ] Skill directory structure created
- [ ] Agent triggers Claude Code as expected
- [ ] Examples demonstrate clear usage patterns
- [ ] Color matches role convention

---

## 📚 ADDITIONAL RESOURCES

### Official Documentation (via Context7)
- Anthropic Claude Code docs: `/anthropics/claude-code`
- Community templates: `/davila7/claude-code-templates`

### Project-Specific
- Iterative workflow: `.claude/agents/README-ITERATIVE-V2.md`
- Agent examples: `.claude/agents/` (architect-agent, test-architect, etc.)
- PRD system: `PRDs/WORKFLOW-ITERATIVO.md`

### Scripts
- `scripts/init-agent.sh` - Initialize new agent from template
- `scripts/validate-agent.sh` - Validate agent structure and YAML

### Templates
- `assets/agent-minimal-template.md` - Complete agent template
- `assets/yaml-examples.yml` - Working YAML frontmatter examples

---

**Last Updated**: 2025-10-24
**Maintained by**: Agent Creator Skill (self-referential)
