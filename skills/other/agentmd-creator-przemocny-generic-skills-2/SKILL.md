---
name: agentmd-creator
description: >
  Create AI agent configuration files (AGENTS.md, CLAUDE.md, .cursorrules, etc.) for general-purpose and business-domain agents through guided briefing process. Use when user wants to create agent configuration file, set up AI assistant for specific role or domain, configure agent for business workflows, generate AGENTS.md or CLAUDE.md, customize AI behavior for organization, or define agent boundaries and guidelines. Trigger on phrases like create agent config, setup AI assistant, make AGENTS.md, configure agent for role, AI agent for business domain, or help me configure Claude/Cursor/Windsurf.
---

# AgentMD Creator

Create AI agent configuration files through guided briefing process for general-purpose and business-domain agents.

## Workflow

6-step process: Brief → Load References → Generate → Customize → Apply Best Practices → Present

### Step 1: Briefing Questions

Ask user these questions ONE AT A TIME (not all at once). Adapt based on answers.

**1. Agent Purpose (REQUIRED)**

"Jaki jest główny cel tego agenta? Co ma robić?"

Examples: Research assistant, Sales support, Customer service, Content creator, HR coordinator

**If unclear:** Provide examples and ask for specific scenarios
**If too broad:** Help narrow down to primary function

**2. Domain/Industry (can infer from purpose)**

"W jakiej dziedzinie lub branży będzie pracował?"

Examples: General purpose, Sales/CRM, Marketing, Finance, HR, Legal, Healthcare, Real Estate

**If general purpose:** Can skip domain-specific questions
**If unclear:** Suggest domain based on purpose

**3. IDE/Platform (REQUIRED)**

"Jakiego narzędzia używasz lub planujesz używać?"

Options:
- Claude Code → Generate `CLAUDE.md`
- Cursor → Generate `.cursor/rules/*.mdc`
- Windsurf → Generate `.windsurf/rules/*.md`
- Antigravity → Generate `.antigravity/rules.md`
- JetBrains Junie → Generate `.junie/guidelines.md`
- GitHub Copilot → Generate `.github/copilot-instructions.md`
- Multiple/Universal → Generate `AGENTS.md`

**If "don't know":** Recommend `AGENTS.md` (universal format)
**If multiple:** Generate `AGENTS.md` as base, offer platform-specific additions

**4. Specificity Level (default: Moderate if unsure)**

"Jak szczegółowy ma być agent?"

Options:
- **General** (50-100 lines): Basic role, boundaries, key references
- **Moderate** (100-200 lines): Detailed processes, tools, communication style
- **Detailed** (200-300 lines): Comprehensive workflows, templates, edge cases

**If unsure:** Default to Moderate (good balance)
**Guidance:** "Start with Moderate, can always expand later"

**5. Special Requirements (OPTIONAL)**

"Czy są jakieś specjalne wymagania? (compliance, security, specific tools, workflows)"

**If none:** Proceed with defaults from domain
**If many:** Prioritize top 2-3 most critical

### Step 2: Load Appropriate References

Based on user's answers, read relevant reference files:

**Always read:**
- `references/best-practices.md` - Universal best practices
- `references/platforms.md` - Platform-specific guidance for chosen IDE

**Read based on domain:**
- `references/use-cases.md` - Load section matching user's domain/purpose

### Step 3: Generate Configuration File

Create configuration file following this structure:

#### For AGENTS.md / CLAUDE.md (Universal Format)

```markdown
# [Project/Agent Name]

[One-line description of agent's purpose]

## Role
[Specific role definition with domain expertise]

## Tools and Systems
[List of tools, platforms, credentials locations]

## Knowledge Base
[Locations of documentation, templates, policies]

## Communication Style
[Tone, format, timing preferences]

## Workflows
[Key processes this agent handles]

## Important Notes
[Domain-specific gotchas, warnings, critical information]

## Boundaries

### Always Do
[Non-negotiable actions and practices]

### Ask First
[Actions requiring human approval or verification]

### Never Do
[Forbidden actions, compliance requirements, safety measures]
```

#### For Cursor (.mdc format)

Create modular files in `.cursor/rules/`:

```markdown
---
name: "core-agent-role"
description: "Core agent behaviors and boundaries"
alwaysApply: true
---

# [Agent Role]

[Instructions]
```

Split into multiple files:
- `001-core-role.mdc` - Role and boundaries
- `100-workflows.mdc` - Process workflows
- `200-domain-knowledge.mdc` - Domain-specific knowledge

#### For Windsurf

```markdown
# [Agent Name] Rules

## Role
[Definition]

## Workflows
[Processes]

## Boundaries
[Always/Ask/Never structure]
```

Keep under 6000 characters per file.

#### For Platform-Specific

Follow platform guidelines from `references/platforms.md`

### Step 4: Customize Based on Specificity and Domain

Adapt generated configuration to match both specificity level and domain requirements.

**A. Apply Specificity Level:**

**General (50-100 lines):**
- Role definition
- Key boundaries (Always/Never only)
- Critical tools/systems
- 2-3 most important workflows

