---
name: skill-analyzer
description: Analyzes project requirements in CLAUDE.md and identifies relevant skills from SkillOS library. Populates the "Available Skills" section with indexed skills and usage guidance, and the "Missing Skills" section with project-specific skills that should be created. Use this after project-context-generator creates the initial CLAUDE.md, or when project requirements change and skill selection needs updating.
---

# Skill Analyzer

## Overview

This skill analyzes a project's CLAUDE.md file to understand requirements, then intelligently selects relevant skills from the SkillOS library and identifies project-specific skills that need to be created. It updates CLAUDE.md with a complete skills index that guides development work.

## When to Use This Skill

Use this skill when:
- Initial CLAUDE.md has been created and needs skill mapping
- Project requirements have evolved and skill selection needs updating
- Starting work on a cloned SkillOS repository for a new project
- Auditing which skills are actually relevant to the current project

**Important:** This skill requires an existing CLAUDE.md file with project context (sections 1-4). Run `project-context-generator` first if CLAUDE.md doesn't exist.

## Workflow

### Step 1: Locate and Read CLAUDE.md

Ask the user for the CLAUDE.md file location (if not provided):
- "Where is your project's CLAUDE.md file?"
- Default assumption: `./CLAUDE.md` in the current working directory

Read and parse the CLAUDE.md file, focusing on:
- Project Overview (section 1): Goals, use cases, target users
- Technical Architecture (section 2): Tech stack, structure, key decisions
- Project Constraints (section 3): Performance, security, resources
- Development Conventions (section 4): Naming, testing, code style

### Step 2: Identify SkillOS Location

Determine where the SkillOS library is located:
- Check if the current directory contains a `meta-skills/` folder
- If yes, assume SkillOS skills are in the current directory structure
- If no, ask: "Where is your SkillOS library located?"

Expected SkillOS structure:
```
SkillOS/
├── meta-skills/           # Meta-skills that operate on other skills
│   ├── project-context-generator/
│   ├── skill-analyzer/
│   └── ...
└── skills/                # General-purpose skills (optional, depends on user's organization)
    ├── frontend-design/
    ├── api-design/
    └── ...
```

### Step 3: Scan Available Skills

Traverse the SkillOS directory to build a catalog of available skills:

**For each skill found:**
1. Read the `SKILL.md` frontmatter (name + description)
2. Extract skill metadata:
   - Name
   - Description (what it does + when to use)
   - Skill type (meta-skill vs. general skill)
3. Store in a temporary catalog for analysis

**Output example:**
```
Found 15 skills in SkillOS:
  Meta-skills (3):
    - project-context-generator
    - skill-analyzer
    - skill-creator
  General skills (12):
    - frontend-design
    - api-design
    - database-schema
    - ...
```

### Step 4: Match Skills to Project Requirements

Analyze the project context against each skill's description to determine relevance.

**Matching criteria:**
- **Tech stack alignment**: Does the skill's domain match the project's technologies?
  - Example: `frontend-design` skill for a React project
- **Domain relevance**: Does the skill address problems in this project's domain?
  - Example: `pdf-processing` skill if project generates reports
- **Workflow needs**: Does the project workflow benefit from this skill?
  - Example: `docx` skill if documentation is a key deliverable
- **Explicit mentions**: Are there specific references in CLAUDE.md?
  - Example: "need to generate visualizations" → `data-visualization` skill

**Scoring approach (simple heuristic):**
- High relevance: Core to the project (e.g., frontend skill for a web app)
- Medium relevance: Potentially useful but not central
- Low relevance: Marginal or speculative utility

Select skills with High or Medium relevance.

**Example output:**
```
Selected 6 relevant skills:
  - frontend-design (High)
  - api-design (High)
  - database-schema (High)
  - docx (Medium - for documentation)
  - skill-creator (Medium - for creating project-specific skills)
  - testing-patterns (Medium)
```

### Step 5: Identify Missing Project-Specific Skills

Based on the project context, identify domain-specific skills that don't exist in the SkillOS library but should be created for this project.

**Look for:**
- **Domain models**: Unique business logic or data models
  - Example: "User membership tiers with points system" → `membership-management` skill
- **Integrations**: Third-party APIs or services
  - Example: "Stripe payment processing" → `payment-integration` skill
- **Specialized workflows**: Project-specific processes
  - Example: "ETL pipeline for customer data" → `customer-data-pipeline` skill
- **Business rules**: Complex or frequently-referenced logic
  - Example: "Pricing calculation with volume discounts" → `pricing-engine` skill