**Moderate (100-200 lines):**
- Detailed role with context
- Full boundaries (Always/Ask/Never)
- All relevant tools and systems
- Communication style
- Main workflows with steps
- Important notes

**Detailed (200-300 lines):**
- Comprehensive role with examples
- Detailed boundaries with reasoning
- Complete tool ecosystem
- Communication style with templates
- All workflows with decision trees
- Knowledge base organization
- Edge cases and exceptions
- Compliance requirements

**B. Add Domain-Specific Elements:**

Based on chosen domain, enhance with specific requirements. Common domains:

- **Sales/CRM:** Lead qualification, CRM fields, follow-up sequences
- **Customer Support:** SLA targets, escalation paths, response templates
- **HR:** Confidentiality, compliance standards, approval workflows
- **Finance:** Data accuracy, approval thresholds, audit trails
- **Marketing:** Brand guidelines, content calendar, campaign tracking
- **Legal:** Document confidentiality, compliance checklists, attorney escalation

**Reference:** See `references/use-cases.md` for detailed patterns and complete guidance for each domain.

### Step 5: Apply Best Practices

Review generated configuration against quality criteria from `references/best-practices.md`.

**Quality Review Checklist:**

1. **Length Check:**
   - General: 50-100 lines? ✓
   - Moderate: 100-200 lines? ✓
   - Detailed: 200-300 lines? ✓

2. **Boundaries Complete:**
   - "Always Do" section present? ✓
   - "Ask First" section present? ✓
   - "Never Do" section present? ✓
   - At least 3 items in each? ✓

3. **Tools Specific:**
   - Platform names included? (e.g., "Salesforce" not "CRM")
   - Credential locations specified? (e.g., "1Password: Sales CRM")
   - File paths provided? (e.g., /templates/sales-emails/)

4. **Content Quality:**
   - No generic advice? ("be professional" → specify what professional means)
   - Examples concrete? (specific scenarios, not abstract descriptions)
   - References used? (links to docs, not copied content)

5. **Domain Appropriateness:**
   - Domain-specific elements included?
   - Communication style matches domain?
   - Compliance requirements covered (if applicable)?

**If any check fails:** Revise configuration before presenting to user.

**Reference:** See `references/best-practices.md` for detailed criteria and examples.

### Step 6: Present and Iterate

1. Show generated configuration to user
2. Explain key sections and their purpose
3. Ask: "Czy chcesz jakieś zmiany lub doprecyzowania?"
4. Iterate based on feedback
5. Save to appropriate file location

## Output Format

**File Location:**
- AGENTS.md → Root of project
- CLAUDE.md → Root or `.claude/`
- .cursor/rules/*.mdc → `.cursor/rules/` directory
- .windsurf/rules/*.md → `.windsurf/rules/` directory
- .antigravity/rules.md → `.antigravity/` directory
- .junie/guidelines.md → `.junie/` directory
- .github/copilot-instructions.md → `.github/` directory

**Content:**
- Well-structured markdown
- Clear section headings
- Specific, actionable guidance
- Domain-appropriate examples
- Complete boundaries section

## Examples of Good Agent Configurations

See `references/examples.md` for complete, detailed examples including:

**Available examples:**
- **Research Assistant** (General, ~80 lines) - Systematic research with source credibility
- **Sales Assistant** (Moderate, ~150 lines) - CRM coordination with MEDDIC methodology
- **Customer Support** (Moderate, ~130 lines) - Ticket handling with escalation paths
- **HR Coordinator** (Detailed, ~200 lines) - Recruiting, onboarding, compliance

**Quick preview - Research Assistant structure:**
```markdown
# Research Assistant
[Role definition]
## Tools and Systems
[Specific tools with locations]
## Boundaries
### Always Do / Ask First / Never Do
[3-tier boundary structure]
```

**Use these examples to:**
- Match specificity level to user's choice
- Adapt structure to chosen domain
- Scale boundaries appropriately
- Format tools section correctly

See full examples in `references/examples.md`

## Tips for Success

1. **Start simple, iterate:** Begin with general config, add detail based on real usage
2. **User-specific language:** If user speaks Polish, use Polish in generated config
3. **Domain expertise:** Leverage user's domain knowledge during briefing
4. **Real examples:** Ask for actual scenarios to make config concrete
5. **Test and refine:** Encourage user to test agent and report issues

## Common Mistakes to Avoid

- **Too generic:** "Be helpful and professional" → Specify what professional means in this context
- **Too long:** 500+ lines → Split into modules or remove redundancy
- **Missing boundaries:** No clear Never section → Always include safety boundaries
- **Vague tools:** "Use CRM" → "Use Salesforce, credentials in 1Password"
- **No examples:** Abstract descriptions → Include concrete examples
- **One-size-fits-all:** Same config for all domains → Customize per domain

## Validation

Before finalizing, verify:
- [ ] Role clearly defined
- [ ] Tools/systems specified with access info
- [ ] Boundaries include all three tiers (Always/Ask/Never)
- [ ] Domain-specific guidance included
- [ ] Appropriate length for specificity level
- [ ] User confirms it matches their needs