**For each missing skill, define:**
- **Name**: Descriptive name for the skill
- **Rationale**: Why this skill is needed for the project
- **Suggested content**: What should be included (references, scripts, workflows)
- **Priority**: High (core to project), Medium (helpful but not critical), Low (nice-to-have)

**Example output:**
```
Identified 3 missing skills:

1. ecommerce-product-catalog (High priority)
   - Rationale: Product management is core to this e-commerce platform
   - Suggested content:
     - Product schema and category hierarchy
     - SKU generation and validation rules
     - Inventory sync workflows
     - references/product_schema.md
     - scripts/validate_sku.py

2. payment-integration (High priority)
   - Rationale: Stripe integration with custom retry logic and webhook handling
   - Suggested content:
     - Stripe API integration patterns
     - Webhook signature verification
     - Refund and chargeback workflows
     - references/stripe_api.md
     - scripts/webhook_handler.py

3. user-membership (Medium priority)
   - Rationale: Membership tiers affect pricing and features
   - Suggested content:
     - Membership tier definitions
     - Points calculation logic
     - Tier upgrade/downgrade rules
     - references/membership_rules.md
```

### Step 6: Update CLAUDE.md

Update the CLAUDE.md file with two sections:

#### Section 5: Available Skills

For each selected skill, add:
- **Skill name** (linked to the skill if possible)
- **Relevance to this project**: Brief explanation of why/when to use in this context
- **Key use cases**: Specific scenarios in this project where the skill applies
- **Related skills**: Other skills that work well in combination

**Example:**
```markdown
## 5. Available Skills

### frontend-design
**Relevance:** Core skill for building the e-commerce UI with React and Tailwind.
**Key use cases:**
- Creating product listing pages
- Building shopping cart interface
- Implementing checkout flow
**Related skills:** Works with `api-design` for data fetching, `testing-patterns` for component tests.

### api-design
**Relevance:** Guides RESTful API design for product, cart, and order endpoints.
**Key use cases:**
- Designing product catalog API
- Implementing cart management endpoints
- Creating order processing API
**Related skills:** Works with `database-schema` for data modeling.
```

#### Section 6: Missing Skills (Project-Specific)

For each identified missing skill, add:
- **Skill name**
- **Rationale**: Why it's needed
- **Suggested content**: What should be included
- **Priority**: High/Medium/Low
- **Next steps**: Guidance on creating the skill (e.g., "Use skill-creator to generate this skill")

**Example:**
```markdown
## 6. Missing Skills (Project-Specific)

### ecommerce-product-catalog
**Rationale:** Product management is core to this e-commerce platform. Centralizing product schema, SKU rules, and inventory workflows will ensure consistency.

**Suggested content:**
- `references/product_schema.md` - Product and category data models
- `references/sku_rules.md` - SKU generation and validation logic
- `scripts/validate_sku.py` - SKU validation utility

**Priority:** High

**Next steps:** Use `skill-creator` to initialize this skill, then populate with project-specific product logic.
```

Save the updated CLAUDE.md file.

### Step 7: Report Results

Present a summary to the user:

```
✅ Skill analysis complete!

📊 Results:
- Scanned 15 skills in SkillOS
- Selected 6 relevant skills (added to section 5)
- Identified 3 missing project-specific skills (added to section 6)

📝 Updated CLAUDE.md at [path]

🎯 Next steps:
1. Review the "Available Skills" section - adjust if any are irrelevant
2. Review the "Missing Skills" section - prioritize which to create first
3. Use `skill-creator` to build the missing skills as needed
```

## Important Notes

### Skills Stay Independent

This skill **does not modify** any skills in the SkillOS library. It only reads their metadata and creates an index in CLAUDE.md.

Project-specific context lives in CLAUDE.md, not in the skills themselves.

### Re-run When Requirements Change

As the project evolves, requirements may shift. Re-run this skill to:
- Add newly relevant skills
- Remove skills that are no longer applicable
- Update missing skills list based on new needs

### Skill Selection is Heuristic-Based

The skill matching process is not perfect. Users should review and adjust:
- Remove skills that aren't actually needed
- Add skills that were missed
- Adjust priorities for missing skills

**Encourage user review**: "Please review the selected skills and let me know if any should be added or removed."

## Resources

This skill doesn't require external references or scripts. It operates by:
1. Reading SKILL.md frontmatter from skills in SkillOS
2. Analyzing project context in CLAUDE.md
3. Applying matching heuristics
4. Updating CLAUDE.md with results
